from nonebot.plugin import PluginMetadata, inherit_supported_adapters, require

require("nonebot_plugin_alconna")
require("nonebot_plugin_htmlrender")

from .__main__ import usage  # noqa: E402
from .config import ConfigModel  # noqa: E402

__version__ = "0.1.2"
__plugin_meta__ = PluginMetadata(
    name="CNRail",
    description="查询 12306 列车时刻表",
    usage=usage,
    type="application",
    homepage="https://github.com/lgc-NB2Dev/nonebot-plugin-cnrail",
    config=ConfigModel,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
    extra={"License": "MIT", "Author": "student_2333 & XieXiLin"},
)
