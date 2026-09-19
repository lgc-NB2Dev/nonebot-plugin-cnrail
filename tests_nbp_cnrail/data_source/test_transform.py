"""Tests for the pure helpers of the RailGo data source."""

from typing import Any

import httpx
import pytest

from tests_nbp_cnrail.utils.data_source_fixtures import (
    TRAIN_DATE,
    TWO_STATION_TIMETABLE,
    main_data,
)
from tests_nbp_cnrail.utils.railgo_api import timetable_item


def test_normalize_train_code_strips_uppercases_and_cuts_at_slash(
    cnrail_plugin: object,
) -> None:
    """Train codes are trimmed, uppercased and truncated at the first slash."""
    from nonebot_plugin_cnrail.data_source import _normalize_train_code

    assert _normalize_train_code("  g1  ") == "G1"
    assert _normalize_train_code("g1/g2") == "G1"
    assert _normalize_train_code("") == ""


def test_candidate_parts_uppercases_and_drops_empty_parts(
    cnrail_plugin: object,
) -> None:
    """Slash separated candidates are split, trimmed and deduplicated."""
    from nonebot_plugin_cnrail.data_source import _candidate_parts

    assert _candidate_parts("g1/G2") == {"G1", "G2"}
    assert _candidate_parts(" g1 // g2 ") == {"G1", "G2"}
    assert _candidate_parts("") == set()


async def test_make_client_targets_the_given_base_url_with_shared_defaults(
    cnrail_plugin: object,
) -> None:
    """Clients follow redirects and use the module timeout for the requested API host."""
    from nonebot_plugin_cnrail import data_source

    client = data_source._make_client(data_source.RAILGO_V1_API_BASE)

    try:
        assert isinstance(client, httpx.AsyncClient)
        assert str(client.base_url) == data_source.RAILGO_V1_API_BASE
        assert client.timeout == httpx.Timeout(data_source.REQUEST_TIMEOUT)
        assert client.follow_redirects is True
    finally:
        await client.aclose()


def test_display_train_number_prefers_the_full_number_list(
    cnrail_plugin: object,
) -> None:
    """A populated ``numberFull`` is joined with slashes, ignoring the timetable code."""
    from nonebot_plugin_cnrail.data_source import _display_train_number

    data = main_data(
        numberFull=["G1", "G2"],
        timetable=[timetable_item(trainCode="G9")],
    )

    assert _display_train_number(data) == "G1/G2"


def test_display_train_number_falls_back_to_the_first_timetable_code(
    cnrail_plugin: object,
) -> None:
    """An empty ``numberFull`` makes the first timetable entry name the train."""
    from nonebot_plugin_cnrail.data_source import _display_train_number

    data = main_data(numberFull=[], timetable=[timetable_item(trainCode="G9")])

    assert _display_train_number(data) == "G9"


@pytest.mark.parametrize(
    ("timetable", "expected"),
    [
        ([], 0),
        ([timetable_item(distance=None)], 0),
        ([timetable_item(distance=None), timetable_item(distance=500)], 500),
    ],
)
def test_last_distance_treats_missing_distances_as_zero(
    cnrail_plugin: object,
    timetable: list[dict[str, Any]],
    expected: int,
) -> None:
    """The reported distance is the largest timetable distance, empty ones counting zero."""
    from nonebot_plugin_cnrail.data_source import _last_distance

    assert _last_distance(main_data(timetable=timetable)) == expected


def test_to_search_data_prefers_spend_and_uses_endpoint_stations(
    cnrail_plugin: object,
) -> None:
    """Search data spans the first and last station and takes its duration from ``spend``."""
    from nonebot_plugin_cnrail.data_source import _to_search_data

    search = _to_search_data(
        main_data(timetable=TWO_STATION_TIMETABLE, spend=280, numberKind="高速"),
    )

    assert search.train_number == "G1"
    assert search.begin_station_name == "上海虹桥"
    assert search.departure_time == "13:30"
    assert search.end_station_name == "北京南"
    assert search.arrival_time == "18:58"
    assert search.duration_minutes == 280
    assert search.train_type == "高速"
    assert search.day_count == 2
    assert search.distance == 1318


def test_to_search_data_falls_back_to_the_last_run_time_without_spend(
    cnrail_plugin: object,
) -> None:
    """A missing ``spend`` leaves the last station's run time as the duration."""
    from nonebot_plugin_cnrail.data_source import _to_search_data

    search = _to_search_data(
        main_data(timetable=[timetable_item(day=0, runTime=95)], spend=0),
    )

    assert search.duration_minutes == 95
    assert search.day_count == 1


def test_to_detail_data_prefers_bureau_short_name_as_company(
    cnrail_plugin: object,
) -> None:
    """Detail stations carry the bureau short name, distances and speeds of their row."""
    from nonebot_plugin_cnrail.data_source import _to_detail_data

    detail = _to_detail_data(main_data(timetable=TWO_STATION_TIMETABLE))

    assert detail.train_number == "G1"
    assert detail.train_type == "高速"
    assert detail.company_name == "北京局"
    assert detail.routing.train_model == "CR400AF-2001"
    assert detail.routing.routing_items == []
    assert [station.station_name for station in detail.via_stations] == [
        "上海虹桥",
        "北京南",
    ]

    first, last = detail.via_stations
    assert first.company_name == "北京局"
    assert first.station_telegram_code == "AOH"
    assert first.train_number == "G1"
    assert first.arrival_time == "13:20"
    assert first.departure_time == "13:30"
    assert first.stop_minutes == 2
    assert first.distance == 100
    assert first.speed is None
    assert first.day_index == 0
    assert last.stop_minutes == 5
    assert last.distance == 1318
    assert last.speed == 305.5
    assert last.day_index == 1


def test_to_detail_data_falls_back_to_the_bureau_when_short_name_is_empty(
    cnrail_plugin: object,
) -> None:
    """An empty bureau short name makes the plain bureau name the company."""
    from nonebot_plugin_cnrail.data_source import _to_detail_data

    detail = _to_detail_data(
        main_data(
            bureau="哈尔滨局",
            bureauShortName="",
            timetable=TWO_STATION_TIMETABLE,
        ),
    )

    assert detail.company_name == "哈尔滨局"
    assert {station.company_name for station in detail.via_stations} == {"哈尔滨局"}


def test_to_detail_data_defaults_a_missing_distance_to_zero(
    cnrail_plugin: object,
) -> None:
    """A station without distance is reported as zero rather than null."""
    from nonebot_plugin_cnrail.data_source import _to_detail_data

    detail = _to_detail_data(main_data(timetable=[timetable_item(distance=None)]))

    assert detail.via_stations[0].distance == 0


def test_to_detail_data_of_an_empty_timetable_has_no_stations(
    cnrail_plugin: object,
) -> None:
    """A train without timetable still yields a detail shell naming it."""
    from nonebot_plugin_cnrail.data_source import _to_detail_data

    detail = _to_detail_data(main_data(numberFull=["G1"], timetable=[]))

    assert detail.via_stations == []
    assert detail.routing.routing_items == []
    assert detail.routing.train_model == "CR400AF-2001"
    assert detail.train_number == "G1"


def test_to_train_info_returns_none_for_an_empty_timetable(
    cnrail_plugin: object,
) -> None:
    """A train without timetable cannot produce a ``TrainInfo``."""
    from nonebot_plugin_cnrail.data_source import _to_train_info

    assert _to_train_info(main_data(timetable=[]), None, TRAIN_DATE) is None


def test_to_train_info_carries_search_detail_sn_and_date(
    cnrail_plugin: object,
) -> None:
    """The assembled info exposes the search summary, detail, serial numbers and date."""
    from nonebot_plugin_cnrail.data_source import _to_train_info
    from nonebot_plugin_cnrail.models import TrainSNData

    sn = [
        TrainSNData(
            emu_serial_number="CR400AF-2001",
            date=TRAIN_DATE,
            train_number="G1",
        ),
    ]

    info = _to_train_info(main_data(timetable=TWO_STATION_TIMETABLE), sn, TRAIN_DATE)

    assert info is not None
    assert info.search.distance == 1318
    assert info.detail.routing.train_model == "CR400AF-2001"
    assert info.sn == sn
    assert info.train_date == TRAIN_DATE
