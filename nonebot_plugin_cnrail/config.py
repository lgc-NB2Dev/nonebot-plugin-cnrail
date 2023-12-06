from nonebot import get_driver
from pydantic import BaseModel

# from pydantic.fields import Field
# from pydantic.networks import AnyHttpUrl


class ConfigModel(BaseModel):
    # cnrail_max_suggestions: int = 5
    # cnrail_moerail_base_url: AnyHttpUrl = Field("https://rail.re")
    pass


config: ConfigModel = ConfigModel.parse_obj(get_driver().config.dict())
