from pathlib import Path
from typing import List, Optional

import httpx
import jinja2
from nonebot import logger
from nonebot_plugin_htmlrender import get_new_page
from playwright.async_api import Request, Route
from pydantic.tools import parse_obj_as

from .models import TrainInfo, TrainStation, TrainSummary

CHINA_RAIL_SEARCH_API = "https://search.12306.cn/search/v1/train/search"
CHINA_RAIL_DETAIL_API = "https://kyfw.12306.cn/otn/queryTrainInfo/query"

ACG_IMAGE_URL = "https://www.loliapi.com/acg/pe/"

TEMPLATE_PATH = Path(__file__).parent / "templates" / "template.html.jinja"

ROUTE_BASE_URL = "https://rail.re/"
ROUTE_IMAGE_URL = f"{ROUTE_BASE_URL}image"


class MultipleTrainFoundError(Exception):
    def __init__(self, trains: List[TrainSummary]) -> None:
        self.trains = trains
        super().__init__(trains)


async def query_train_info(
    train_code: str,
    train_date: str,
) -> Optional[TrainInfo]:
    train_code = train_code.upper()

    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(
            CHINA_RAIL_SEARCH_API,
            params={
                "keyword": train_code,
                "date": train_date.replace("-", ""),
            },
        )
        resp.raise_for_status()

    raw_data = resp.json()["data"]
    if not raw_data:
        return None

    data = parse_obj_as(List[TrainSummary], raw_data)
    if len(data) > 1:
        summary = next(
            (train for train in data if train.station_train_code == train_code),
            None,
        )
        if not summary:
            raise MultipleTrainFoundError(data)
    else:
        summary = data[0]

    if summary.station_train_code != train_code:
        return None

    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(
            CHINA_RAIL_DETAIL_API,
            params={
                "leftTicketDTO.train_no": summary.train_no,
                "leftTicketDTO.train_date": train_date,
                "rand_code": "",
            },
        )
        resp.raise_for_status()

    raw_data = resp.json()["data"]["data"]
    if not raw_data:
        return None

    stations = parse_obj_as(List[TrainStation], raw_data)
    return TrainInfo(summary=summary, stations=stations)


async def render_train_info(info: TrainInfo) -> bytes:
    template = jinja2.Template(
        TEMPLATE_PATH.read_text(encoding="u8"),
        enable_async=True,
    )
    html = await template.render_async(info=info)

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
