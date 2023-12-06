from nonebot import on_command
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.adapters import Message, Event, Bot
from nonebot.params import CommandArg
from nonebot_plugin_saa import Text, Image, MessageFactory, extract_target

from .utils import query_train_info

# region command register
search_train_info = on_command("train", aliases={"列车信息"})

# endregion


@search_train_info.handle()
async def _(bot: Bot, event: Event, message: Message = CommandArg()):
    try:
        extract_target(event)
    except RuntimeError:
        logger.warning("SAA 不支持的平台，取消响应")
    train_no = str(message).strip()
    if not train_no:
        await search_train_info.finish("请输入车次")
    try:
        train_info = await query_train_info(train_no)
    except ValueError:
        await search_train_info.finish("查询到多个车次，可能是当日未开行，请检查您的车次是否正确")
    if not train_info:
        await search_train_info.finish("未查询到车次，可能是当日未开行，请检查您的车次是否正确")
