"""Tests for the ``TrainDetailData.arrived`` arrival-time calculation."""

from typing import TYPE_CHECKING

from tests_nbp_cnrail.utils.clock import freeze_clock
from tests_nbp_cnrail.utils.railgo_api import detail_data, via_station

if TYPE_CHECKING:
    import pytest


def test_arrived_is_true_for_an_arrival_before_the_frozen_now(
    cnrail_plugin: object,
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    """A station whose arrival already happened counts as arrived."""
    from nonebot_plugin_cnrail import models

    freeze_clock(monkeypatch, models)
    detail = detail_data(
        via_station(arrivalTime="08:00", departureTime="08:02"),
        via_station(stationName="北京南", arrivalTime="09:00"),
    )

    assert detail.arrived(1, "2026-09-19") is True


def test_arrived_is_false_for_an_arrival_after_the_frozen_now(
    cnrail_plugin: object,
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    """A station whose arrival is still ahead does not count as arrived."""
    from nonebot_plugin_cnrail import models

    freeze_clock(monkeypatch, models)
    detail = detail_data(via_station(arrivalTime="23:00", departureTime="23:02"))

    assert detail.arrived(0, "2026-09-19") is False


def test_arrived_shifts_the_arrival_across_days_by_the_day_index(
    cnrail_plugin: object,
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    """The day index shifts the arrival into the next day and flips the verdict."""
    from nonebot_plugin_cnrail import models

    freeze_clock(monkeypatch, models)
    detail = detail_data(
        via_station(arrivalTime="08:00", dayIndex=0),
        via_station(stationName="北京南", arrivalTime="08:00", dayIndex=1),
    )

    assert detail.arrived(0, "2026-09-19") is True
    assert detail.arrived(1, "2026-09-19") is False


def test_arrived_is_false_without_any_station_time(
    cnrail_plugin: object,
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    """A station with neither arrival nor departure time has not arrived."""
    from nonebot_plugin_cnrail import models

    freeze_clock(monkeypatch, models)
    detail = detail_data(via_station(arrivalTime=None, departureTime=None))

    assert detail.arrived(0, "2026-09-19") is False


def test_arrived_is_false_for_an_unparsable_arrival_time(
    cnrail_plugin: object,
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    """A station time that is not a valid time of day has not arrived."""
    from nonebot_plugin_cnrail import models

    freeze_clock(monkeypatch, models)
    detail = detail_data(via_station(arrivalTime="not-a-time", departureTime="08:00"))

    assert detail.arrived(0, "2026-09-19") is False


def test_arrived_falls_back_to_the_departure_time(
    cnrail_plugin: object,
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    """A station without an arrival time is judged by its departure time."""
    from nonebot_plugin_cnrail import models

    freeze_clock(monkeypatch, models)
    detail = detail_data(
        via_station(arrivalTime=None, departureTime="08:00"),
        via_station(stationName="北京南", arrivalTime=None, departureTime="23:00"),
    )

    assert detail.arrived(0, "2026-09-19") is True
    assert detail.arrived(1, "2026-09-19") is False
