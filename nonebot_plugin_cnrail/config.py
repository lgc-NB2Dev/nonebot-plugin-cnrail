from typing_extensions import Annotated

from nonebot import get_plugin_config
from pydantic import BaseModel, Field, HttpUrl


class ConfigModel(BaseModel):
    CNRAIL_ACG_IMAGE_URL: Annotated[str, HttpUrl] = Field(
        "https://www.loliapi.com/acg/pe/",
    )


config = get_plugin_config(ConfigModel)
