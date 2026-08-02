from dataclasses import dataclass

import httpx
from nonebot import logger
from nonebot.compat import type_validate_python

from .models import TrainDetailData, TrainSearchData, TrainSearchResult, TrainSNData

MOERAIL_API_BASE = "https://rail.moefactory.com/api/"
REQUEST_TIMEOUT = 15


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


async def generate_word(train_code: str, train_date: str) -> str:
    async with httpx.AsyncClient(
        base_url=MOERAIL_API_BASE,
        follow_redirects=True,
        timeout=REQUEST_TIMEOUT,
    ) as client:
        resp = await client.post(
            url="/trainNumber/query",
            data={
                "date": train_date.replace("-", ""),
                "trainNumber": train_code,
            },
        )
        resp.raise_for_status()
        result = type_validate_python(TrainSearchResult, resp.json()["data"])
    return f"{result.data[0].train_number} | {result.data[0].begin_station_name} - {result.data[0].end_station_name} | 耗时 {result.data[0].duration_minutes} 分钟"


async def get_train_sn(train_code: str) -> list[TrainSNData] | None:
    try:
        async with httpx.AsyncClient(
            base_url=MOERAIL_API_BASE,
            follow_redirects=True,
            timeout=REQUEST_TIMEOUT,
        ) as client:
            resp = await client.post(
                url="/emuSerialNumber/query",
                data={"keyword": train_code},
            )
            resp.raise_for_status()
        payload = resp.json()

        if payload.get("code") != 200:
            logger.warning(
                f"API Error during train serial number query: {payload.get('message') or 'unknown error'}"
            )
            return None

        return (
            type_validate_python(list[TrainSNData], payload["data"])
            if payload.get("data")
            else None
        )

    except Exception:
        logger.warning("Failed to query train serial number", exc_info=True)
        return None


async def query_train_info(
    train_code: str,
    train_date: str,
) -> TrainInfo | None:
    async with httpx.AsyncClient(
        base_url=MOERAIL_API_BASE,
        follow_redirects=True,
        timeout=REQUEST_TIMEOUT,
    ) as client:
        resp = await client.post(
            url="/trainNumber/query",
            data={
                "date": train_date.replace("-", ""),
                "trainNumber": train_code,
            },
        )
        resp.raise_for_status()
        result = type_validate_python(TrainSearchResult, resp.json()["data"])

    if not result.data:
        return None

    search_data = result.data[0]
    if result.total_count > 1 and search_data.train_number != train_code:
        async with httpx.AsyncClient(
            base_url=MOERAIL_API_BASE,
            follow_redirects=True,
            timeout=REQUEST_TIMEOUT,
        ) as client:
            resp = await client.post(
                url="/search/getTrainCandidates",
                data={
                    "keywords": train_code,
                },
            )
            resp.raise_for_status()
            result = resp.json()["data"]
            if not result:
                return None
            raise MultipleTrainFoundError(result)

    async with httpx.AsyncClient(
        base_url=MOERAIL_API_BASE,
        follow_redirects=True,
        timeout=REQUEST_TIMEOUT,
    ) as client:
        resp = await client.post(
            url="/trainDetails/query",
            data={
                "date": train_date.replace("-", ""),
                "trainIndex": search_data.train_index,
            },
        )
        resp.raise_for_status()

    detail_data = type_validate_python(TrainDetailData, resp.json()["data"])

    sn_data = await get_train_sn(train_code)

    return TrainInfo(
        search=search_data,
        detail=detail_data,
        sn=sn_data,
        train_date=train_date,
    )
