"""Tests for the CNRail via-station, routing and train-detail models."""

from typing import Any

import pytest
from nonebot.compat import model_dump
from pydantic import ValidationError

from tests_nbp_cnrail.utils.railgo_api import detail_data, via_station


def test_detail_via_station_parses_a_full_camel_case_payload(
    cnrail_plugin: object,
) -> None:
    """Every declared via-station field maps from its camelCase alias."""
    from nonebot_plugin_cnrail.models import TrainDetailViaStation

    station = TrainDetailViaStation(
        **via_station(
            stationTelegramCode="AOH",
            arrivalTime="13:28",
            departureTime="13:30",
            distance=1318,
            checkoutName="上海虹桥",
            speed=305.5,
            companyName="上海局",
            province="上海",
            district="闵行",
            outOfDateFlag=1,
            isTurn=True,
        ),
    )

    assert station.station_name == "上海虹桥"
    assert station.train_number == "G1"
    assert station.stop_minutes == 2
    assert station.day_index == 0
    assert station.station_telegram_code == "AOH"
    assert station.arrival_time == "13:28"
    assert station.departure_time == "13:30"
    assert station.distance == 1318
    assert station.checkout_name == "上海虹桥"
    assert station.speed == 305.5
    assert station.company_name == "上海局"
    assert station.province == "上海"
    assert station.district == "闵行"
    assert station.out_of_date_flag == 1
    assert station.is_turn is True


def test_detail_via_station_accepts_snake_case_field_names(
    cnrail_plugin: object,
) -> None:
    """A station keyed by field names matches the camelCase one."""
    from nonebot_plugin_cnrail.models import TrainDetailViaStation

    camel = TrainDetailViaStation(
        **via_station(dayIndex=1, stationTelegramCode="AOH", speed=305.5),
    )
    snake = TrainDetailViaStation(
        station_name="上海虹桥",
        train_number="G1",
        stop_minutes=2,
        day_index=1,
        station_telegram_code="AOH",
        speed=305.5,
    )

    assert model_dump(snake) == model_dump(camel)
    assert snake.day_index == 1


def test_detail_via_station_defaults_optional_fields(cnrail_plugin: object) -> None:
    """A station without optional data keeps every declared default."""
    from nonebot_plugin_cnrail.models import TrainDetailViaStation

    station = TrainDetailViaStation(**via_station())

    assert station.station_telegram_code is None
    assert station.arrival_time is None
    assert station.departure_time is None
    assert station.distance == 0
    assert station.checkout_name is None
    assert station.speed is None
    assert station.company_name == ""
    assert station.province == ""
    assert station.district == ""
    assert station.out_of_date_flag == 0
    assert station.is_turn is False


def test_detail_via_station_requires_a_day_index(cnrail_plugin: object) -> None:
    """A station without its day index is rejected."""
    from nonebot_plugin_cnrail.models import TrainDetailViaStation

    payload: dict[str, Any] = {
        "stationName": "上海虹桥",
        "trainNumber": "G1",
        "stopMinutes": 2,
    }

    with pytest.raises(ValidationError):
        TrainDetailViaStation(**payload)


def test_detail_routing_item_accepts_camel_case_and_snake_case_keys(
    cnrail_plugin: object,
) -> None:
    """A routing leg maps from camelCase aliases and from field names alike."""
    from nonebot_plugin_cnrail.models import TrainDetailRoutingItem

    camel_payload: dict[str, Any] = {
        "trainNumber": "G1",
        "beginStationName": "上海虹桥",
        "departureTime": "08:00",
        "endStationName": "北京南",
        "arrivalTime": "12:28",
    }
    camel = TrainDetailRoutingItem(**camel_payload)
    snake = TrainDetailRoutingItem(
        train_number="G1",
        begin_station_name="上海虹桥",
        departure_time="08:00",
        end_station_name="北京南",
        arrival_time="12:28",
    )

    assert model_dump(snake) == model_dump(camel)
    assert camel.begin_station_name == "上海虹桥"
    assert camel.arrival_time == "12:28"


def test_detail_routing_item_requires_an_arrival_time(cnrail_plugin: object) -> None:
    """A routing leg without its arrival time is rejected."""
    from nonebot_plugin_cnrail.models import TrainDetailRoutingItem

    payload: dict[str, Any] = {
        "trainNumber": "G1",
        "beginStationName": "上海虹桥",
        "departureTime": "08:00",
        "endStationName": "北京南",
    }

    with pytest.raises(ValidationError):
        TrainDetailRoutingItem(**payload)


def test_detail_routing_parses_nested_camel_case_items(cnrail_plugin: object) -> None:
    """The routing section maps its nested legs and the train model."""
    from nonebot_plugin_cnrail.models import TrainDetailRouting

    payload: dict[str, Any] = {
        "routingItems": [
            {
                "trainNumber": "G1",
                "beginStationName": "上海虹桥",
                "departureTime": "08:00",
                "endStationName": "北京南",
                "arrivalTime": "12:28",
            },
        ],
        "trainModel": "CR400AF",
    }
    routing = TrainDetailRouting(**payload)

    assert routing.train_model == "CR400AF"
    assert routing.routing_items[0].train_number == "G1"
    assert routing.routing_items[0].end_station_name == "北京南"


def test_detail_routing_defaults_to_no_legs(cnrail_plugin: object) -> None:
    """A routing section without legs is valid and yields an empty list."""
    from nonebot_plugin_cnrail.models import TrainDetailRouting

    payload: dict[str, Any] = {"trainModel": "CR400AF"}

    assert TrainDetailRouting(**payload).routing_items == []


def test_detail_routing_requires_a_train_model(cnrail_plugin: object) -> None:
    """A routing section without its train model is rejected."""
    from nonebot_plugin_cnrail.models import TrainDetailRouting

    payload: dict[str, Any] = {"routingItems": []}

    with pytest.raises(ValidationError):
        TrainDetailRouting(**payload)


def test_train_detail_data_parses_a_full_camel_case_payload(
    cnrail_plugin: object,
) -> None:
    """The detail payload maps identity fields plus nested stations and routing."""
    from nonebot_plugin_cnrail.models import TrainDetailData

    payload: dict[str, Any] = {
        "trainNumber": "G1",
        "trainType": "高速",
        "companyName": "上海局",
        "foodCoachName": "9",
        "crType": 1,
        "viaStations": [
            via_station(),
            via_station(stationName="北京南", dayIndex=1, distance=1318),
        ],
        "routing": {"routingItems": [], "trainModel": "CR400AF"},
    }
    detail = TrainDetailData(**payload)

    assert detail.train_number == "G1"
    assert detail.train_type == "高速"
    assert detail.company_name == "上海局"
    assert detail.food_coach_name == "9"
    assert detail.cr_type == 1
    assert detail.via_stations[1].station_name == "北京南"
    assert detail.via_stations[1].day_index == 1
    assert detail.via_stations[1].distance == 1318
    assert detail.routing.train_model == "CR400AF"
    assert detail.routing.routing_items == []


def test_train_detail_data_defaults_food_coach_and_cr_type(
    cnrail_plugin: object,
) -> None:
    """Detail data without the optional coach fields keeps their defaults."""

    detail = detail_data(via_station())

    assert detail.food_coach_name is None
    assert detail.cr_type == 0


def test_train_detail_data_requires_via_stations(cnrail_plugin: object) -> None:
    """Detail data without any via station is rejected."""
    from nonebot_plugin_cnrail.models import TrainDetailData

    payload: dict[str, Any] = {
        "trainNumber": "G1",
        "trainType": "高速",
        "companyName": "上海局",
        "routing": {"trainModel": "CR400AF"},
    }

    with pytest.raises(ValidationError):
        TrainDetailData(**payload)
