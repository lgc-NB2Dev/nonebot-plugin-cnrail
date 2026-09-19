"""Canned timetables and model instances for the data source tests."""

from typing import Any

from nonebot.compat import type_validate_python

from tests_nbp_cnrail.utils.railgo_api import timetable_item, train_main_payload

TRAIN_DATE = "2026-09-19"

TWO_STATION_TIMETABLE = [
    timetable_item(
        arrive="13:20",
        depart="13:30",
        distance=100,
        runTime=40,
        station="上海虹桥",
        stationTelecode="AOH",
        stopTime=2,
        trainCode="G1",
    ),
    timetable_item(
        arrive="18:58",
        day=1,
        depart="19:00",
        distance=1318,
        runTime=300,
        speed=305.5,
        station="北京南",
        stationTelecode="VNP",
        stopTime=5,
        trainCode="G1",
    ),
]

G2_TIMETABLE = [
    timetable_item(station="上海虹桥", trainCode="G2"),
    timetable_item(day=1, runTime=250, station="北京南", trainCode="G2"),
]


def main_data(**overrides: Any) -> Any:
    """Build a validated ``RailGoTrainMainData`` from canned camelCase fields."""
    from nonebot_plugin_cnrail.models import RailGoTrainMainData

    return type_validate_python(RailGoTrainMainData, train_main_payload(**overrides))
