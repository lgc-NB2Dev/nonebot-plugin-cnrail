import httpx
from typing import Optional

import asyncio

from nonebot.log import logger

from .base import Train, Train_Stop

CHINA_RAIL_SEARCH_API = "https://search.12306.cn/search/v1/h5/search?keyword={train_no}"
CHINA_RAIL_DETAIL_API = "https://kyfw.12306.cn/otn/queryTrainInfo/query?leftTicketDTO.train_no={train_no}&leftTicketDTO.train_date={date}&rand_code="


async def query_train_info(train_no: str) -> Optional[Train]:
    async with httpx.AsyncClient() as client:
        resp = await client.get(CHINA_RAIL_SEARCH_API.format(train_no=train_no))
        if resp.status_code != 200:
            return None
    if len(resp.json()["data"]) > 1:
        logger.warning(
            "More than one train found:\n",
            "\n".join([x.word for x in resp.json()["data"]]),
        )
        raise ValueError("More than one train found")
    if (
        len(resp.json()["data"]) == 0
        or resp.json()["data"][0]["params"]["station_train_code"] != train_no
    ):
        return None
    train = Train(
        **resp.json()["data"][0]["params"],
        word=resp.json()["data"][0]["word"],
        train_class_name="",
        service_type=0,
        stops=[],
    )
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            CHINA_RAIL_DETAIL_API.format(train_no=train.train_no, date=train.date)
        )
        if resp.status_code != 200:
            return None
    resp_json = resp.json()
    train.service_type = resp_json["data"]["data"][0]["service_type"]
    train.train_class_name = resp_json["data"]["data"][0]["train_class_name"]
    train.stops = [Train_Stop(**x) for x in resp_json["data"]["data"]]
