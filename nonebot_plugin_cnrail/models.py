from datetime import datetime, timedelta
from typing import List, Optional, Union
from nonebot.log import logger
import pytz
from pydantic import BaseModel, Field

TZ_SHANGHAI = pytz.timezone("Asia/Shanghai")


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

    @property
    def pass_time(self) -> str:
        start_datetime = datetime.strptime(self.departure_time, "%H:%M")
        end_datetime = datetime.strptime(self.arrival_time, "%H:%M")
        if end_datetime < start_datetime:
            end_datetime += timedelta(days=1)
        time_difference = end_datetime - start_datetime
        return f"{(str(self.day_count - 1 + time_difference.days) + ' 天') if (self.day_count - 1 + time_difference.days) > 0 else ''} {time_difference.seconds // 3600} 时 {time_difference.seconds % 3600 // 60} 分"


class TrainSearchResult(BaseModel):
    page_index: int = Field(alias="pageIndex")
    page_size: int = Field(alias="pageSize")
    total_pages: int = Field(alias="totalPages")
    total_count: int = Field(alias="totalCount")
    data: List[TrainSearchData]


class TrainDetailviaSation(BaseModel):
    station_name: str = Field(alias="stationName")
    station_telegram_code: Optional[str] = Field(alias="stationTelegramCode")
    train_number: str = Field(alias="trainNumber")
    arrival_time: Optional[str] = Field(alias="arrivalTime")
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


class TrainDetailRoutingMissingItem(BaseModel):
    train_number: str = Field(alias="trainNumber")
    begin_station_name: Optional[str] = Field(alias="beginStationName")
    departure_time: Optional[str] = Field(alias="departureTime")
    end_station_name: Optional[str] = Field(alias="endStationName")
    arrival_time: Optional[str] = Field(alias="arrivalTime")


class TrainDetailRouing(BaseModel):
    routing_items: List[
        Union[TrainDetailRoutingItem, TrainDetailRoutingMissingItem]
    ] = Field(alias="routingItems")
    train_model: str = Field(alias="trainModel")


class TrainDetailData(BaseModel):
    train_number: str = Field(alias="trainNumber")
    train_type: str = Field(alias="trainType")
    company_name: str = Field(alias="companyName")
    food_coach_name: Optional[str] = Field(alias="foodCoachName")
    via_stations: List[TrainDetailviaSation] = Field(alias="viaStations")
    cr_type: int = Field(alias="crType")
    routing: TrainDetailRouing

    def arrived(self, station_index: int, train_date: str) -> bool:  # 有待修改
        logger.debug(f"index: {station_index}, date: {train_date}")
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
        logger.debug(
            f"arrive: {arrive_time_str}, arrive_datetime: {arrive_datetime}, now: {datetime.now(TZ_SHANGHAI)}, bool: {datetime.now(TZ_SHANGHAI) >= arrive_datetime}",
        )
        return datetime.now(TZ_SHANGHAI) >= arrive_datetime


class TrainSNData(BaseModel):
    train_sn: str = Field(alias="trainSN")
    date: str
    train_number: str = Field(alias="trainNumber")


class ReturnData(BaseModel):
    search: TrainSearchData
    datail: TrainDetailData
    sn: Optional[List[TrainSNData]]
    train_date: str
