"""Tests for the HTML pipeline of ``nonebot_plugin_cnrail.render``."""

from typing import TYPE_CHECKING

from tests_nbp_cnrail.utils.render_fakes import (
    BACKGROUND_BYTES,
    SCREENSHOT_BYTES,
    SN_SERIAL,
    THEME_CSS,
    FakeDebugWriter,
    install_render_dependencies,
    render_once,
)

if TYPE_CHECKING:
    import pytest


async def test_render_train_info_renders_summary_and_serves_background(
    cnrail_plugin: object,
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    """A successful render exposes the summary, theme CSS, background, and image."""
    from nonebot_plugin_cnrail import render

    writer = FakeDebugWriter(enabled=False)
    page = install_render_dependencies(monkeypatch, debug_writer=writer)

    image, html = await render_once(page, train_date="2026-09-19")

    assert writer.writes == []
    assert image == SCREENSHOT_BYTES
    assert page.goto_calls == [f"{render.ROUTE_BASE_URL}/"]
    assert page.wait_for_selector_calls == [("#done", "attached")]
    assert page.screenshot_calls == [{"selector": ".bg-wrapper", "type": "jpeg"}]

    html_route = page.fulfilled[f"{render.ROUTE_BASE_URL}/"]
    assert html_route.fulfill_calls == [
        {"status": 200, "content_type": "text/html", "body": html},
    ]
    for expected in (
        "G1",
        "上海虹桥",
        "北京南",
        "历时 4 时 28 分",
        "担当路局：北京局",
        "列车型号：CR400AF-2001",
        THEME_CSS,
    ):
        assert expected in html

    background_route = await page.request(f"{render.ROUTE_BASE_URL}/bg")
    assert background_route.fulfill_calls == [
        {
            "status": 200,
            "content_type": "image/png",
            "body": BACKGROUND_BYTES,
        },
    ]


async def test_render_train_info_shows_sn_matching_the_train_date(
    cnrail_plugin: object,
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    """An SN entry dated like the train replaces the train model line."""
    page = install_render_dependencies(monkeypatch)

    _image, html = await render_once(
        page,
        train_date="2026-09-19",
        sn_dates=["2026-09-19"],
        sn_serial=SN_SERIAL,
    )

    assert f"车组号：{SN_SERIAL}" in html
    assert "列车型号" not in html


async def test_render_train_info_falls_back_to_train_model_without_matching_sn(
    cnrail_plugin: object,
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    """A missing SN list and an SN dated differently both keep the model line."""
    page = install_render_dependencies(monkeypatch)

    for sn_dates in (None, ["2026-09-18"]):
        _image, html = await render_once(
            page,
            train_date="2026-09-19",
            sn_dates=sn_dates,
            sn_serial=SN_SERIAL,
        )

        assert SN_SERIAL not in html
        assert "列车型号：CR400AF-2001" in html


async def test_render_train_info_marks_arrived_stations_using_the_train_date(
    cnrail_plugin: object,
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    """The train date decides which station points are marked as already arrived."""
    page = install_render_dependencies(monkeypatch)

    _image, past_html = await render_once(page, train_date="2020-01-01")
    _image, future_html = await render_once(page, train_date="2099-01-01")

    assert "station-point arrived" in past_html
    assert "arrived" not in future_html


async def test_render_train_info_keeps_rendering_when_background_fetch_fails(
    cnrail_plugin: object,
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    """A failed background fetch still renders the card and 404s the bg route."""
    from nonebot_plugin_cnrail import render

    page = install_render_dependencies(monkeypatch, background=None)

    image, html = await render_once(page, train_date="2026-09-19")

    assert image == SCREENSHOT_BYTES
    for expected in ("G1", "上海虹桥", "北京南", "历时 4 时 28 分"):
        assert expected in html
    assert render.BACKGROUND_CSS not in html
    assert "<style>" not in html

    background_route = await page.request(f"{render.ROUTE_BASE_URL}/bg")
    assert background_route.fulfill_calls == [{"status": 404}]


async def test_render_train_info_falls_back_to_background_css_when_palette_fails(
    cnrail_plugin: object,
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    """A failed palette keeps the fetched background and uses the fallback CSS."""
    from nonebot_plugin_cnrail import render

    page = install_render_dependencies(monkeypatch, palette_fails=True)

    image, html = await render_once(page, train_date="2026-09-19")

    assert image == SCREENSHOT_BYTES
    assert render.BACKGROUND_CSS in html
    assert THEME_CSS not in html

    background_route = await page.request(f"{render.ROUTE_BASE_URL}/bg")
    assert background_route.fulfill_calls == [
        {
            "status": 200,
            "content_type": "image/png",
            "body": BACKGROUND_BYTES,
        },
    ]


async def test_render_train_info_writes_served_html_to_debug_writer(
    cnrail_plugin: object,
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    """With debugging enabled the served HTML is also written to the debug dir."""
    writer = FakeDebugWriter()
    page = install_render_dependencies(monkeypatch, debug_writer=writer)

    _image, html = await render_once(page, train_date="2026-09-19")

    assert writer.writes == [(html, "{time}.html")]
