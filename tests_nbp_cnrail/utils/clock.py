"""Pinning a plugin module's ``datetime.now`` for time-dependent tests."""

from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import tzinfo
    from types import ModuleType

    import pytest

# The instant the model tests pin their clock to, in Shanghai time.
FROZEN_INSTANT = "2026-09-19T20:00:00"


def freeze_clock(
    monkeypatch: "pytest.MonkeyPatch",
    module: "ModuleType",
    instant: str = FROZEN_INSTANT,
) -> None:
    """Pin ``module.datetime.now`` to ``instant`` read in the Shanghai timezone."""
    from nonebot_plugin_cnrail.utils import TZ_SHANGHAI

    frozen = TZ_SHANGHAI.localize(datetime.fromisoformat(instant))

    class _FrozenDatetime(datetime):
        @classmethod
        def now(cls, tz: "tzinfo | None" = None) -> datetime:
            return frozen if tz is None else frozen.astimezone(tz)

    monkeypatch.setattr(module, "datetime", _FrozenDatetime)
