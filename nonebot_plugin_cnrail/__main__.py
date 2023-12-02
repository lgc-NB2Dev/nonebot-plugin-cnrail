from arclet.alconna import Alconna
from nonebot_plugin_alconna import AlconnaMatcher, Query, on_alconna, Args, CommandMeta
from nonebot_plugin_alconna.uniseg import Text

from .utils import train_info, rail_search

# region commands
tinfo = on_alconna(
    Alconna(
        "train_info",
        Args["train?", Text],
        meta=CommandMeta(description="查询列车信息", usage="在指令后附带列车的车次"),
    ),
    aliases={"列车信息", "车次信息", "火车信息", "火车车次信息"},
    auto_send_output=True,
    use_cmd_start=True,
)

# sinfo = on_alconna(
#     Alconna(
#         "station_info",
#         Args["station?", Text],
#         meta=CommandMeta(description="查询车站信息", usage="在指令后附带车站的名称"),
#     ),
#     aliases={"车站信息", "站点信息", "火车站信息", "火车站点信息"},
#     auto_send_output=True,
#     use_cmd_start=True,
# )

rinfo = on_alconna(
    Alconna(
        "route_info",
        Args["route?", Text],
        meta=CommandMeta(description="查询交路信息", usage="在指令后附带路线的名称"),
    ),
    aliases={"交路信息", "线路信息", "火车路线信息", "火车线路信息"},
    auto_send_output=True,
    use_cmd_start=True,
)
# endregion


# region matchers
@tinfo.handle()
async def _(
    matcher: AlconnaMatcher,
    train_id_query: Query[Text] = Query("train"),
):
    train_id: str = train_id_query.result.text
    message = await train_info(train_id, matcher)
    await matcher.finish(message)


# @sinfo.handle()
# async def _(
#     matcher: AlconnaMatcher,
#     station_name_query: Query[Text] = Query("station"),
# ):
#     station_name: str = station_name_query.result.text
#     message = await train_info(station_name, matcher)
#     await matcher.finish(message)


@rinfo.handle()
async def _(
    matcher: AlconnaMatcher,
    route_name_query: Query[Text] = Query("route"),
):
    route_name: str = route_name_query.result.text
    message = await rail_search(route_name)
    await matcher.finish(message)


# endregion
