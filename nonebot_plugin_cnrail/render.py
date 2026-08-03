from pathlib import Path
from typing import TYPE_CHECKING, cast

import httpx
import jinja2 as jj
from cookit.pw import RouterGroup, make_real_path_router
from cookit.pw.loguru import log_router_err
from nonebot import logger
from nonebot.utils import run_sync
from nonebot_plugin_htmlrender import get_new_page
from playwright.async_api import Route
from yarl import URL

from .colors import BACKGROUND_CSS, generate_theme_css
from .config import config
from .data_source import TrainInfo
from .utils import debug

if TYPE_CHECKING:
    from playwright.async_api import Page, Route
    from yarl import URL

RES_PATH = Path(__file__).parent / "res"
TEMPLATES_PATH = RES_PATH / "templates"

TEMPLATE_ENV = jj.Environment(
    loader=jj.FileSystemLoader(str(TEMPLATES_PATH)),
    autoescape=jj.select_autoescape(["html", "xml"]),
    enable_async=True,
)

ROUTE_BASE_URL = "https://cnrail.nonebot"

base_router_group = RouterGroup()


async def _fetch_background() -> tuple[bytes, str]:
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(config.CNRAIL_ACG_IMAGE_URL, follow_redirects=True)
    resp.raise_for_status()
    return resp.content, resp.headers.get("content-type", "image/jpeg").split(";", 1)[0]


@base_router_group.router(f"{ROUTE_BASE_URL}/res/**/*")
@log_router_err()
@make_real_path_router
async def _(url: "URL", **_):
    return RES_PATH.joinpath(*url.parts[2:])


async def render_train_info(data: TrainInfo, train_date: str) -> bytes:
    background: bytes | None = None
    background_content_type = "image/jpeg"
    theme_css = ""
    try:
        background, background_content_type = await _fetch_background()
    except Exception:
        logger.exception("Failed to fetch background image")
    if background is not None:
        try:
            theme_css = await run_sync(generate_theme_css)(background)
        except Exception:
            logger.exception("Failed to generate background color palette")
        if not theme_css:
            theme_css = BACKGROUND_CSS

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
        theme_css=theme_css,
    )
    if debug.enabled:
        debug.write(html, "{time}.html")

    router_group = base_router_group.copy()

    @router_group.router(f"{ROUTE_BASE_URL}/")
    @log_router_err()
    async def _(route: "Route", **_):
        await route.fulfill(status=200, content_type="text/html", body=html)

    @router_group.router(f"{ROUTE_BASE_URL}/bg")
    @log_router_err()
    async def _(route: "Route", **_):
        if background is None:
            await route.fulfill(status=404)
            return
        await route.fulfill(
            status=200,
            content_type=background_content_type,
            body=background,
        )

    async with get_new_page() as raw_page:
        page = cast("Page", raw_page)
        await router_group.apply(page)
        await page.goto(f"{ROUTE_BASE_URL}/")
        await page.wait_for_selector("#done", state="attached")

        return await page.locator(".bg-wrapper").screenshot(type="jpeg")
