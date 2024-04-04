from pathlib import Path
from typing import List, Optional

import httpx
import jinja2
import pytz
from nonebot import logger
from nonebot.compat import type_validate_python
from nonebot_plugin_htmlrender import get_new_page
from playwright.async_api import Request, Route

from .config import config
from .models import ReturnData, TrainDetailData, TrainSearchResult, TrainSNData

MOERAIL_API_BASE = "https://train.moefactory.com/api/"

TEMPLATE_PATH = Path(__file__).parent / "templates" / "train_table.html.jinja"

ROUTE_BASE_URL = "https://cnrail.nonebot/"
ROUTE_IMAGE_URL = f"{ROUTE_BASE_URL}image"

TZ_SHANGHAI = pytz.timezone("Asia/Shanghai")


class MultipleTrainFoundError(Exception):
    def __init__(self, trains: List[str]) -> None:
        self.trains = trains
        super().__init__(trains)


async def generate_word(train_code: str, train_date: str) -> str:
    async with httpx.AsyncClient(
        base_url=MOERAIL_API_BASE,
        follow_redirects=True,
    ) as client:
        resp = await client.post(
            url="/trainNumber/query",
            data={
                "date": train_date.replace("-", ""),
                "trainNumber": train_code,
            },
        )
        resp.raise_for_status()
        result = type_validate_python(TrainSearchResult, resp.json()["data"])
    return f"{result.data[0].train_number} | {result.data[0].begin_station_name} - {result.data[0].end_station_name} | 耗时 {result.data[0].duration_minutes} 分钟"


async def get_train_sn(train_code: str) -> Optional[List[TrainSNData]]:
    async with httpx.AsyncClient(
        base_url=MOERAIL_API_BASE,
        follow_redirects=True,
    ) as client:
        resp = await client.post(
            url="/crTrainSN/query",
            data={
                "keyword": train_code,
            },
        )
        resp.raise_for_status()
    return (
        type_validate_python(List[TrainSNData], resp.json()["data"])
        if resp.json()["data"]
        else None
    )


async def query_train_info(
    train_code: str,
    train_date: str,
) -> Optional[ReturnData]:
    async with httpx.AsyncClient(
        base_url=MOERAIL_API_BASE,
        follow_redirects=True,
    ) as client:
        resp = await client.post(
            url="/trainNumber/query",
            data={
                "date": train_date.replace("-", ""),
                "trainNumber": train_code,
            },
        )
        resp.raise_for_status()
        result = type_validate_python(TrainSearchResult, resp.json()["data"])

    if result.total_count != 1 and result.data[0].train_number != train_code:
        async with httpx.AsyncClient(
            base_url=MOERAIL_API_BASE,
            follow_redirects=True,
        ) as client:
            resp = await client.post(
                url="/search/getTrainCandidates",
                data={
                    "keywords": train_code,
                },
            )
            resp.raise_for_status()
            result = resp.json()["data"]
            if not result:
                return None
            raise MultipleTrainFoundError(result)

    search_data = result.data[0]

    async with httpx.AsyncClient(
        base_url=MOERAIL_API_BASE,
        follow_redirects=True,
    ) as client:
        resp = await client.post(
            url="/trainDetails/query",
            data={
                "date": train_date.replace("-", ""),
                "trainIndex": search_data.train_index,
            },
        )
        resp.raise_for_status()

    datail_data = type_validate_python(TrainDetailData, resp.json()["data"])

    sn_data = await get_train_sn(train_code)

    return ReturnData(
        search=search_data,
        datail=datail_data,
        sn=sn_data,
        train_date=train_date,
    )


async def render_train_info(return_data: ReturnData, train_date: str) -> bytes:
    template = jinja2.Template(
        TEMPLATE_PATH.read_text(encoding="u8"),
        enable_async=True,
    )
    html = await template.render_async(
        summary=return_data.search,
        detail=return_data.datail,
        sn=(
            next((i.train_sn for i in return_data.sn if i.date == train_date), None)
            if return_data.sn
            else None
        ),
        train_date=return_data.train_date,
    )
    if (dbg := Path.cwd() / "cnrail-debug.html").exists():
        dbg.write_text(html, encoding="u8")

    async def bg_router(route: Route, _: Request):
        async with httpx.AsyncClient(follow_redirects=True) as client:
            resp = await client.get(config.CNRAIL_ACG_IMAGE_URL, follow_redirects=True)
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
