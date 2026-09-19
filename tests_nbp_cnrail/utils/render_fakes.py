"""Shared fakes and helpers for the ``nonebot_plugin_cnrail.render`` tests.

Rendering is exercised without a browser: ``render.get_new_page`` is replaced by
a page substitute which replays the routes registered through
``cookit.pw.RouterGroup`` exactly like Playwright would (the document request on
``goto``, plus explicit background and resource requests).
"""

from fnmatch import fnmatchcase
from typing import TYPE_CHECKING, Any, cast
from typing_extensions import Self

import httpx

if TYPE_CHECKING:
    import pytest

SCREENSHOT_BYTES = b"fake-jpeg-screenshot-bytes"
BACKGROUND_BYTES = b"fake-background-bytes"
THEME_CSS = "/* generated theme css */"
SN_SERIAL = "CRH380B-3676"
MISSING_RES_URL_PATH = "/res/assets/missing.css"


class FakeRoute:
    """Playwright route substitute recording how the code answers a request."""

    def __init__(self) -> None:
        self.fulfill_calls: list[dict[str, Any]] = []
        self.abort_calls: list[str | None] = []

    async def fulfill(self, **kwargs: Any) -> None:
        """Record one ``fulfill`` call."""
        self.fulfill_calls.append(kwargs)

    async def abort(self, error_code: str | None = None) -> None:
        """Record one ``abort`` call."""
        self.abort_calls.append(error_code)


class FakeRequest:
    """Request substitute exposing the ``url`` attribute cookit routers read."""

    def __init__(self, url: str) -> None:
        self.url = url


class FakeLocator:
    """Locator substitute returning canned screenshot bytes."""

    def __init__(self, page: "FakePage", selector: str) -> None:
        self.page = page
        self.selector = selector

    async def screenshot(self, **kwargs: Any) -> bytes:
        """Record the screenshot request and return the canned image."""
        self.page.screenshot_calls.append({"selector": self.selector, **kwargs})
        return self.page.screenshot_bytes


class FakePage:
    """Playwright page substitute that replays registered routes on request."""

    def __init__(self) -> None:
        self.screenshot_bytes = SCREENSHOT_BYTES
        self.routes: list[tuple[str, Any]] = []
        self.goto_calls: list[str] = []
        self.wait_for_selector_calls: list[tuple[str, str | None]] = []
        self.screenshot_calls: list[dict[str, Any]] = []
        self.fulfilled: dict[str, FakeRoute] = {}

    async def route(self, pattern: str, handler: Any) -> None:
        """Register one route handler, as Playwright does."""
        self.routes.append((pattern, handler))

    async def goto(self, url: str) -> None:
        """Record the navigation and request the document it targets."""
        self.goto_calls.append(url)
        await self.request(url)

    async def request(self, url: str) -> FakeRoute:
        """Dispatch ``url`` to the most recently registered matching route."""
        for pattern, handler in reversed(self.routes):
            if fnmatchcase(url, pattern):
                route = FakeRoute()
                await handler(route, FakeRequest(url))
                self.fulfilled[url] = route
                return route
        msg = f"no route registered for {url}"
        raise AssertionError(msg)

    def locator(self, selector: str) -> FakeLocator:
        """Return a locator bound to ``selector``."""
        return FakeLocator(self, selector)

    async def wait_for_selector(self, selector: str, state: str | None = None) -> None:
        """Record the readiness wait."""
        self.wait_for_selector_calls.append((selector, state))


class FakePageContext:
    """Async context manager yielding a prepared ``FakePage``."""

    def __init__(self, page: FakePage) -> None:
        self.page = page
        self.entered = False
        self.exited = False

    async def __aenter__(self) -> FakePage:
        self.entered = True
        return self.page

    async def __aexit__(self, *_args: object) -> None:
        self.exited = True


class FakeDebugWriter:
    """``cookit.DebugFileWriter`` substitute recording written HTML."""

    def __init__(self, *, enabled: bool = True) -> None:
        self.enabled = enabled
        self.writes: list[tuple[str, str]] = []

    def write(self, content: str, file_name: str) -> None:
        """Record one written file."""
        self.writes.append((content, file_name))


class RecordingAsyncClient:
    """``httpx.AsyncClient`` substitute serving one canned response."""

    def __init__(self, response: httpx.Response, **kwargs: Any) -> None:
        self.response = response
        self.kwargs = kwargs
        self.get_calls: list[tuple[str, dict[str, Any]]] = []
        self.closed = False

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *_args: object) -> None:
        self.closed = True

    async def get(self, url: str, **kwargs: Any) -> httpx.Response:
        """Record the request and return the canned response."""
        self.get_calls.append((url, kwargs))
        return self.response


def install_fake_page(monkeypatch: "pytest.MonkeyPatch") -> FakePage:
    """Route ``render.get_new_page`` to a recording page substitute."""
    from nonebot_plugin_cnrail import render

    page = FakePage()
    context = FakePageContext(page)
    monkeypatch.setattr(render, "get_new_page", lambda **_kwargs: context)
    return page


def install_render_dependencies(
    monkeypatch: "pytest.MonkeyPatch",
    *,
    background: tuple[bytes, str] | None = (BACKGROUND_BYTES, "image/png"),
    palette_fails: bool = False,
    debug_writer: FakeDebugWriter | None = None,
) -> FakePage:
    """Stub the background fetch, palette, and debug writer, then install a page."""
    from nonebot_plugin_cnrail import render

    async def fetch_background() -> tuple[bytes, str]:
        if background is None:
            msg = "background unavailable"
            raise RuntimeError(msg)
        return background

    def generate_theme_css(_background: bytes) -> str:
        if palette_fails:
            msg = "palette unavailable"
            raise RuntimeError(msg)
        return THEME_CSS

    monkeypatch.setattr(render, "_fetch_background", fetch_background)
    monkeypatch.setattr(render, "generate_theme_css", generate_theme_css)
    monkeypatch.setattr(
        render,
        "debug",
        debug_writer if debug_writer is not None else FakeDebugWriter(enabled=False),
    )
    return install_fake_page(monkeypatch)


def install_fake_http_client(
    monkeypatch: "pytest.MonkeyPatch",
    response: httpx.Response,
) -> list[RecordingAsyncClient]:
    """Serve ``response`` for every ``render`` HTTP request, keeping the clients."""
    from nonebot_plugin_cnrail import render

    clients: list[RecordingAsyncClient] = []

    def make_client(**kwargs: Any) -> RecordingAsyncClient:
        client = RecordingAsyncClient(response, **kwargs)
        clients.append(client)
        return client

    monkeypatch.setattr(render.httpx, "AsyncClient", make_client)
    return clients


def http_response(
    content: bytes,
    headers: dict[str, str] | None = None,
    status: int = 200,
) -> httpx.Response:
    """Build a real ``httpx.Response`` for a fake client to return."""
    return httpx.Response(
        status,
        content=content,
        headers=headers if headers is not None else {},
        request=httpx.Request("GET", "https://cnrail.test/background"),
    )


def make_train_info(
    *,
    train_date: str,
    sn_dates: list[str] | None = None,
    sn_serial: str = "CR400AF-2001",
) -> Any:
    """Build a ``TrainInfo`` from RailGo payloads through the real conversions."""
    from nonebot.compat import type_validate_python
    from nonebot_plugin_cnrail import data_source

    from tests_nbp_cnrail.utils.railgo_api import timetable_item, train_main_payload

    timetable = [
        timetable_item(
            station="上海虹桥",
            arrive="13:00",
            depart="13:05",
            trainCode="G1",
            day=0,
            distance=0,
            runTime=0,
            stopTime=5,
        ),
        timetable_item(
            station="南京南",
            arrive="15:02",
            depart="15:05",
            trainCode="G1",
            day=0,
            distance=1000,
            runTime=0,
            stopTime=3,
        ),
        timetable_item(
            station="北京南",
            arrive="17:28",
            depart="17:30",
            trainCode="G1",
            day=0,
            distance=1318,
            runTime=268,
            stopTime=2,
        ),
    ]
    payload = type_validate_python(
        data_source.RailGoTrainMainData,
        train_main_payload(timetable=timetable, spend=268),
    )
    sn = (
        [
            data_source.TrainSNData(
                emu_serial_number=sn_serial,
                date=date,
                train_number="G1",
            )
            for date in sn_dates
        ]
        if sn_dates is not None
        else None
    )
    info = data_source._to_train_info(payload, sn, train_date)
    assert info is not None
    return info


async def render_once(
    page: FakePage,
    *,
    train_date: str,
    sn_dates: list[str] | None = None,
    sn_serial: str = "CR400AF-2001",
) -> tuple[bytes, str]:
    """Render one train info page into ``page``, returning its image and HTML."""
    from nonebot_plugin_cnrail import render

    info = make_train_info(
        train_date=train_date,
        sn_dates=sn_dates,
        sn_serial=sn_serial,
    )

    image = await render.render_train_info(info, train_date)

    fulfilled = page.fulfilled[f"{render.ROUTE_BASE_URL}/"].fulfill_calls[0]
    return image, cast("str", fulfilled["body"])
