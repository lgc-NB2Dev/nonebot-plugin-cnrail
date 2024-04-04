from datetime import datetime, timedelta
from typing import Any, List, Optional, Tuple, cast

import pytz
from pydantic import BaseModel, Field, PrivateAttr

TZ_SHANGHAI = pytz.timezone("Asia/Shanghai")


class TrainSummary(BaseModel):
    date: str
    from_station: str
    station_train_code: str
    to_station: str
    total_num: str
    train_no: str

    @property
    def date_iso(self) -> str:
        return f"{self.date[:4]}-{self.date[4:6]}-{self.date[6:]}"

    @property
    def word(self) -> str:
        return f"{self.station_train_code} {self.from_station}-{self.to_station} | 途经 {self.total_num} 站"


class TrainStation(BaseModel):
    arrive_day_str: str
    arrive_time: str
    station_train_code: str
    station_name: str
    arrive_day_diff: str
    OT: List[Any] = Field(default_factory=list)
    start_time: str
    wz_num: str
    station_no: str
    running_time: str

    @property
    def stay_minutes(self) -> int:
        arrive_t = datetime.strptime(self.arrive_time, "%H:%M").replace(
            tzinfo=TZ_SHANGHAI,
        )
        start_t = datetime.strptime(self.start_time, "%H:%M").replace(
            tzinfo=TZ_SHANGHAI,
        )
        if arrive_t > start_t:
            start_t += timedelta(days=1)
        return (start_t - arrive_t).seconds // 60


class TrainInfo(BaseModel):
    summary: TrainSummary
    stations: List[TrainStation]
    maintancer: str
    emu_no: Optional[str]

    _arrive_next_day: Optional[bool] = PrivateAttr(None)

    @property
    def station_train_codes(self) -> List[str]:
        codes = []
        for x in (x for x in self.stations if x.station_train_code not in codes):
            codes.append(x.station_train_code)  # noqa: PERF401
        return codes

    @property
    def total_time(self) -> Tuple[int, int]:
        return cast(
            Any,
            tuple(int(x) for x in self.stations[-1].running_time.split(":")),
        )

    @property
    def date_summary(self) -> str:
        week_names = ["一", "二", "三", "四", "五", "六", "日"]
        date = datetime.fromisoformat(self.summary.date_iso)
        return f"{date.month} 月 {date.day} 日 周{week_names[date.weekday()]}"

    @property
    def arrive_next_day(self) -> bool:
        if self._arrive_next_day is None:
            self._arrive_next_day = bool(
                next((x for x in self.stations if int(x.arrive_day_diff) > 0), None),
            )
        return self._arrive_next_day

    def arrived(self, station_index: int) -> bool:
        # 不在今日到达的车次，拿不到始发日期，摆烂了
        if self.arrive_next_day:
            return True

        station = self.stations[station_index]
        arrive_time_str = (
            station.arrive_time if ":" in station.arrive_time else station.start_time
        )
        arrive_datetime = datetime.fromisoformat(
            f"{self.summary.date_iso}T{arrive_time_str}",
        ).replace(tzinfo=TZ_SHANGHAI)
        # if (day_diff := int(station.arrive_day_diff)) > 0:
        #     arrive_time += timedelta(days=day_diff)
        return datetime.now(TZ_SHANGHAI) >= arrive_datetime


# --- #


class TrainSearchData(BaseModel):
    train_index: int = Field(alias="trainIndex")
    train_number: str = Field(alias="trainNumber")
    begin_station_name: str = Field(alias="beginStationName")
    departure_time: str = Field(alias="departureTime")
    end_station_name: str = Field(alias="endStationName")
    arrival_time: str = Field(alias="arrivalTime")
    day_count: int = Field(alias="dayCount")
    duration_minutes: int = Field(alias="durationMinutes")
    distance: int = Field(alias="distance")
    train_type: str = Field(alias="trainType")
    cr_type: int = Field(alias="crType")
    out_of_date_flag: int = Field(alias="outOfDateFlag")


class TrainSearchResult(BaseModel):
    page_index: int = Field(alias="pageIndex")
    page_size: int = Field(alias="pageSize")
    total_pages: int = Field(alias="totalPages")
    total_count: int = Field(alias="totalCount")
    data: List[TrainSearchData]


class TrainSearchResponse(BaseModel):
    code: int
    data: TrainSearchResult
    message: Optional[str]


class TrainDetailviaSation(BaseModel):
    station_name: str = Field(alias="stationName")
    station_telegram_code: str = Field(alias="stationTelegramCode")
    train_number: str = Field(alias="trainNumber")
    arrive_time: Optional[str] = Field(alias="arriveTime")
    departure_time: Optional[str] = Field(alias="departureTime")
    stop_minutes: int = Field(alias="stopMinutes")
    distance: int
    checkout_name: Optional[str] = Field(alias="checkoutName")
    speed: Optional[int]
    day_index: int = Field(alias="dayIndex")
    company_name: str = Field(alias="companyName")
    province: str
    district: str
    out_of_date_flag: int = Field(alias="outOfDateFlag")
    is_turn: bool = Field(alias="isTurn")


class TrainDetailRoutingItem(BaseModel):
    train_number: str = Field(alias="trainNumber")
    begin_station_name: str = Field(alias="beginStationName")
    departure_time: str = Field(alias="departureTime")
    end_station_name: str = Field(alias="endStationName")
    arrival_time: str = Field(alias="arrivalTime")


class TrainDetailRouing(BaseModel):
    routing_items: List[TrainDetailRoutingItem] = Field(alias="routingItems")
    train_model: str = Field(alias="trainModel")


class TrainDetailData(BaseModel):
    train_number: str = Field(alias="trainNumber")
    train_type: str = Field(alias="trainType")
    company_name: str = Field(alias="companyName")
    food_coach_name: str = Field(alias="foodCoachName")
    via_stations: List[TrainDetailviaSation] = Field(alias="viaStations")
    cr_type: int = Field(alias="crType")
    routing: TrainDetailRouing


class TrainDetailResult(BaseModel):
    code: int
    data: TrainDetailData
    message: Optional[str]
