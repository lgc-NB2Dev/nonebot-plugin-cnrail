from nonebot.plugin import PluginMetadata, inherit_supported_adapters, require

from . import __main__ as __main__
from .config import ConfigModel
from .help import usage

require("nonebot_plugin_saa")

__version__ = "0.1.0"
__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-cnrail",
    description="查询 12306 列车时刻表",
    usage=usage,
    type="application",
    homepage="https://github.com/XieXiLin2/nonebot-plugin-cnrail",
    config=ConfigModel,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_saa"),
    extra={"License": "MIT", "Author": "XieXiLin"},
)
