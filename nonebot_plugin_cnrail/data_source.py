from pathlib import Path
from typing import List, Optional
from datetime import datetime

import httpx
import jinja2
from nonebot import logger
from nonebot_plugin_htmlrender import get_new_page
from playwright.async_api import Request, Route
from pydantic.tools import parse_obj_as

from .models import TrainInfo, TrainStation, TrainSummary

CHINA_RAIL_SEARCH_API = "https://search.12306.cn/search/v1/train/search"
CHINA_RAIL_DETAIL_API = "https://kyfw.12306.cn/otn/queryTrainInfo/query"
RAIL_RE_API = "https://api.rail.re/"

CNRAIL_DATA_BASE_URL = "https://cnrail-data.baka.pub/data/"

ACG_IMAGE_URL = "https://www.loliapi.com/acg/pe/"

TEMPLATE_PATH = Path(__file__).parent / "templates" / "train_table.html.jinja"

ROUTE_BASE_URL = "https://cnrail.nonebot/"
ROUTE_IMAGE_URL = f"{ROUTE_BASE_URL}image"


class MultipleTrainFoundError(Exception):
    def __init__(self, trains: List[TrainSummary]) -> None:
        self.trains = trains
        super().__init__(trains)


async def query_emu_from_train_code(train_code: str) -> Optional[List]:
    async with httpx.AsyncClient(base_url=RAIL_RE_API, follow_redirects=True) as client:
        resp = await client.get(f"/train/{train_code}")
        resp.raise_for_status()

    data = resp.json()
    if not data:
        return None

    return data


async def query_emu_from_emu_no(emu_no: str) -> Optional[List]:
    async with httpx.AsyncClient(base_url=RAIL_RE_API, follow_redirects=True) as client:
        resp = await client.get(f"/emu/{emu_no}")
        resp.raise_for_status()

    data = resp.json()
    if not data:
        return None

    return data


async def query_train_info(train_code: str, train_date: str) -> Optional[TrainInfo]:
    train_code = train_code.upper()

    async def get_search_data(train_code: str, train_date: str) -> Optional[List]:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            resp = await client.get(
                CHINA_RAIL_SEARCH_API,
                params={
                    "keyword": train_code,
                    "date": train_date.replace("-", ""),
                },
            )
            resp.raise_for_status()

        return resp.json()["data"]

    raw_data = await get_search_data(train_code=train_code, train_date=train_date)
    if not raw_data:
        async with httpx.AsyncClient(
            base_url=CNRAIL_DATA_BASE_URL,
            follow_redirects=True,
        ) as client:
            resp = await client.get("/alias.json")
            resp.raise_for_status()

        train_code = resp.json()[train_code]

        raw_data = await get_search_data(train_code=train_code, train_date=train_date)
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

    async with httpx.AsyncClient(
        base_url=CNRAIL_DATA_BASE_URL,
        follow_redirects=True,
    ) as client:
        resp = await client.get("/maintance.json")
        resp.raise_for_status()

    maintancer = resp.json()[train_code]

    today_date = datetime.today().date()
    train_date_obj = datetime.strptime(train_date, "%Y-%m-%d").date()

    emu_no = None

    if (train_date_obj <= today_date) and (
        emu_data := await query_emu_from_train_code(train_code)
    ):
        for i in emu_data:
            if datetime.strptime(i["date"], "%Y-%m-%d %H:%M").date() == train_date_obj:
                emu_no = i["emu_no"]
                break

    return TrainInfo(
        summary=summary,
        stations=stations,
        maintancer=maintancer,
        emu_no=emu_no,
    )


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
