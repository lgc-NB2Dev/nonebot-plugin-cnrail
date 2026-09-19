from nonebot import get_plugin_config
from nonebot.compat import field_validator, type_validate_python
from pydantic import BaseModel, Field, HttpUrl


class ConfigModel(BaseModel):
    CNRAIL_ACG_IMAGE_URL: str = Field(
        "https://www.loliapi.com/acg/pe/",
    )

    @field_validator("CNRAIL_ACG_IMAGE_URL", mode="after")
    def _validate_acg_image_url(cls, v: str) -> str:  # noqa: N805
        """Reject values that are not URLs while keeping the field a plain string."""
        type_validate_python(HttpUrl, v)
        return v


config = get_plugin_config(ConfigModel)
