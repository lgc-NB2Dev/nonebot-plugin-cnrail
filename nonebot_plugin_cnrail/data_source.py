from dataclasses import dataclass
from typing import TypeVar

import httpx
from nonebot import logger
from nonebot.compat import type_validate_python

from .models import (
    RailGoCoachPicData,
    RailGoTrainMainData,
    RailGoV2Response,
    TrainDetailData,
    TrainDetailRouting,
    TrainDetailViaStation,
    TrainSearchData,
    TrainSNData,
)

RAILGO_V1_API_BASE = "https://data.railgo.zenglingkun.cn/api/"
RAILGO_V2_API_BASE = "https://rg-api.zenglingkun.cn/api/v2/"
REQUEST_TIMEOUT = 15
USER_AGENT = "nonebot-plugin-cnrail"

T = TypeVar("T")


@dataclass
class TrainInfo:
    search: TrainSearchData
    detail: TrainDetailData
    sn: list[TrainSNData] | None
    train_date: str


class MultipleTrainFoundError(Exception):
    def __init__(self, trains: list[str]) -> None:
        self.trains = trains
        super().__init__(trains)


def _make_client(base_url: str) -> httpx.AsyncClient:
    return httpx.AsyncClient(
        base_url=base_url,
        follow_redirects=True,
        headers={"User-Agent": USER_AGENT},
        timeout=REQUEST_TIMEOUT,
    )


def _normalize_train_code(train_code: str) -> str:
    return train_code.strip().upper().split("/", 1)[0]


def _candidate_parts(train_code: str) -> set[str]:
    return {part.strip().upper() for part in train_code.split("/") if part.strip()}


async def _query_v2_data(
    client: httpx.AsyncClient,
    url: str,
    params: dict[str, str],
    model_type: type[T],
) -> T | None:
    resp = await client.get(url, params=params)
    if resp.status_code == 400:
        return None
    resp.raise_for_status()

    result = type_validate_python(RailGoV2Response, resp.json())
    if not result.success:
        logger.warning(f"RailGo API error: {result.msg or 'unknown error'}")
        return None
    if result.data is None:
        return None
    return type_validate_python(model_type, result.data)


async def _query_train_main(
    client: httpx.AsyncClient,
    train_code: str,
    train_date: str,
) -> RailGoTrainMainData | None:
    if not train_code:
        return None
    return await _query_v2_data(
        client,
        "getTrainMain",
        {"trainNum": train_code, "date": train_date},
        RailGoTrainMainData,
    )


async def _query_coach_pic(
    client: httpx.AsyncClient,
    train_code: str,
) -> RailGoCoachPicData | None:
    if not train_code:
        return None
    return await _query_v2_data(
        client,
        "getCoachPic",
        {"train": train_code},
        RailGoCoachPicData,
    )


async def _query_train_candidates(train_code: str) -> list[str]:
    async with _make_client(RAILGO_V1_API_BASE) as client:
        resp = await client.get(
            "train/preselect",
            params={"keyword": train_code.strip().upper()},
        )
        if resp.status_code == 404:
            return []
        resp.raise_for_status()

    payload = resp.json()
    if not isinstance(payload, list):
        return []
    return [item for item in payload if isinstance(item, str)]


def _display_train_number(data: RailGoTrainMainData) -> str:
    if data.number_full:
        return "/".join(data.number_full)
    return data.timetable[0].train_code


def _last_distance(data: RailGoTrainMainData) -> int:
    return max((station.distance or 0 for station in data.timetable), default=0)


def _to_search_data(data: RailGoTrainMainData) -> TrainSearchData:
    first_station = data.timetable[0]
    last_station = data.timetable[-1]
    return TrainSearchData(
        train_number=_display_train_number(data),
        begin_station_name=first_station.station,
        departure_time=first_station.depart,
        end_station_name=last_station.station,
        arrival_time=last_station.arrive,
        duration_minutes=data.spend or last_station.run_time,
        train_type=data.number_kind,
        day_count=last_station.day + 1,
        distance=_last_distance(data),
    )


def _to_detail_data(data: RailGoTrainMainData) -> TrainDetailData:
    company_name = data.bureau_short_name or data.bureau
    return TrainDetailData(
        train_number=_display_train_number(data),
        train_type=data.number_kind,
        company_name=company_name,
        via_stations=[
            TrainDetailViaStation(
                station_name=station.station,
                station_telegram_code=station.station_telecode,
                train_number=station.train_code,
                arrival_time=station.arrive,
                departure_time=station.depart,
                stop_minutes=station.stop_time,
                distance=station.distance or 0,
                speed=station.speed,
                day_index=station.day,
                company_name=company_name,
            )
            for station in data.timetable
        ],
        routing=TrainDetailRouting(train_model=data.car),
    )


def _to_train_info(
    data: RailGoTrainMainData,
    sn_data: list[TrainSNData] | None,
    train_date: str,
) -> TrainInfo | None:
    if not data.timetable:
        return None
    return TrainInfo(
        search=_to_search_data(data),
        detail=_to_detail_data(data),
        sn=sn_data,
        train_date=train_date,
    )


async def get_train_sn(train_code: str, train_date: str) -> list[TrainSNData] | None:
    try:
        async with _make_client(RAILGO_V2_API_BASE) as client:
            coach_pic = await _query_coach_pic(
                client, _normalize_train_code(train_code)
            )

        if coach_pic is None or not coach_pic.car_code:
            return None
        return [
            TrainSNData(
                emu_serial_number=coach_pic.car_code,
                date=train_date,
                train_number=train_code,
            ),
        ]

    except Exception:
        logger.warning("Failed to query train serial number", exc_info=True)
        return None


async def generate_word(train_code: str, train_date: str) -> str:
    query_code = _normalize_train_code(train_code)
    async with _make_client(RAILGO_V2_API_BASE) as client:
        data = await _query_train_main(client, query_code, train_date)

    if data is None or not data.timetable:
        return f"{train_code} | 当日未开行"

    summary = _to_search_data(data)
    return (
        f"{summary.train_number} | "
        f"{summary.begin_station_name} - {summary.end_station_name} | "
        f"耗时 {summary.duration_minutes} 分钟"
    )


async def query_train_info(
    train_code: str,
    train_date: str,
) -> TrainInfo | None:
    query_code = _normalize_train_code(train_code)

    async with _make_client(RAILGO_V2_API_BASE) as client:
        data = await _query_train_main(client, query_code, train_date)

        if data is None:
            candidates = await _query_train_candidates(train_code)
            if not candidates:
                return None

            if any(
                query_code in _candidate_parts(candidate) for candidate in candidates
            ):
                return None

            if len(candidates) > 1:
                raise MultipleTrainFoundError(candidates)

            query_code = _normalize_train_code(candidates[0])
            data = await _query_train_main(client, query_code, train_date)
            if data is None:
                return None

        sn_data = None
        coach_pic = await _query_coach_pic(client, query_code)
        if coach_pic is not None and coach_pic.car_code:
            sn_data = [
                TrainSNData(
                    emu_serial_number=coach_pic.car_code,
                    date=train_date,
                    train_number=query_code,
                ),
            ]

    return _to_train_info(data, sn_data, train_date)
