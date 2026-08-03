from datetime import datetime, timedelta

from cookit import camel_case
from cookit.pyd import model_with_alias_generator
from pydantic import BaseModel, ConfigDict, Field

from .utils import TZ_SHANGHAI


@model_with_alias_generator(camel_case)
class RailGoTimetableItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    arrive: str
    day: int
    depart: str
    run_time: int = 0
    station: str
    station_telecode: str
    stop_time: int
    train_code: str
    distance: int | None = None
    speed: float | None = None


@model_with_alias_generator(camel_case)
class RailGoTrainMainData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    bureau: str = ""
    bureau_short_name: str = ""
    car: str = ""
    car_owner: str = ""
    number_full: list[str] = Field(default_factory=list)
    number_kind: str = ""
    rundays: list[str] = Field(default_factory=list)
    runner: str = ""
    spend: int = 0
    timetable: list[RailGoTimetableItem]


@model_with_alias_generator(camel_case)
class RailGoCoachPicData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    car_code: str = ""
    car_type: str = ""
    train_style: str = ""


class RailGoV2Response(BaseModel):
    data: object | None
    msg: str = ""
    success: bool


@model_with_alias_generator(camel_case)
class TrainSearchData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    train_number: str
    begin_station_name: str
    departure_time: str
    end_station_name: str
    arrival_time: str
    duration_minutes: int
    train_type: str
    day_count: int = 1
    distance: int = 0
    cr_type: int = 0
    out_of_date_flag: int = 0

    @property
    def pass_time(self) -> str:
        days, remaining_minutes = divmod(self.duration_minutes, 60 * 24)
        hours, minutes = divmod(remaining_minutes, 60)
        day_text = f"{days} 天 " if days else ""
        return f"{day_text}{hours} 时 {minutes} 分"


@model_with_alias_generator(camel_case)
class TrainDetailViaStation(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    station_name: str
    train_number: str
    stop_minutes: int
    day_index: int
    station_telegram_code: str | None = None
    arrival_time: str | None = None
    departure_time: str | None = None
    distance: int = 0
    checkout_name: str | None = None
    speed: float | None = None
    company_name: str = ""
    province: str = ""
    district: str = ""
    out_of_date_flag: int = 0
    is_turn: bool = False


@model_with_alias_generator(camel_case)
class TrainDetailRoutingItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    train_number: str
    begin_station_name: str
    departure_time: str
    end_station_name: str
    arrival_time: str


@model_with_alias_generator(camel_case)
class TrainDetailRouting(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    routing_items: list[TrainDetailRoutingItem] = Field(default_factory=list)
    train_model: str


@model_with_alias_generator(camel_case)
class TrainDetailData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    train_number: str
    train_type: str
    company_name: str
    via_stations: list[TrainDetailViaStation]
    routing: TrainDetailRouting
    food_coach_name: str | None = None
    cr_type: int = 0

    def arrived(self, station_index: int, train_date: str) -> bool:
        station = self.via_stations[station_index]
        arrive_time_str = station.arrival_time or station.departure_time
        if not arrive_time_str:
            return False
        try:
            arrive_datetime = (
                datetime.fromisoformat(f"{train_date}T{arrive_time_str}")
                + timedelta(days=station.day_index)
            ).replace(tzinfo=TZ_SHANGHAI)
        except ValueError:
            return False
        return datetime.now(TZ_SHANGHAI) >= arrive_datetime


@model_with_alias_generator(camel_case)
class TrainSNData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    emu_serial_number: str
    date: str
    train_number: str
