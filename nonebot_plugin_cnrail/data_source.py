from pathlib import Path
from typing import List, Optional

import httpx
import jinja2
import pytz
from nonebot import logger
from nonebot.compat import type_validate_python
from nonebot_plugin_htmlrender import get_new_page
from playwright.async_api import Request, Route

# from .models import TrainInfo, TrainStation, TrainSummary
from .models import ReturnData, TrainDetailData, TrainSearchResult, TrainSNData

# CHINA_RAIL_SEARCH_API = "https://search.12306.cn/search/v1/train/search"
# CHINA_RAIL_DETAIL_API = "https://kyfw.12306.cn/otn/queryTrainInfo/query"
# RAIL_RE_API = "https://api.rail.re/"

# CNRAIL_DATA_BASE_URL = "https://cnrail-data.baka.pub/data/"

MOERAIL_API_BASE = "https://train.moefactory.com/api/"

ACG_IMAGE_URL = "https://www.loliapi.com/acg/pe/"

TEMPLATE_PATH = Path(__file__).parent / "templates" / "train_table.html.jinja"

ROUTE_BASE_URL = "https://cnrail.nonebot/"
ROUTE_IMAGE_URL = f"{ROUTE_BASE_URL}image"

TZ_SHANGHAI = pytz.timezone("Asia/Shanghai")


class MultipleTrainFoundError(Exception):
    def __init__(self, trains: List[str]) -> None:
        self.trains = trains
        super().__init__(trains)


# async def query_emu_from_train_code(train_code: str) -> Optional[List]:
#     async with httpx.AsyncClient(base_url=RAIL_RE_API, follow_redirects=True) as client:
#         resp = await client.get(f"/train/{train_code}")
#         resp.raise_for_status()

#     data = resp.json()
#     if not data:
#         return None

#     return data


# async def query_emu_from_emu_no(emu_no: str) -> Optional[List]:
#     async with httpx.AsyncClient(base_url=RAIL_RE_API, follow_redirects=True) as client:
#         resp = await client.get(f"/emu/{emu_no}")
#         resp.raise_for_status()

#     data = resp.json()
#     if not data:
#         return None

#     return data


# async def query_train_info(train_code: str, train_date: str) -> Optional[TrainInfo]:
#     train_code = train_code.upper()

#     async def get_search_data(train_code: str, train_date: str) -> Optional[List]:
#         async with httpx.AsyncClient(follow_redirects=True) as client:
#             resp = await client.get(
#                 CHINA_RAIL_SEARCH_API,
#                 params={
#                     "keyword": train_code,
#                     "date": train_date.replace("-", ""),
#                 },
#             )
#             resp.raise_for_status()

#         return resp.json()["data"]

#     raw_data = await get_search_data(train_code=train_code, train_date=train_date)
#     if not raw_data:
#         async with httpx.AsyncClient(
#             base_url=CNRAIL_DATA_BASE_URL,
#             follow_redirects=True,
#         ) as client:
#             resp = await client.get("/alias.json")
#             resp.raise_for_status()

#         try:
#             train_code = resp.json()[train_code]
#         except KeyError:
#             return None

#         raw_data = await get_search_data(train_code=train_code, train_date=train_date)
#         if not raw_data:
#             return None

#     data = type_validate_python(List[TrainSummary], raw_data)
#     if len(data) > 1:
#         summary = next(
#             (train for train in data if train.station_train_code == train_code),
#             None,
#         )
#         if not summary:
#             raise MultipleTrainFoundError(data)
#     else:
#         summary = data[0]

#     if summary.station_train_code != train_code:
#         return None

#     async with httpx.AsyncClient(follow_redirects=True) as client:
#         resp = await client.get(
#             CHINA_RAIL_DETAIL_API,
#             params={
#                 "leftTicketDTO.train_no": summary.train_no,
#                 "leftTicketDTO.train_date": train_date,
#                 "rand_code": "",
#             },
#         )
#         resp.raise_for_status()

#     raw_data = resp.json()["data"]["data"]
#     if not raw_data:
#         return None

#     stations = type_validate_python(List[TrainStation], raw_data)

#     async with httpx.AsyncClient(
#         base_url=CNRAIL_DATA_BASE_URL,
#         follow_redirects=True,
#     ) as client:
#         resp = await client.get("/maintance.json")
#         resp.raise_for_status()

#     maintancer = resp.json()[train_code]

#     today_date = datetime.now(TZ_SHANGHAI).date()
#     train_date_obj = (
#         datetime.strptime(train_date, "%Y-%m-%d").replace(tzinfo=TZ_SHANGHAI).date()
#     )

#     emu_no = None

#     if (train_date_obj <= today_date) and (
#         emu_data := await query_emu_from_train_code(train_code)
#     ):
#         for i in emu_data:
#             date_data = (
#                 datetime.strptime(i["date"], "%Y-%m-%d %H:%M")
#                 .replace(tzinfo=TZ_SHANGHAI)
#                 .date()
#             )
#             if date_data == train_date_obj:
#                 emu_no = i["emu_no"]
#                 break

#     return TrainInfo(
#         summary=summary,
#         stations=stations,
#         maintancer=maintancer,
#         emu_no=emu_no,
#     )


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

    return ReturnData(search=search_data, datail=datail_data, sn=sn_data)


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
    )
    if (dbg := Path.cwd() / "cnrail-debug.html").exists():
        dbg.write_text(html, encoding="u8")

    async def bg_router(route: Route, _: Request):
        async with httpx.AsyncClient(follow_redirects=True) as client:
            resp = await client.get(ACG_IMAGE_URL, follow_redirects=True)
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
