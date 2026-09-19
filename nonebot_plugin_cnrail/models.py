from datetime import datetime, timedelta

from cookit import camel_case
from cookit.pyd import PYDANTIC_V2, model_with_model_config
from pydantic import BaseModel, ConfigDict, Field

from .utils import TZ_SHANGHAI

if PYDANTIC_V2:
    model_config = ConfigDict(
        alias_generator=camel_case,
        populate_by_name=True,
        # validate_by_alias=True, validate_by_name=True,  # they are 2.11+
    )
else:
    model_config = ConfigDict(
        alias_generator=camel_case,
        allow_population_by_field_name=True,
    )


@model_with_model_config(model_config)
class CNRailBaseModel(BaseModel):
    pass


class RailGoTimetableItem(CNRailBaseModel):
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


class RailGoTrainMainData(CNRailBaseModel):
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


class RailGoCoachPicData(CNRailBaseModel):
    car_code: str = ""
    car_type: str = ""
    train_style: str = ""


class RailGoV2Response(CNRailBaseModel):
    data: object | None
    msg: str = ""
    success: bool


class TrainSearchData(CNRailBaseModel):
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


class TrainDetailViaStation(CNRailBaseModel):
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


class TrainDetailRoutingItem(CNRailBaseModel):
    train_number: str
    begin_station_name: str
    departure_time: str
    end_station_name: str
    arrival_time: str


class TrainDetailRouting(CNRailBaseModel):
    routing_items: list[TrainDetailRoutingItem] = Field(default_factory=list)
    train_model: str


class TrainDetailData(CNRailBaseModel):
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


class TrainSNData(CNRailBaseModel):
    emu_serial_number: str
    date: str
    train_number: str
