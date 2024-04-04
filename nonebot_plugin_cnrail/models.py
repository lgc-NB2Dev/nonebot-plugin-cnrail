from typing import List, Optional, Union

from pydantic import BaseModel, Field


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


class TrainSNData(BaseModel):
    train_sn: str = Field(alias="trainSN")
    date: str
    train_number: str = Field(alias="trainNumber")


class ReturnData(BaseModel):
    search: TrainSearchData
    datail: TrainDetailData
    sn: Optional[List[TrainSNData]]
