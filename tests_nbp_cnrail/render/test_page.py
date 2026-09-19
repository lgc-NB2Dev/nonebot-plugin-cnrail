"""Tests for the page/route plumbing of ``nonebot_plugin_cnrail.render``."""

from typing import Any, cast

import httpx
import pytest

from tests_nbp_cnrail.utils.render_fakes import (
    MISSING_RES_URL_PATH,
    FakeRequest,
    FakeRoute,
    http_response,
    install_fake_http_client,
)


@pytest.mark.parametrize(
    ("headers", "expected_content_type"),
    [
        ({"content-type": "image/jpeg"}, "image/jpeg"),
        ({"content-type": "image/png; charset=x"}, "image/png"),
        ({}, "image/jpeg"),
    ],
)
async def test_fetch_background_returns_body_and_normalized_content_type(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
    headers: dict[str, str],
    expected_content_type: str,
) -> None:
    """Bodies come back raw and content types lose their parameters or default."""
    from nonebot_plugin_cnrail import render

    clients = install_fake_http_client(
        monkeypatch,
        http_response(b"background-bytes", headers),
    )

    result = await render._fetch_background()

    assert result == (b"background-bytes", expected_content_type)
    assert len(clients) == 1
    assert clients[0].kwargs == {"follow_redirects": True}
    assert clients[0].closed
    assert clients[0].get_calls == [
        (str(render.config.CNRAIL_ACG_IMAGE_URL), {"follow_redirects": True}),
    ]


async def test_fetch_background_raises_on_http_error(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A non-success background response surfaces as an HTTP status error."""
    from nonebot_plugin_cnrail import render

    install_fake_http_client(monkeypatch, http_response(b"", status=503))

    with pytest.raises(httpx.HTTPStatusError):
        await render._fetch_background()


async def test_res_router_serves_bundled_files_and_404s_unknown_ones(
    cnrail_plugin: object,
) -> None:
    """The resource route maps plugin URLs onto files, and 404s missing ones."""
    from nonebot_plugin_cnrail import render
    from yarl import URL

    router = next(
        item
        for item in render.base_router_group.routers
        if item.pattern == f"{render.ROUTE_BASE_URL}/res/**/*"
    )

    async def request(url: str) -> FakeRoute:
        route = FakeRoute()
        await router.func(
            route=cast("Any", route),
            request=cast("Any", FakeRequest(url)),
            info=router,
            url=URL(url),
            matched=None,
        )
        return route

    served = await request(f"{render.ROUTE_BASE_URL}/res/assets/index.css")
    assert served.abort_calls == []
    assert served.fulfill_calls == [{"path": render.RES_PATH / "assets" / "index.css"}]
    assert (render.RES_PATH / "assets" / "index.css").is_relative_to(render.RES_PATH)

    missing = await request(f"{render.ROUTE_BASE_URL}{MISSING_RES_URL_PATH}")
    assert missing.fulfill_calls == [{"status": 404}]
