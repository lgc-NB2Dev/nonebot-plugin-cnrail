from pathlib import Path

import httpx
import jinja2 as jj
from cookit.pw import RouterGroup, make_real_path_router
from cookit.pw.loguru import log_router_err
from nonebot import logger
from nonebot_plugin_htmlrender import get_new_page
from playwright.async_api import Route
from yarl import URL

from .config import config
from .data_source import TrainInfo
from .debug import write_debug_file

RES_PATH = Path(__file__).parent / "res"
TEMPLATES_PATH = RES_PATH / "templates"

TEMPLATE_ENV = jj.Environment(
    loader=jj.FileSystemLoader(str(TEMPLATES_PATH)),
    autoescape=jj.select_autoescape(["html", "xml"]),
    enable_async=True,
)

ROUTE_BASE_URL = "https://cnrail.nonebot"

base_router_group = RouterGroup()


@base_router_group.router(f"{ROUTE_BASE_URL}/bg")
@log_router_err()
async def _(route: Route, **_):
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            resp = await client.get(config.CNRAIL_ACG_IMAGE_URL, follow_redirects=True)
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


@base_router_group.router(f"{ROUTE_BASE_URL}/res/**/*")
@log_router_err()
@make_real_path_router
async def _(url: URL, **_):
    return RES_PATH.joinpath(*url.parts[2:])


async def render_train_info(data: TrainInfo, train_date: str) -> bytes:
    template = TEMPLATE_ENV.get_template("train_table.html.jinja")
    html = await template.render_async(
        summary=data.search,
        detail=data.detail,
        sn=(
            next((i.emu_serial_number for i in data.sn if i.date == train_date), None)
            if data.sn
            else None
        ),
        train_date=data.train_date,
    )
    write_debug_file("cnrail_{time}.html", html)

    router_group = base_router_group.copy()

    @router_group.router(f"{ROUTE_BASE_URL}/")
    @log_router_err()
    async def _(route: Route, **_):
        await route.fulfill(status=200, content_type="text/html", body=html)

    async with get_new_page() as page:
        await router_group.apply(page)
        await page.goto(f"{ROUTE_BASE_URL}/")
        await page.wait_for_selector("#done", state="attached")

        elem = await page.query_selector(".bg-wrapper")
        assert elem
        return await elem.screenshot(type="jpeg")
