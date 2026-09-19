"""Tests for the shared model configuration and the RailGo payload models."""

from typing import Any

import pytest
from nonebot.compat import model_dump
from pydantic import ValidationError

from tests_nbp_cnrail.utils.railgo_api import (
    coach_pic_payload,
    timetable_item,
    train_main_payload,
    v2_envelope,
)


def test_base_model_ignores_unknown_keys(cnrail_plugin: object) -> None:
    """The shared base model keeps pydantic's default of dropping unknown keys."""
    from nonebot_plugin_cnrail.models import CNRailBaseModel

    payload: dict[str, Any] = {"unknownKey": 1, "another": "x"}

    assert model_dump(CNRailBaseModel(**payload)) == {}


def test_timetable_item_parses_a_full_camel_case_payload(cnrail_plugin: object) -> None:
    """A camelCase timetable row populates every declared field."""
    from nonebot_plugin_cnrail.models import RailGoTimetableItem

    item = RailGoTimetableItem(**timetable_item(distance=1318, speed=305.5))

    assert item.arrive == "13:28"
    assert item.day == 0
    assert item.depart == "13:30"
    assert item.run_time == 268
    assert item.station == "上海虹桥"
    assert item.station_telecode == "AOH"
    assert item.stop_time == 2
    assert item.train_code == "G1"
    assert item.distance == 1318
    assert item.speed == 305.5


def test_timetable_item_accepts_snake_case_field_names(cnrail_plugin: object) -> None:
    """A row keyed by field names yields the same fields as the camelCase row."""
    from nonebot_plugin_cnrail.models import RailGoTimetableItem

    camel = RailGoTimetableItem(**timetable_item(distance=1318, speed=305.5))
    snake = RailGoTimetableItem(
        arrive="13:28",
        day=0,
        depart="13:30",
        run_time=268,
        station="上海虹桥",
        station_telecode="AOH",
        stop_time=2,
        train_code="G1",
        distance=1318,
        speed=305.5,
    )

    assert model_dump(snake) == model_dump(camel)


def test_timetable_item_ignores_unknown_and_misspelled_keys(
    cnrail_plugin: object,
) -> None:
    """Keys that are neither a field name nor a generated alias are dropped."""
    from nonebot_plugin_cnrail.models import RailGoTimetableItem

    item = RailGoTimetableItem(**timetable_item(stationName="北京南", bogusKey=1))

    assert item.station == "上海虹桥"


def test_timetable_item_defaults_timing_and_optional_measurements(
    cnrail_plugin: object,
) -> None:
    """A row without run time or measurements falls back to the declared defaults."""
    from nonebot_plugin_cnrail.models import RailGoTimetableItem

    payload: dict[str, Any] = {
        "arrive": "13:28",
        "day": 0,
        "depart": "13:30",
        "station": "上海虹桥",
        "stationTelecode": "AOH",
        "stopTime": 2,
        "trainCode": "G1",
    }
    item = RailGoTimetableItem(**payload)

    assert item.run_time == 0
    assert item.distance is None
    assert item.speed is None


def test_timetable_item_requires_stop_time(cnrail_plugin: object) -> None:
    """A row missing its stop time is rejected."""
    from nonebot_plugin_cnrail.models import RailGoTimetableItem

    payload: dict[str, Any] = {
        "arrive": "13:28",
        "day": 0,
        "depart": "13:30",
        "station": "上海虹桥",
        "stationTelecode": "AOH",
        "trainCode": "G1",
    }

    with pytest.raises(ValidationError):
        RailGoTimetableItem(**payload)


def test_train_main_data_parses_a_camel_case_payload_with_nested_timetable(
    cnrail_plugin: object,
) -> None:
    """The train payload maps its metadata and the nested camelCase timetable rows."""
    from nonebot_plugin_cnrail.models import RailGoTrainMainData

    data = RailGoTrainMainData(**train_main_payload())

    assert data.bureau == "京"
    assert data.bureau_short_name == "北京局"
    assert data.car == "CR400AF-2001"
    assert data.car_owner == "北京局"
    assert data.number_full == ["G1"]
    assert data.number_kind == "高速"
    assert data.rundays == ["20260919"]
    assert data.runner == "北京局"
    assert data.spend == 268
    assert data.timetable[0].station == "上海虹桥"
    assert data.timetable[0].run_time == 268


def test_train_main_data_accepts_snake_case_timetable_rows(
    cnrail_plugin: object,
) -> None:
    """Nested timetable rows also accept snake_case field names."""
    from nonebot_plugin_cnrail.models import RailGoTrainMainData

    data = RailGoTrainMainData(
        **train_main_payload(
            timetable=[
                {
                    "arrive": "13:28",
                    "day": 0,
                    "depart": "13:30",
                    "run_time": 268,
                    "station": "上海虹桥",
                    "station_telecode": "AOH",
                    "stop_time": 2,
                    "train_code": "G1",
                },
            ],
        ),
    )

    assert data.timetable[0].station_telecode == "AOH"
    assert data.timetable[0].stop_time == 2


def test_train_main_data_defaults_metadata_and_accepts_an_empty_timetable(
    cnrail_plugin: object,
) -> None:
    """Metadata fields carry empty defaults, and the timetable may be empty."""
    from nonebot_plugin_cnrail.models import RailGoTrainMainData

    data = RailGoTrainMainData(timetable=[])

    assert data.bureau == ""
    assert data.bureau_short_name == ""
    assert data.car == ""
    assert data.car_owner == ""
    assert data.number_full == []
    assert data.number_kind == ""
    assert data.rundays == []
    assert data.runner == ""
    assert data.spend == 0
    assert data.timetable == []


def test_train_main_data_requires_a_timetable(cnrail_plugin: object) -> None:
    """The timetable is required even when every metadata field is provided."""
    from nonebot_plugin_cnrail.models import RailGoTrainMainData

    payload: dict[str, Any] = {
        "bureau": "京",
        "bureauShortName": "北京局",
        "numberFull": ["G1"],
        "numberKind": "高速",
    }

    with pytest.raises(ValidationError):
        RailGoTrainMainData(**payload)


def test_coach_pic_data_parses_a_camel_case_payload(cnrail_plugin: object) -> None:
    """The coach picture payload maps its camelCase keys onto the fields."""
    from nonebot_plugin_cnrail.models import RailGoCoachPicData

    data = RailGoCoachPicData(**coach_pic_payload())

    assert data.car_code == "CR400AF-2001"
    assert data.car_type == "二等座"
    assert data.train_style == "复兴号"


def test_coach_pic_data_defaults_every_field_to_empty(cnrail_plugin: object) -> None:
    """An empty coach picture payload is valid and yields empty strings."""
    from nonebot_plugin_cnrail.models import RailGoCoachPicData

    data = RailGoCoachPicData()

    assert data.car_code == ""
    assert data.car_type == ""
    assert data.train_style == ""


def test_v2_response_keeps_an_object_payload_uncoerced(cnrail_plugin: object) -> None:
    """The envelope hands the raw API object through without converting it."""
    from nonebot_plugin_cnrail.models import RailGoV2Response

    payload = train_main_payload()
    response = RailGoV2Response(**v2_envelope(payload))

    assert type(response.data) is dict
    assert response.data == payload
    assert response.success is True
    assert response.msg == ""


def test_v2_response_allows_a_null_payload_and_reports_failure(
    cnrail_plugin: object,
) -> None:
    """A failed envelope carries a null payload together with its message."""
    from nonebot_plugin_cnrail.models import RailGoV2Response

    response = RailGoV2Response(
        **v2_envelope(None, success=False, msg="train not found"),
    )

    assert response.data is None
    assert response.success is False
    assert response.msg == "train not found"


def test_v2_response_requires_a_success_flag(cnrail_plugin: object) -> None:
    """An envelope without its success flag is rejected."""
    from nonebot_plugin_cnrail.models import RailGoV2Response

    payload: dict[str, Any] = {"data": None, "msg": "boom"}

    with pytest.raises(ValidationError):
        RailGoV2Response(**payload)
