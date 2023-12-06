from pydantic import BaseModel


class Train_Stop(BaseModel):
    arrive_day_str: str
    station_name: str
    arrive_time: str
    start_time: str
    station_no: str
    running_time: str


class Train(BaseModel):
    date: str
    station_train_code: str
    train_no: str
    total_num: str
    from_station: str
    to_station: str
    word: str
    train_class_name: str
    service_type: int
    stops: list[Train_Stop]
