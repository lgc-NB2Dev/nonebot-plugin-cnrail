"""Tests for the shared timezone and debug helpers."""

from datetime import datetime, timedelta

import pytest


def test_tz_shanghai_is_the_asia_shanghai_zone(cnrail_plugin: object) -> None:
    """The shared timezone is named Asia/Shanghai."""
    from nonebot_plugin_cnrail.utils import TZ_SHANGHAI

    assert TZ_SHANGHAI.zone == "Asia/Shanghai"


@pytest.mark.parametrize(
    "instant",
    ["2024-01-15T12:00:00", "2024-07-15T12:00:00"],
)
def test_tz_shanghai_stays_utc_plus_eight_all_year(
    cnrail_plugin: object,
    instant: str,
) -> None:
    """Shanghai has no DST anymore, so winter and summer both sit at UTC+8."""
    from nonebot_plugin_cnrail.utils import TZ_SHANGHAI

    localized = TZ_SHANGHAI.localize(datetime.fromisoformat(instant))

    assert localized.utcoffset() == timedelta(hours=8)


def test_debug_writer_is_disabled_by_default(cnrail_plugin: object) -> None:
    """The plugin ships a cookit debug writer that stays disabled by default."""
    from cookit import DebugFileWriter
    from nonebot_plugin_cnrail import utils

    assert isinstance(utils.debug, DebugFileWriter)
    assert utils.debug.enabled is False
