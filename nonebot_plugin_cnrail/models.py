from datetime import datetime, timedelta
from typing import List, Optional, Union

from cookit.pyd import CamelAliasModel

from .utils import TZ_SHANGHAI


class TrainSearchData(CamelAliasModel):
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


class TrainSearchResult(CamelAliasModel):
    page_index: int
    page_size: int
    total_pages: int
    total_count: int
    data: List[TrainSearchData]


class TrainDetailViaStation(CamelAliasModel):
    station_name: str
    station_telegram_code: Optional[str]
    train_number: str
    arrival_time: Optional[str]
    departure_time: Optional[str]
    stop_minutes: int
    distance: int
    checkout_name: Optional[str]
    speed: Optional[int]
    day_index: int
    company_name: str
    province: str
    district: str
    out_of_date_flag: int
    is_turn: bool


class TrainDetailRoutingItem(CamelAliasModel):
    train_number: str
    begin_station_name: str
    departure_time: str
    end_station_name: str
    arrival_time: str


class TrainDetailRoutingMissingItem(CamelAliasModel):
    train_number: str
    begin_station_name: Optional[str]
    departure_time: Optional[str]
    end_station_name: Optional[str]
    arrival_time: Optional[str]


class TrainDetailRouting(CamelAliasModel):
    routing_items: List[Union[TrainDetailRoutingItem, TrainDetailRoutingMissingItem]]
    train_model: str


class TrainDetailData(CamelAliasModel):
    train_number: str
    train_type: str
    company_name: str
    food_coach_name: Optional[str]
    via_stations: List[TrainDetailViaStation]
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


class TrainSNData(CamelAliasModel):
    emu_serial_number: str
    date: str
    train_number: str
