"""Tests for the HTTP level query helpers of the RailGo data source."""

import httpx
import pytest

from tests_nbp_cnrail.utils.data_source_fixtures import TRAIN_DATE
from tests_nbp_cnrail.utils.railgo_api import (
    GET_COACH_PIC,
    GET_TRAIN_MAIN,
    TRAIN_PRESELECT,
    FakeRailGo,
    coach_pic_payload,
    train_main_payload,
    v2_envelope,
)


async def test_query_v2_data_returns_none_for_a_bad_request(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An HTTP 400 from RailGo means "no data" instead of raising."""
    from nonebot_plugin_cnrail import data_source
    from nonebot_plugin_cnrail.models import RailGoTrainMainData

    api = FakeRailGo().route(GET_TRAIN_MAIN, status=400).install(monkeypatch)

    async with data_source._make_client(data_source.RAILGO_V2_API_BASE) as client:
        result = await data_source._query_v2_data(
            client,
            GET_TRAIN_MAIN,
            {"trainNum": "G1"},
            RailGoTrainMainData,
        )

    assert result is None
    assert api.queries(GET_TRAIN_MAIN) == [{"trainNum": "G1"}]


async def test_query_v2_data_returns_none_when_the_envelope_fails(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An unsuccessful envelope is treated as missing data."""
    from nonebot_plugin_cnrail import data_source
    from nonebot_plugin_cnrail.models import RailGoTrainMainData

    FakeRailGo().route(
        GET_TRAIN_MAIN,
        json=v2_envelope(train_main_payload(), success=False, msg="boom"),
    ).install(monkeypatch)

    async with data_source._make_client(data_source.RAILGO_V2_API_BASE) as client:
        result = await data_source._query_v2_data(
            client,
            GET_TRAIN_MAIN,
            {"trainNum": "G1"},
            RailGoTrainMainData,
        )

    assert result is None


async def test_query_v2_data_returns_none_when_the_envelope_has_no_data(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A successful envelope without payload is treated as missing data."""
    from nonebot_plugin_cnrail import data_source
    from nonebot_plugin_cnrail.models import RailGoTrainMainData

    FakeRailGo().route(GET_TRAIN_MAIN, json=v2_envelope(None)).install(monkeypatch)

    async with data_source._make_client(data_source.RAILGO_V2_API_BASE) as client:
        result = await data_source._query_v2_data(
            client,
            GET_TRAIN_MAIN,
            {"trainNum": "G1"},
            RailGoTrainMainData,
        )

    assert result is None


async def test_query_v2_data_raises_for_server_errors(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Server side failures surface as ``HTTPStatusError``."""
    from nonebot_plugin_cnrail import data_source
    from nonebot_plugin_cnrail.models import RailGoTrainMainData

    FakeRailGo().route(GET_TRAIN_MAIN, status=500).install(monkeypatch)

    async with data_source._make_client(data_source.RAILGO_V2_API_BASE) as client:
        with pytest.raises(httpx.HTTPStatusError):
            await data_source._query_v2_data(
                client,
                GET_TRAIN_MAIN,
                {"trainNum": "G1"},
                RailGoTrainMainData,
            )


async def test_query_v2_data_validates_the_success_payload(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The envelope payload is validated into the requested model type."""
    from nonebot_plugin_cnrail import data_source
    from nonebot_plugin_cnrail.models import RailGoTrainMainData

    FakeRailGo().route(
        GET_TRAIN_MAIN,
        json=v2_envelope(train_main_payload(spend=42)),
    ).install(monkeypatch)

    async with data_source._make_client(data_source.RAILGO_V2_API_BASE) as client:
        result = await data_source._query_v2_data(
            client,
            GET_TRAIN_MAIN,
            {"trainNum": "G1"},
            RailGoTrainMainData,
        )

    assert isinstance(result, RailGoTrainMainData)
    assert result.spend == 42


async def test_query_train_main_skips_the_request_without_a_train_code(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An empty train code short circuits before any request is made."""
    from nonebot_plugin_cnrail import data_source

    api = FakeRailGo().install(monkeypatch)

    async with data_source._make_client(data_source.RAILGO_V2_API_BASE) as client:
        result = await data_source._query_train_main(client, "", TRAIN_DATE)

    assert result is None
    assert api.requests == []


async def test_query_train_main_sends_train_number_and_date(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The main timetable query asks ``getTrainMain`` for number and date."""
    from nonebot_plugin_cnrail import data_source

    api = (
        FakeRailGo()
        .route(GET_TRAIN_MAIN, json=v2_envelope(train_main_payload()))
        .install(monkeypatch)
    )

    async with data_source._make_client(data_source.RAILGO_V2_API_BASE) as client:
        result = await data_source._query_train_main(client, "G1", TRAIN_DATE)

    assert result is not None
    assert result.spend == 268
    assert api.queries(GET_TRAIN_MAIN) == [{"trainNum": "G1", "date": TRAIN_DATE}]


async def test_query_coach_pic_skips_the_request_without_a_train_code(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An empty train code short circuits the coach picture query."""
    from nonebot_plugin_cnrail import data_source

    api = FakeRailGo().install(monkeypatch)

    async with data_source._make_client(data_source.RAILGO_V2_API_BASE) as client:
        result = await data_source._query_coach_pic(client, "")

    assert result is None
    assert api.requests == []


async def test_query_coach_pic_sends_the_train_code(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The coach picture query asks ``getCoachPic`` for the train."""
    from nonebot_plugin_cnrail import data_source

    api = (
        FakeRailGo()
        .route(GET_COACH_PIC, json=v2_envelope(coach_pic_payload()))
        .install(monkeypatch)
    )

    async with data_source._make_client(data_source.RAILGO_V2_API_BASE) as client:
        result = await data_source._query_coach_pic(client, "G1")

    assert result is not None
    assert result.car_code == "CR400AF-2001"
    assert api.queries(GET_COACH_PIC) == [{"train": "G1"}]


async def test_query_train_candidates_returns_empty_list_for_unknown_keyword(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A 404 from the preselect endpoint means the keyword matches nothing."""
    from nonebot_plugin_cnrail import data_source

    api = FakeRailGo().route(TRAIN_PRESELECT, status=404).install(monkeypatch)

    assert await data_source._query_train_candidates("G1") == []
    assert api.queries(TRAIN_PRESELECT) == [{"keyword": "G1"}]


async def test_query_train_candidates_keeps_only_string_entries(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Non string entries of the preselect payload are dropped."""
    from nonebot_plugin_cnrail import data_source

    FakeRailGo().route(
        TRAIN_PRESELECT,
        json=["G1", 42, None, {"trainCode": "G2"}, "G3"],
    ).install(monkeypatch)

    assert await data_source._query_train_candidates("G1") == ["G1", "G3"]


async def test_query_train_candidates_returns_empty_list_for_non_list_payload(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A payload that is not a list yields no candidates."""
    from nonebot_plugin_cnrail import data_source

    FakeRailGo().route(TRAIN_PRESELECT, json={"data": ["G1"]}).install(monkeypatch)

    assert await data_source._query_train_candidates("G1") == []


async def test_query_train_candidates_normalizes_the_keyword(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The preselect keyword is trimmed and uppercased before being sent."""
    from nonebot_plugin_cnrail import data_source

    api = FakeRailGo().route(TRAIN_PRESELECT, json=[]).install(monkeypatch)

    assert await data_source._query_train_candidates("  g1  ") == []
    assert api.queries(TRAIN_PRESELECT) == [{"keyword": "G1"}]


async def test_query_train_candidates_raises_for_server_errors(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Server side failures of the preselect endpoint are not swallowed."""
    from nonebot_plugin_cnrail import data_source

    FakeRailGo().route(TRAIN_PRESELECT, status=500).install(monkeypatch)

    with pytest.raises(httpx.HTTPStatusError):
        await data_source._query_train_candidates("G1")
