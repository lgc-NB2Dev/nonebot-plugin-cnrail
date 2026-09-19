"""Tests for the plugin entry module."""

import re

HOMEPAGE = "https://github.com/lgc-NB2Dev/nonebot-plugin-cnrail"
VERSION_PATTERN = r"\d+\.\d+\.\d+(?:[.\-+][0-9A-Za-z.]+)?"


def test_plugin_metadata_declares_the_command_contract(cnrail_plugin: object) -> None:
    """The plugin advertises its name, usage, homepage and configuration model."""
    from nonebot_plugin_cnrail import __plugin_meta__
    from nonebot_plugin_cnrail.config import ConfigModel

    assert __plugin_meta__.name == "CNRail"
    assert __plugin_meta__.description == "查询 12306 列车时刻表"
    assert __plugin_meta__.usage == "使用指令 train -h 查看帮助"
    assert __plugin_meta__.homepage == HOMEPAGE
    assert __plugin_meta__.type == "application"
    assert __plugin_meta__.config is ConfigModel
    assert __plugin_meta__.supported_adapters


def test_plugin_version_looks_like_a_release(cnrail_plugin: object) -> None:
    """The package exposes a non-empty PEP 440 style release version."""
    from nonebot_plugin_cnrail import __version__

    assert __version__
    assert re.fullmatch(VERSION_PATTERN, __version__) is not None


def test_loading_the_plugin_also_loads_its_requirements(cnrail_plugin: object) -> None:
    """The plugin's alconna and htmlrender requirements are available once loaded."""
    import nonebot

    assert nonebot.get_plugin("nonebot_plugin_alconna") is not None
    assert nonebot.get_plugin("nonebot_plugin_htmlrender") is not None
