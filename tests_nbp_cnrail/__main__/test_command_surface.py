"""Tests for how the `train` command is registered and triggered."""

from typing import TYPE_CHECKING, Any

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


async def test_train_command_reaches_the_query_flow_through_aliases(
    app: "App",
    cnrail_plugin: object,
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    """Both aliases trigger the same query flow as the command itself."""
    from nonebot_plugin_cnrail import __main__ as main

    freeze_clock(monkeypatch, main, "2024-12-15")

    async def query(train_code: str, train_date: str) -> Any:
        return None

    queried = patch_queries(monkeypatch, main, query)
    patch_render(monkeypatch, main, b"unused")

    triggers = ("/列车信息 G1", "/查询列车 G1", f"{COMMAND} G1")
    for trigger in triggers:
        payloads = await run_train_command(app, monkeypatch, trigger)
        assert payloads == [MISSING_TRAIN_TEXT]

    assert queried == [("G1", TODAY)] * len(triggers)


async def test_train_command_ignores_input_without_the_command_start_prefix(
    app: "App",
    cnrail_plugin: object,
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    """Bare command text is not answered because the command-start prefix is required."""
    from nonebot_plugin_cnrail import __main__ as main

    async def query(train_code: str, train_date: str) -> Any:
        return None

    queried = patch_queries(monkeypatch, main, query)
    patch_render(monkeypatch, main, b"unused")

    for text in ("hello world", "train G1", "列车信息 G1"):
        assert await run_train_command(app, monkeypatch, text) == []

    assert queried == []


def test_train_command_registers_its_configuration(cnrail_plugin: object) -> None:
    """The command exposes its name, aliases, metadata and command-start prefix."""
    from arclet.alconna import command_manager
    from nonebot import get_driver
    from nonebot_plugin_cnrail import __main__ as main

    command = main.search_train_info.command()

    assert command.name == "train"
    assert command.path == "Alconna::train"
    assert command_manager.get_command(command.path) is not None
    assert command.prefixes
    assert command.prefixes == list(get_driver().config.command_start)

    shortcuts = " ".join(str(shortcut) for shortcut in command.get_shortcuts())
    assert "列车信息" in shortcuts
    assert "查询列车" in shortcuts

    assert command.meta.description == "查询列车信息"
    assert command.meta.usage == "train <车次> [日期（可选，只包含月和日）]"
    assert command.meta.example == "train G1 12-10"
