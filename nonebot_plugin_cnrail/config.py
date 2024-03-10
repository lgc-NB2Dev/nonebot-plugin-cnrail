from nonebot import get_plugin_config
from pydantic import BaseModel


class ConfigModel(BaseModel):
    pass


config = get_plugin_config(ConfigModel)
