"""Tests for the `train` command help and argument-error branches."""

from typing import TYPE_CHECKING

from tests_nbp_cnrail.utils.command_fixtures import COMMAND, run_train_command

if TYPE_CHECKING:
    import pytest
    from nonebug import App


async def test_train_command_finishes_with_the_help_output(
    app: "App",
    cnrail_plugin: object,
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    """The `-h` option is answered by the matcher with the alconna help text."""
    payloads = await run_train_command(app, monkeypatch, f"{COMMAND} -h")

    assert len(payloads) == 1
    assert isinstance(payloads[0], str)
    assert "train <车次> [日期（可选，只包含月和日）]" in payloads[0]
    assert "train G1 12-10" in payloads[0]


async def test_train_command_finishes_with_the_parse_error_and_a_help_hint(
    app: "App",
    cnrail_plugin: object,
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    """A bare command without its train argument is answered with an error and a hint."""
    payloads = await run_train_command(app, monkeypatch, COMMAND)

    assert len(payloads) == 1
    assert isinstance(payloads[0], str)
    assert payloads[0].endswith("使用指令 `train -h` 查看帮助")
