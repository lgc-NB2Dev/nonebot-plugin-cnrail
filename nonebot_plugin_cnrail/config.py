from nonebot import get_driver
from pydantic import BaseModel


class ConfigModel(BaseModel):
    CNRAIL_MAX_SUGGESTIONS: int = 5
    CNRAIL_MOERAIL_DOMAIN: str = "rail.re"


config: ConfigModel = ConfigModel.parse_obj(get_driver().config.dict())
