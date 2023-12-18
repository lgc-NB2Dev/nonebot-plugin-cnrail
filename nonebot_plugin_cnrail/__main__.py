import string
from contextlib import suppress
from datetime import date, datetime
from typing import Optional

from arclet.alconna import Alconna, Args, Arparma, CommandMeta
from httpx import TimeoutException
from nonebot import logger
from nonebot_plugin_alconna import AlconnaMatcher, on_alconna
from nonebot_plugin_alconna.uniseg import UniMessage

from .data_source import MultipleTrainFoundError, query_train_info, render_train_info


def parse_date(date_str: str) -> date:
    for x in string.whitespace:
        date_str = date_str.replace(x, "")
    today_date = date.today()

    def parse(df: str) -> Optional[date]:
        with suppress(ValueError):
            parsed = (
                datetime.strptime(date_str, df).replace(year=today_date.year).date()
            )
            if parsed < today_date:
                parsed = parsed.replace(year=today_date.year + 1)
            return parsed
        return None

    date_formats = ("%m/%d", "%m-%d", "%m月%d日", "%m月%d号", "%m月%d")
    if r := next((parse(x) for x in date_formats if parse(x)), None):
        return r
    raise ValueError


search_train_info = on_alconna(
    Alconna(
        "train",
        Args["train", str]["date?", str],
        meta=CommandMeta(
            description="查询列车信息",
            usage="train <车次> [日期（可选，只包含月和日）]",
            example="train G1 12-10",
        ),
    ),
    aliases={"列车信息", "查询列车"},
    skip_for_unmatch=False,
    use_cmd_start=True,
)


@search_train_info.handle()
async def _(matcher: AlconnaMatcher, parma: Arparma):
    if parma.error_info:
        await matcher.finish(f"{parma.error_info}\n使用指令 `train -h` 查看帮助")


@search_train_info.handle()
async def _(matcher: AlconnaMatcher, parma: Arparma):
    train_no: str = parma["train"]
    train_date: Optional[str] = parma["date"]

    try:
        date_obj = parse_date(train_date) if train_date else date.today()
    except ValueError:
        await matcher.finish("日期格式不正确")

    try:
        train_info = await query_train_info(train_no, date_obj.isoformat())
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
        with_date_tip = "\n（可查询日期范围一般为前二日 ~ 后十四日）" if train_date else ""
        await matcher.finish(f"未查询到车次，可能是当日未开行，请检查您的车次是否正确{with_date_tip}")

    try:
        img_bytes = await render_train_info(train_info)
    except Exception:
        logger.exception("Failed to render train info")
        await matcher.finish("渲染图片时出现错误，请检查后台输出")

    await matcher.finish(UniMessage.image(raw=img_bytes))
