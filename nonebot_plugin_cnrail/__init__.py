from nonebot.plugin import PluginMetadata, inherit_supported_adapters, require

require("nonebot_plugin_alconna")
require("nonebot_plugin_htmlrender")

from . import __main__ as __main__  # noqa: E402
from .config import ConfigModel  # noqa: E402

__version__ = "0.1.6"
__plugin_meta__ = PluginMetadata(
    name="CNRail",
    description="查询 12306 列车时刻表",
    usage="使用指令 train -h 查看帮助",
    type="application",
    homepage="https://github.com/lgc-NB2Dev/nonebot-plugin-cnrail",
    config=ConfigModel,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
    extra={"License": "MIT", "Author": "student_2333 & XieXiLin"},
)
