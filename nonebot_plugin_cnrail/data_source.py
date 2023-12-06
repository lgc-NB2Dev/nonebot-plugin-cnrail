from pathlib import Path
from typing import List, Optional

import httpx
import jinja2
from nonebot import logger
from nonebot_plugin_htmlrender import get_new_page
from playwright.async_api import Request, Route
from pydantic.tools import parse_obj_as

from .models import TrainInfo, TrainStation, TrainSummary

CHINA_RAIL_SEARCH_API = "https://search.12306.cn/search/v1/h5/search"
CHINA_RAIL_DETAIL_API = "https://kyfw.12306.cn/otn/queryTrainInfo/query"

ACG_IMAGE_URL = "https://www.loliapi.com/acg/pe/"

TEMPLATE_PATH = Path(__file__).parent / "templates" / "template.html.jinja"
TEMPLATE = jinja2.Template(TEMPLATE_PATH.read_text(encoding="u8"), enable_async=True)

ROUTE_BASE_URL = "https://cnrail.nonebot/"
ROUTE_IMAGE_URL = f"{ROUTE_BASE_URL}image"


class MultipleTrainFoundError(Exception):
    def __init__(self, trains: List[TrainSummary]) -> None:
        self.trains = trains
        super().__init__()


async def query_train_info(train_code: str) -> Optional[TrainInfo]:
    train_code = train_code.upper()
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(
            CHINA_RAIL_SEARCH_API,
            params={"keyword": train_code},
        )
        resp.raise_for_status()

    data = parse_obj_as(List[TrainSummary], resp.json()["data"])

    if not data:
        return None
    if len(data) > 1:
        train_summary = next(
            (train for train in data if train.params.station_train_code == train_code),
            None,
        )
        if not train_summary:
            raise MultipleTrainFoundError(data)
    else:
        train_summary = data[0]

    params = train_summary.params
    if params.station_train_code != train_code:
        return None

    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(
            CHINA_RAIL_DETAIL_API,
            params={
                "leftTicketDTO.train_no": params.train_no,
                "leftTicketDTO.train_date": params.date,
                "rand_code": "",
            },
        )
        resp.raise_for_status()

    data = resp.json()["data"]["data"]
    stations = parse_obj_as(List[TrainStation], data)
    return TrainInfo(summary=train_summary, stations=stations)


async def render_train_info(info: TrainInfo) -> bytes:
    html = await TEMPLATE.render_async(info=info)

    async def bg_router(route: Route, _: Request):
        async with httpx.AsyncClient(follow_redirects=True) as client:
            resp = await client.get(ACG_IMAGE_URL)
        try:
            resp.raise_for_status()
        except Exception:
            logger.exception("Failed to fetch image")
            await route.abort()
        else:
            await route.fulfill(
                status=resp.status_code,
                headers=dict(resp.headers),
                body=resp.content,
            )

    async def root_router(route: Route, _: Request):
        await route.fulfill(
            status=200,
            headers={"Content-Type": "text/html"},
            body=html,
        )

    async with get_new_page() as page:
        await page.route(ROUTE_BASE_URL, root_router)
        await page.route(ROUTE_IMAGE_URL, bg_router)
        await page.goto(ROUTE_BASE_URL)
        await page.wait_for_selector("#done", state="attached")

        elem = await page.query_selector(".bg-wrapper")
        assert elem
        return await elem.screenshot(type="jpeg")
