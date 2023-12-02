import httpx
from nonebot.log import logger
from nonebot_plugin_alconna import AlconnaMatcher

from .config import config


async def train_info(train_code: str, matcher: AlconnaMatcher) -> str:
    async with httpx.AsyncClient() as client:
        train_search_data = (
            await client.get(
                f"https://search.12306.cn/search/v1/h5/search?keyword={train_code}"
            )
        ).json()
    logger.debug(f"12306 Search Train Response:\n{train_search_data}")
    train_data = train_search_data["data"]
    train_info = None
    for train in train_data:
        if train["params"]["station_train_code"] == train_code:
            train_info = train
            break
    if train_info is None:
        if len(train_data) == 0:
            await matcher.finish("暂未开行或车次输入有误，请核对后再试")
        else:
            await matcher.finish(
                "未找到该车次" + "，以下可能为您想搜索的车次:\n"
                if config.CNRAIL_MAX_SUGGESTIONS > 0
                else ""
                + "\n".join(
                    [
                        train["params"]["station_train_code"]
                        for train in train_data[: config.CNRAIL_MAX_SUGGESTIONS]
                    ]
                )
            )
    train_id = train_info["params"]["train_no"]
    train_date = train_info["params"]["date"]
    train_total_stops = train_info["params"]["total_num"]
    async with httpx.AsyncClient() as client:
        train_search_timeshift = (
            await client.get(
                f"https://kyfw.12306.cn/otn/queryTrainInfo/query?leftTicketDTO.train_no={train_id}&leftTicketDTO.train_date={train_date}&rand_code="
            )
        ).json()
    logger.debug(f"12306 Train Timeshift Response:\n{train_search_timeshift}")
    train_timeshift = train_search_timeshift["data"]["data"]
    has_air_condition = True if train_timeshift[0]["service"] == "1" else False
    train_start_time = train_timeshift[0]["start_time"]
    train_end_time = train_timeshift[-1]["arrive_time"]
    train_total_time = train_timeshift[-1]["running_time"]
    message = (
        f"您查询的 {train_code} 次列车信息如下:\n"
        f"运行日期: {train_date}\n"
        f"始终站: {train_timeshift[0]['station_name']} -{train_timeshift[-1]['station_name']}\n"
        f"空调服务: {'是' if has_air_condition else '否'}\n"
        f"列车始发时间：{train_start_time}\n"
        f"列车终到时间: {train_end_time}\n"
        f"列车运行时间: {train_total_time}\n"
        f"列车共途径: {train_total_stops} 个车站\n"
        f"\n"
        f"{await rail_search(train_code)}"
    )
    return message


async def rail_search(train_code: str) -> str:
    async with httpx.AsyncClient() as client:
        train_set_data = (
            await client.get(
                f"https://api.{config.CNRAIL_MOERAIL_DOMAIN}/train/{train_code}"
            )
        ).json()
    if train_set_data is not {}:
        message = "车组号:\n"
        for data, emo_no in train_set_data.items():
            message += f"{data}: {emo_no}\n"
    else:
        message = ""
    return message
