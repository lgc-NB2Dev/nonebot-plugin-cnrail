from nonebot import logger, on_command
from nonebot.adapters import Message
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot_plugin_alconna.uniseg import Image, UniMessage

from .data_source import MultipleTrainFoundError, query_train_info, render_train_info

usage = "指令：train 车次"


search_train_info = on_command("train", aliases={"列车信息"})


@search_train_info.handle()
async def _(matcher: Matcher, arg_msg: Message = CommandArg()):
    train_no = str(arg_msg).strip()
    if not train_no:
        await matcher.finish("请输入车次")

    try:
        train_info = await query_train_info(train_no)
    except MultipleTrainFoundError as e:
        much_text = "\n结果过多，仅显示前五个" if len(e.trains) > 5 else ""
        info_text = "\n".join(x.word for x in e.trains[:5])
        await matcher.finish(f"查询到多个车次，请检查您的车次是否正确\n{info_text}{much_text}")
    except Exception:
        logger.exception("Failed to query train info")
        await matcher.finish("查询信息时出现错误，请检查后台输出")

    if not train_info:
        await matcher.finish("未查询到车次，可能是当日未开行，请检查您的车次是否正确")

    try:
        img_bytes = await render_train_info(train_info)
    except Exception:
        logger.exception("Failed to render train info")
        await matcher.finish("渲染图片时出现错误，请检查后台输出")

    await UniMessage(Image(raw=img_bytes)).send(reply_to=True)
    await matcher.finish()
