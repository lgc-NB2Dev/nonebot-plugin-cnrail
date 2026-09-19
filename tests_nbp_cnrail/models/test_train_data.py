"""Tests for the CNRail train-search and serial-number models."""

from typing import Any

import pytest
from nonebot.compat import model_dump
from pydantic import ValidationError

from tests_nbp_cnrail.utils.railgo_api import search_payload


def test_search_data_populates_from_camel_case_aliases(cnrail_plugin: object) -> None:
    """A camelCase search result populates every declared field."""
    from nonebot_plugin_cnrail.models import TrainSearchData

    data = TrainSearchData(
        **search_payload(dayCount=2, distance=1318, crType=1, outOfDateFlag=1),
    )

    assert data.train_number == "G1"
    assert data.begin_station_name == "上海虹桥"
    assert data.departure_time == "08:00"
    assert data.end_station_name == "北京南"
    assert data.arrival_time == "12:28"
    assert data.duration_minutes == 268
    assert data.train_type == "高速"
    assert data.day_count == 2
    assert data.distance == 1318
    assert data.cr_type == 1
    assert data.out_of_date_flag == 1


def test_search_data_accepts_snake_case_field_names(cnrail_plugin: object) -> None:
    """A search result keyed by field names matches the camelCase one."""
    from nonebot_plugin_cnrail.models import TrainSearchData

    camel = TrainSearchData(**search_payload(dayCount=2, distance=1318))
    snake = TrainSearchData(
        train_number="G1",
        begin_station_name="上海虹桥",
        departure_time="08:00",
        end_station_name="北京南",
        arrival_time="12:28",
        duration_minutes=268,
        train_type="高速",
        day_count=2,
        distance=1318,
    )

    assert model_dump(snake) == model_dump(camel)
    assert snake.begin_station_name == "上海虹桥"
    assert snake.day_count == 2


def test_search_data_ignores_unknown_and_misspelled_keys(cnrail_plugin: object) -> None:
    """Keys that are neither a field name nor a generated alias are dropped."""
    from nonebot_plugin_cnrail.models import TrainSearchData

    data = TrainSearchData(**search_payload(TrainNumber="D1", bogusKey="x"))

    assert data.train_number == "G1"


def test_search_data_defaults_booking_metadata(cnrail_plugin: object) -> None:
    """Omitted booking fields fall back to their declared defaults."""
    from nonebot_plugin_cnrail.models import TrainSearchData

    data = TrainSearchData(**search_payload())

    assert data.day_count == 1
    assert data.distance == 0
    assert data.cr_type == 0
    assert data.out_of_date_flag == 0


def test_search_data_requires_a_train_number(cnrail_plugin: object) -> None:
    """A search result without a train number is rejected."""
    from nonebot_plugin_cnrail.models import TrainSearchData

    payload = search_payload()
    del payload["trainNumber"]

    with pytest.raises(ValidationError):
        TrainSearchData(**payload)


@pytest.mark.parametrize(
    ("duration_minutes", "expected"),
    [
        (0, "0 时 0 分"),
        (30, "0 时 30 分"),
        (268, "4 时 28 分"),
        (1440, "1 天 0 时 0 分"),
        (1500, "1 天 1 时 0 分"),
    ],
)
def test_search_data_pass_time_renders_days_hours_and_minutes(
    cnrail_plugin: object,
    duration_minutes: int,
    expected: str,
) -> None:
    """The duration renders as day/hour/minute text, omitting an empty day part."""
    from nonebot_plugin_cnrail.models import TrainSearchData

    data = TrainSearchData(**search_payload(durationMinutes=duration_minutes))

    assert data.pass_time == expected


def test_train_sn_data_accepts_camel_case_and_snake_case_keys(
    cnrail_plugin: object,
) -> None:
    """The serial-number model maps camelCase aliases and field names alike."""
    from nonebot_plugin_cnrail.models import TrainSNData

    payload: dict[str, Any] = {
        "emuSerialNumber": "CR400AF-2001",
        "date": "2026-09-19",
        "trainNumber": "G1",
    }
    camel = TrainSNData(**payload)
    snake = TrainSNData(
        emu_serial_number="CR400AF-2001",
        date="2026-09-19",
        train_number="G1",
    )

    assert model_dump(snake) == model_dump(camel)
    assert camel.emu_serial_number == "CR400AF-2001"


def test_train_sn_data_requires_a_train_number(cnrail_plugin: object) -> None:
    """A serial-number entry without its train number is rejected."""
    from nonebot_plugin_cnrail.models import TrainSNData

    payload: dict[str, Any] = {
        "emuSerialNumber": "CR400AF-2001",
        "date": "2026-09-19",
    }

    with pytest.raises(ValidationError):
        TrainSNData(**payload)
