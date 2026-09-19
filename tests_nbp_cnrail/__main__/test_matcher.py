"""Tests for the `train` command query flow."""

from typing import TYPE_CHECKING, Any, cast

from tests_nbp_cnrail.utils.clock import freeze_clock
from tests_nbp_cnrail.utils.command_fixtures import (
    COMMAND,
    MISSING_TRAIN_TEXT,
    TODAY,
    patch_queries,
    patch_render,
    run_train_command,
)

if TYPE_CHECKING:
    import pytest
    from nonebug import App

DATE_HINT = "\n（可查询日期范围一般为前二日 ~ 后十四日）"


async def test_train_command_sends_the_rendered_image(
    app: "App",
    cnrail_plugin: object,
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    """A known train finishes with one image message carrying the rendered bytes."""
    from nonebot_plugin_alconna.uniseg import Image, UniMessage
    from nonebot_plugin_cnrail import __main__ as main

    freeze_clock(monkeypatch, main, "2024-12-15")
    train_info = cast("Any", object())
    image_bytes = b"\x89PNG-cnrail"

    async def query(train_code: str, train_date: str) -> Any:
        return train_info

    queried = patch_queries(monkeypatch, main, query)
    rendered = patch_render(monkeypatch, main, image_bytes)

    payloads = await run_train_command(app, monkeypatch, f"{COMMAND} G1")

    assert queried == [("G1", TODAY)]
    assert rendered == [(train_info, TODAY)]
    assert len(payloads) == 1
    assert isinstance(payloads[0], UniMessage)
    segment = payloads[0][0]
    assert isinstance(segment, Image)
    assert segment.raw == image_bytes


async def test_train_command_reports_a_missing_train_without_a_date(
    app: "App",
    cnrail_plugin: object,
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    """An unknown train without an explicit date finishes with the plain notice."""
    from nonebot_plugin_cnrail import __main__ as main

    freeze_clock(monkeypatch, main, "2024-12-15")

    async def query(train_code: str, train_date: str) -> Any:
        return None

    queried = patch_queries(monkeypatch, main, query)
    rendered = patch_render(monkeypatch, main, b"unused")

    payloads = await run_train_command(app, monkeypatch, f"{COMMAND} G1")

    assert queried == [("G1", TODAY)]
    assert payloads == [MISSING_TRAIN_TEXT]
    assert rendered == []


async def test_train_command_reports_a_missing_train_with_a_date_hint(
    app: "App",
    cnrail_plugin: object,
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    """An unknown train queried with an explicit date appends the date range hint."""
    from nonebot_plugin_cnrail import __main__ as main

    freeze_clock(monkeypatch, main, "2024-12-15")

    async def query(train_code: str, train_date: str) -> Any:
        return None

    queried = patch_queries(monkeypatch, main, query)
    patch_render(monkeypatch, main, b"unused")

    payloads = await run_train_command(app, monkeypatch, f"{COMMAND} G1 12-20")

    assert queried == [("G1", "2024-12-20")]
    assert payloads == [f"{MISSING_TRAIN_TEXT}{DATE_HINT}"]


async def test_train_command_lists_candidates_up_to_five(
    app: "App",
    cnrail_plugin: object,
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    """An ambiguous train lists every candidate when there are at most five."""
    from nonebot_plugin_cnrail import __main__ as main
    from nonebot_plugin_cnrail.data_source import MultipleTrainFoundError

    freeze_clock(monkeypatch, main, "2024-12-15")
    worded: list[tuple[str, str]] = []

    async def query(train_code: str, train_date: str) -> Any:
        raise MultipleTrainFoundError(["G1", "G2", "G3"])

    async def generate_word(*, train_code: str, train_date: str) -> str:
        worded.append((train_code, train_date))
        return f"{train_code} 摘要"

    patch_queries(monkeypatch, main, query)
    patch_render(monkeypatch, main, b"unused")
    monkeypatch.setattr(main, "generate_word", generate_word)

    payloads = await run_train_command(app, monkeypatch, f"{COMMAND} G1")

    assert worded == [("G1", TODAY), ("G2", TODAY), ("G3", TODAY)]
    assert payloads == [
        "查询到多个车次，请检查您的车次是否正确\nG1 摘要\nG2 摘要\nG3 摘要",
    ]


async def test_train_command_marks_overflowing_candidates(
    app: "App",
    cnrail_plugin: object,
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    """An ambiguous train with more than five candidates shows five and says so."""
    from nonebot_plugin_cnrail import __main__ as main
    from nonebot_plugin_cnrail.data_source import MultipleTrainFoundError

    freeze_clock(monkeypatch, main, "2024-12-15")
    worded: list[str] = []
    candidates = [f"G{index}" for index in range(1, 8)]

    async def query(train_code: str, train_date: str) -> Any:
        raise MultipleTrainFoundError(candidates)

    async def generate_word(*, train_code: str, train_date: str) -> str:
        worded.append(train_code)
        return f"{train_code} 摘要"

    patch_queries(monkeypatch, main, query)
    patch_render(monkeypatch, main, b"unused")
    monkeypatch.setattr(main, "generate_word", generate_word)

    payloads = await run_train_command(app, monkeypatch, f"{COMMAND} G1")

    assert worded == ["G1", "G2", "G3", "G4", "G5"]
    expected = (
        "查询到多个车次，请检查您的车次是否正确\n"
        "G1 摘要\nG2 摘要\nG3 摘要\nG4 摘要\nG5 摘要"
        "\n结果过多，仅显示前五个"
    )
    assert payloads == [expected]


async def test_train_command_reports_a_query_timeout(
    app: "App",
    cnrail_plugin: object,
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    """A timed out upstream query finishes with the timeout notice."""
    from httpx import TimeoutException
    from nonebot_plugin_cnrail import __main__ as main

    freeze_clock(monkeypatch, main, "2024-12-15")

    async def query(train_code: str, train_date: str) -> Any:
        raise TimeoutException("too slow")

    patch_queries(monkeypatch, main, query)
    patch_render(monkeypatch, main, b"unused")

    payloads = await run_train_command(app, monkeypatch, f"{COMMAND} G1")

    assert payloads == ["查询超时，请稍后重试"]


async def test_train_command_reports_an_unexpected_query_failure(
    app: "App",
    cnrail_plugin: object,
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    """An unexpected query error finishes with the generic error notice."""
    from nonebot_plugin_cnrail import __main__ as main

    freeze_clock(monkeypatch, main, "2024-12-15")

    async def query(train_code: str, train_date: str) -> Any:
        raise RuntimeError("boom")

    patch_queries(monkeypatch, main, query)
    patch_render(monkeypatch, main, b"unused")

    payloads = await run_train_command(app, monkeypatch, f"{COMMAND} G1")

    assert payloads == ["查询信息时出现错误，请检查后台输出"]


async def test_train_command_rejects_an_unparsable_date_argument(
    app: "App",
    cnrail_plugin: object,
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    """An invalid date argument finishes before any query is made."""
    from nonebot_plugin_cnrail import __main__ as main

    freeze_clock(monkeypatch, main, "2024-12-15")

    async def query(train_code: str, train_date: str) -> Any:
        return None

    queried = patch_queries(monkeypatch, main, query)
    patch_render(monkeypatch, main, b"unused")

    payloads = await run_train_command(app, monkeypatch, f"{COMMAND} G1 99-99")

    assert payloads == ["日期格式不正确"]
    assert queried == []


async def test_train_command_reports_a_render_failure(
    app: "App",
    cnrail_plugin: object,
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    """A rendering error finishes with the render error notice."""
    from nonebot_plugin_cnrail import __main__ as main

    freeze_clock(monkeypatch, main, "2024-12-15")

    async def query(train_code: str, train_date: str) -> Any:
        return cast("Any", object())

    async def render(*, data: Any, train_date: str) -> bytes:
        raise RuntimeError("no chromium")

    patch_queries(monkeypatch, main, query)
    monkeypatch.setattr(main, "render_train_info", render)

    payloads = await run_train_command(app, monkeypatch, f"{COMMAND} G1")

    assert payloads == ["渲染图片时出现错误，请检查后台输出"]
