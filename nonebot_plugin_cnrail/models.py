from datetime import datetime, timedelta

from cookit import camel_case
from cookit.pyd import model_with_alias_generator
from pydantic import BaseModel

from .utils import TZ_SHANGHAI


@model_with_alias_generator(camel_case)
class TrainSearchData(BaseModel):
    train_index: int
    train_number: str
    begin_station_name: str
    departure_time: str
    end_station_name: str
    arrival_time: str
    day_count: int
    duration_minutes: int
    distance: int
    train_type: str
    cr_type: int
    out_of_date_flag: int

    @property
    def pass_time(self) -> str:
        start_datetime = datetime.strptime(self.departure_time, "%H:%M").replace(
            tzinfo=TZ_SHANGHAI,
        )
        end_datetime = datetime.strptime(self.arrival_time, "%H:%M").replace(
            tzinfo=TZ_SHANGHAI,
        )
        if end_datetime < start_datetime:
            end_datetime += timedelta(days=1)
        time_difference = end_datetime - start_datetime
        return (
            f"{(str(self.day_count - 1 + time_difference.days) + ' 天') if (self.day_count - 1 + time_difference.days) > 0 else ''}"
            f" {time_difference.seconds // 3600} 时 {time_difference.seconds % 3600 // 60} 分"
        )


@model_with_alias_generator(camel_case)
class TrainSearchResult(BaseModel):
    cursor: int
    count: int
    has_more: bool
    total_count: int
    data: list[TrainSearchData]


@model_with_alias_generator(camel_case)
class TrainDetailViaStation(BaseModel):
    station_name: str
    station_telegram_code: str | None
    train_number: str
    arrival_time: str | None
    departure_time: str | None
    stop_minutes: int
    distance: int
    checkout_name: str | None
    speed: int | None
    day_index: int
    company_name: str
    province: str
    district: str
    out_of_date_flag: int
    is_turn: bool


@model_with_alias_generator(camel_case)
class TrainDetailRoutingItem(BaseModel):
    train_number: str
    begin_station_name: str
    departure_time: str
    end_station_name: str
    arrival_time: str


@model_with_alias_generator(camel_case)
class TrainDetailRoutingMissingItem(BaseModel):
    train_number: str
    begin_station_name: str | None
    departure_time: str | None
    end_station_name: str | None
    arrival_time: str | None


@model_with_alias_generator(camel_case)
class TrainDetailRouting(BaseModel):
    routing_items: list[TrainDetailRoutingItem | TrainDetailRoutingMissingItem]
    train_model: str


@model_with_alias_generator(camel_case)
class TrainDetailData(BaseModel):
    train_number: str
    train_type: str
    company_name: str
    food_coach_name: str | None
    via_stations: list[TrainDetailViaStation]
    cr_type: int
    routing: TrainDetailRouting

    def arrived(self, station_index: int, train_date: str) -> bool:  # 有待修改
        # logger.debug(f"index: {station_index}, date: {train_date}")
        station = self.via_stations[station_index]
        arrive_time_str = (
            station.arrival_time
            if station.arrival_time is not None
            else station.departure_time
        )
        arrive_datetime = (
            datetime.fromisoformat(
                f"{train_date}T{arrive_time_str}",
            )
            + timedelta(days=station.day_index)
        ).replace(tzinfo=TZ_SHANGHAI)
        # logger.debug(
        #     f"arrive: {arrive_time_str}, arrive_datetime: {arrive_datetime}, now: {datetime.now(TZ_SHANGHAI)}, bool: {datetime.now(TZ_SHANGHAI) >= arrive_datetime}",
        # )
        return datetime.now(TZ_SHANGHAI) >= arrive_datetime


@model_with_alias_generator(camel_case)
class TrainSNData(BaseModel):
    emu_serial_number: str
    date: str
    train_number: str
