from datetime import datetime, timedelta
from typing import Any, List, Optional, Tuple, cast

import pytz
from pydantic.fields import PrivateAttr
from pydantic.main import BaseModel, Field

TZ_SHANGHAI = pytz.timezone("Asia/Shanghai")


class TrainSummaryParams(BaseModel):
    date: str
    station_train_code: str
    train_no: str
    total_num: str
    from_station: str
    to_station: str


class TrainSummary(BaseModel):
    district_name: str = Field(alias="districtname")
    goto_type: int = Field(alias="gotoType")
    image: str
    image_url: str = Field(alias="imageUrl")
    need_login: bool
    params: TrainSummaryParams
    train_type: str = Field(alias="type")
    url: str
    word: str


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
        arrive_t = datetime.strptime(self.arrive_time, "%H:%M")
        start_t = datetime.strptime(self.start_time, "%H:%M")
        if arrive_t > start_t:
            start_t += timedelta(days=1)
        return (start_t - arrive_t).seconds // 60


class TrainInfo(BaseModel):
    summary: TrainSummary
    stations: List[TrainStation]

    _arrive_next_day: Optional[bool] = PrivateAttr(None)

    @property
    def total_time(self) -> Tuple[int, int]:
        return cast(
            Any,
            tuple(int(x) for x in self.stations[-1].running_time.split(":")),
        )

    @property
    def date_summary(self) -> str:
        week_names = ["一", "二", "三", "四", "五", "六", "日"]
        date = datetime.strptime(self.summary.params.date, "%Y-%m-%d")
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

        date = self.summary.params.date
        station = self.stations[station_index]
        arrive_time = datetime.strptime(
            f"{date} {station.arrive_time if ':' in station.arrive_time else station.start_time}",
            "%Y-%m-%d %H:%M",
        ).replace(tzinfo=TZ_SHANGHAI)
        # if (day_diff := int(station.arrive_day_diff)) > 0:
        #     arrive_time += timedelta(days=day_diff)
        return datetime.now(TZ_SHANGHAI) >= arrive_time