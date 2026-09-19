"""Shared helpers for the `train` command matcher tests."""

from typing import TYPE_CHECKING, Any

from tests_nbp_cnrail.utils.events import make_event

if TYPE_CHECKING:
    import pytest
    from nonebug import App

# The `train` command as it is triggered under the default command start.
COMMAND = "/train"
# The date the matcher tests pin the module clock to.
TODAY = "2024-12-15"
# The plugin's answer when the requested train cannot be found.
MISSING_TRAIN_TEXT = "未查询到车次，可能是当日未开行，请检查您的车次是否正确"


def patch_queries(
    monkeypatch: "pytest.MonkeyPatch",
    main: Any,
    query: Any,
) -> list[tuple[str, str]]:
    """Replace the networked `query_train_info` and record its `(code, date)` calls."""
    queried: list[tuple[str, str]] = []

    async def fake_query_train_info(train_code: str, train_date: str) -> Any:
        queried.append((train_code, train_date))
        return await query(train_code, train_date)

    monkeypatch.setattr(main, "query_train_info", fake_query_train_info)
    return queried


def patch_render(
    monkeypatch: "pytest.MonkeyPatch",
    main: Any,
    image_bytes: bytes | None,
) -> list[tuple[Any, str]]:
    """Replace the browser-backed `render_train_info` and record its calls."""
    rendered: list[tuple[Any, str]] = []

    async def fake_render_train_info(*, data: Any, train_date: str) -> bytes | None:
        rendered.append((data, train_date))
        return image_bytes

    monkeypatch.setattr(main, "render_train_info", fake_render_train_info)
    return rendered


def record_finishes(monkeypatch: "pytest.MonkeyPatch") -> list[Any]:
    """Capture every matcher `finish` payload and abort the handler."""
    from nonebot.exception import FinishedException
    from nonebot_plugin_alconna import AlconnaMatcher

    payloads: list[Any] = []

    @classmethod
    async def fake_finish(cls: Any, message: Any = None, **kwargs: Any) -> None:
        payloads.append(message)
        raise FinishedException

    monkeypatch.setattr(AlconnaMatcher, "finish", fake_finish)
    return payloads


async def run_train_command(
    app: "App",
    monkeypatch: "pytest.MonkeyPatch",
    text: str,
) -> list[Any]:
    """Feed one message to the `train` matcher and return its finishes."""
    from nonebot_plugin_cnrail import __main__ as main

    payloads = record_finishes(monkeypatch)
    async with app.test_matcher(main.search_train_info) as ctx:
        ctx.receive_event(ctx.create_bot(), make_event(text))
    return payloads
