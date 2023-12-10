import datetime
from typing import Optional

from arclet.alconna import Alconna, Args, CommandMeta
from httpx import TimeoutException
from nonebot import logger
from nonebot_plugin_alconna import AlconnaMatcher, Query, on_alconna
from nonebot_plugin_alconna.uniseg import Image, UniMessage

from .data_source import MultipleTrainFoundError, query_train_info, render_train_info

usage = "指令：train 车次"


def parse_date(date_str: str) -> datetime.date:
    today = datetime.datetime.today()
    for df in ("%Y/%m/%d", "%Y-%m-%d", "%Y年%m月%d日", "%m/%d", "%m-%d", "%m月%d日"):
        try:
            parsed_date = datetime.datetime.strptime(date_str, df)
        except ValueError:
            continue
        parsed_date = parsed_date.replace(year=today.year)
        if parsed_date < today:
            parsed_date = parsed_date.replace(year=today.year + 1)
        return parsed_date.date()  # 忘了是不是这个
    raise ValueError


# search_train_info = on_command("train", aliases={"列车信息"})
search_train_info = on_alconna(
    Alconna(
        "train",
        Args["train", str]["date?", str],
        meta=CommandMeta(
            description="查询列车信息",
            usage="train 车次 [日期]",
            example="train G1 2023-12-10",
        ),
    ),
    aliases={"列车信息", "查询列车"},
    auto_send_output=True,
    use_cmd_start=True,
)


@search_train_info.handle()
async def _(
    matcher: AlconnaMatcher,
    train_no_query: Query[str] = Query("train"),
    date_query: Query[Optional[str]] = Query("date", None),
):
    train_no: str = train_no_query.result
    train_date: Optional[str] = date_query.result

    if train_date:
        try:
            train_date = parse_date(train_date).isoformat()
        except ValueError:
            await matcher.finish("日期格式不正确")
    else:
        train_date = datetime.date.today().isoformat()

    try:
        train_info = await query_train_info(train_no, train_date)
    except MultipleTrainFoundError as e:
        much_text = "\n结果过多，仅显示前五个" if len(e.trains) > 5 else ""
        info_text = "\n".join(x.word for x in e.trains[:5])
        await matcher.finish(f"查询到多个车次，请检查您的车次是否正确\n{info_text}{much_text}")
    except TimeoutException:
        await matcher.finish("查询超时，请稍后重试")
    except Exception:
        logger.exception("Failed to query train info")
        await matcher.finish("查询信息时出现错误，请检查后台输出")

    if not train_info:
        await matcher.finish("未查询到车次，可能是当日未开行，请检查您的车次是否正确\n(可查询日期范围为前二日 ~ 后十四日)")

    try:
        img_bytes = await render_train_info(train_info)
    except Exception:
        logger.exception("Failed to render train info")
        await matcher.finish("渲染图片时出现错误，请检查后台输出")

    await UniMessage(Image(raw=img_bytes)).send(reply_to=True)
    await matcher.finish()
