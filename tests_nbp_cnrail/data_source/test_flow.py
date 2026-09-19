"""Tests for the high level data source flows."""

import pytest

from tests_nbp_cnrail.utils.data_source_fixtures import (
    G2_TIMETABLE,
    TRAIN_DATE,
    TWO_STATION_TIMETABLE,
)
from tests_nbp_cnrail.utils.railgo_api import (
    GET_COACH_PIC,
    GET_TRAIN_MAIN,
    TRAIN_PRESELECT,
    FakeRailGo,
    QueuedRailGo,
    coach_pic_payload,
    train_main_payload,
    v2_envelope,
)


async def test_get_train_sn_returns_one_record_from_the_coach_pic(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A coach picture with a serial number becomes a single serial number record."""
    from nonebot_plugin_cnrail import data_source

    api = (
        FakeRailGo()
        .route(GET_COACH_PIC, json=v2_envelope(coach_pic_payload()))
        .install(monkeypatch)
    )

    result = await data_source.get_train_sn("G1", TRAIN_DATE)

    assert result is not None
    assert len(result) == 1
    assert result[0].emu_serial_number == "CR400AF-2001"
    assert result[0].date == TRAIN_DATE
    assert result[0].train_number == "G1"
    assert api.queries(GET_COACH_PIC) == [{"train": "G1"}]


async def test_get_train_sn_normalizes_the_train_code_before_querying(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A loosely formatted train code is normalized for the coach picture query."""
    from nonebot_plugin_cnrail import data_source

    api = (
        FakeRailGo()
        .route(GET_COACH_PIC, json=v2_envelope(coach_pic_payload()))
        .install(monkeypatch)
    )

    result = await data_source.get_train_sn("  g1  ", TRAIN_DATE)

    assert result is not None
    assert api.queries(GET_COACH_PIC) == [{"train": "G1"}]


async def test_get_train_sn_returns_none_without_a_car_code(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A coach picture without serial number yields no records."""
    from nonebot_plugin_cnrail import data_source

    FakeRailGo().route(
        GET_COACH_PIC,
        json=v2_envelope(coach_pic_payload(car_code="")),
    ).install(monkeypatch)

    assert await data_source.get_train_sn("G1", TRAIN_DATE) is None


async def test_get_train_sn_returns_none_when_the_coach_pic_is_missing(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A coach picture RailGo does not have yields no serial number."""
    from nonebot_plugin_cnrail import data_source

    FakeRailGo().route(GET_COACH_PIC, status=400).install(monkeypatch)

    assert await data_source.get_train_sn("G1", TRAIN_DATE) is None


async def test_get_train_sn_returns_none_when_the_request_fails(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Request failures are swallowed into a missing serial number."""
    from nonebot_plugin_cnrail import data_source

    FakeRailGo().route(GET_COACH_PIC, status=500).install(monkeypatch)

    assert await data_source.get_train_sn("G1", TRAIN_DATE) is None


async def test_get_train_sn_returns_none_when_the_payload_is_invalid(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Payloads that do not validate are swallowed into a missing serial number."""
    from nonebot_plugin_cnrail import data_source

    FakeRailGo().route(
        GET_COACH_PIC,
        json=v2_envelope("not a coach picture"),
    ).install(monkeypatch)

    assert await data_source.get_train_sn("G1", TRAIN_DATE) is None


async def test_generate_word_reports_a_train_without_data(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A train RailGo does not know is reported as not running that day."""
    from nonebot_plugin_cnrail import data_source

    FakeRailGo().route(GET_TRAIN_MAIN, status=400).install(monkeypatch)

    assert await data_source.generate_word("G1", TRAIN_DATE) == "G1 | 当日未开行"


async def test_generate_word_reports_a_train_without_timetable(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A train with an empty timetable is reported as not running that day."""
    from nonebot_plugin_cnrail import data_source

    FakeRailGo().route(
        GET_TRAIN_MAIN,
        json=v2_envelope(train_main_payload(timetable=[])),
    ).install(monkeypatch)

    assert await data_source.generate_word("G1", TRAIN_DATE) == "G1 | 当日未开行"


async def test_generate_word_summarizes_the_route_of_the_normalized_code(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A running train is summarized by number, endpoints and duration."""
    from nonebot_plugin_cnrail import data_source

    api = (
        FakeRailGo()
        .route(
            GET_TRAIN_MAIN,
            json=v2_envelope(train_main_payload(timetable=TWO_STATION_TIMETABLE)),
        )
        .install(monkeypatch)
    )

    result = await data_source.generate_word("  g1  ", TRAIN_DATE)

    assert result == "G1 | 上海虹桥 - 北京南 | 耗时 268 分钟"
    assert api.queries(GET_TRAIN_MAIN) == [{"trainNum": "G1", "date": TRAIN_DATE}]


async def test_query_train_info_returns_full_info_and_queries_the_coach_pic(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A directly resolvable train yields full info plus its serial number."""
    from nonebot_plugin_cnrail import data_source

    api = (
        FakeRailGo()
        .route(
            GET_TRAIN_MAIN,
            json=v2_envelope(train_main_payload(timetable=TWO_STATION_TIMETABLE)),
        )
        .route(GET_COACH_PIC, json=v2_envelope(coach_pic_payload()))
        .install(monkeypatch)
    )

    info = await data_source.query_train_info("  g1  ", TRAIN_DATE)

    assert isinstance(info, data_source.TrainInfo)
    assert info.train_date == TRAIN_DATE
    assert info.search.train_number == "G1"
    assert info.search.duration_minutes == 268
    assert info.detail.company_name == "北京局"
    assert info.sn is not None
    assert info.sn[0].emu_serial_number == "CR400AF-2001"
    assert info.sn[0].date == TRAIN_DATE
    assert info.sn[0].train_number == "G1"
    assert api.queries(GET_TRAIN_MAIN) == [{"trainNum": "G1", "date": TRAIN_DATE}]
    assert api.queries(GET_COACH_PIC) == [{"train": "G1"}]
    assert api.queries(TRAIN_PRESELECT) == []


async def test_query_train_info_leaves_sn_empty_without_a_car_code(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A train whose coach picture has no serial number yields info without it."""
    from nonebot_plugin_cnrail import data_source

    FakeRailGo().route(
        GET_TRAIN_MAIN,
        json=v2_envelope(train_main_payload(timetable=TWO_STATION_TIMETABLE)),
    ).route(
        GET_COACH_PIC,
        json=v2_envelope(coach_pic_payload(car_code="")),
    ).install(monkeypatch)

    info = await data_source.query_train_info("G1", TRAIN_DATE)

    assert info is not None
    assert info.sn is None


async def test_query_train_info_leaves_sn_empty_when_the_coach_pic_is_missing(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A train RailGo has no coach picture for still yields info without serial number."""
    from nonebot_plugin_cnrail import data_source

    FakeRailGo().route(
        GET_TRAIN_MAIN,
        json=v2_envelope(train_main_payload(timetable=TWO_STATION_TIMETABLE)),
    ).route(GET_COACH_PIC, status=400).install(monkeypatch)

    info = await data_source.query_train_info("G1", TRAIN_DATE)

    assert info is not None
    assert info.sn is None


async def test_query_train_info_returns_none_for_a_train_without_timetable(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A known train without timetable cannot be rendered into info."""
    from nonebot_plugin_cnrail import data_source

    FakeRailGo().route(
        GET_TRAIN_MAIN,
        json=v2_envelope(train_main_payload(timetable=[])),
    ).route(GET_COACH_PIC, json=v2_envelope(None)).install(monkeypatch)

    assert await data_source.query_train_info("G1", TRAIN_DATE) is None


async def test_query_train_info_resolves_a_single_candidate_and_requeries(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A single preselect candidate is queried again with the resolved train code."""
    from nonebot_plugin_cnrail import data_source

    api = (
        QueuedRailGo(
            [
                (400, None),
                (
                    200,
                    v2_envelope(
                        train_main_payload(
                            numberFull=["G2"],
                            timetable=G2_TIMETABLE,
                        ),
                    ),
                ),
            ],
        )
        .route(TRAIN_PRESELECT, json=["G2"])
        .route(GET_COACH_PIC, json=v2_envelope(coach_pic_payload()))
        .install(monkeypatch)
    )

    info = await data_source.query_train_info("G1", TRAIN_DATE)

    assert info is not None
    assert info.search.train_number == "G2"
    assert info.sn is not None
    assert info.sn[0].emu_serial_number == "CR400AF-2001"
    assert api.queries(GET_TRAIN_MAIN) == [
        {"trainNum": "G1", "date": TRAIN_DATE},
        {"trainNum": "G2", "date": TRAIN_DATE},
    ]
    assert api.queries(GET_COACH_PIC) == [{"train": "G2"}]


async def test_query_train_info_returns_none_when_a_candidate_carries_the_code(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A candidate containing the queried code is never re-queried."""
    from nonebot_plugin_cnrail import data_source

    api = (
        FakeRailGo()
        .route(GET_TRAIN_MAIN, status=400)
        .route(TRAIN_PRESELECT, json=["G1/G2"])
        .install(monkeypatch)
    )

    assert await data_source.query_train_info("G1", TRAIN_DATE) is None
    assert api.queries(GET_TRAIN_MAIN) == [{"trainNum": "G1", "date": TRAIN_DATE}]
    assert api.queries(GET_COACH_PIC) == []


async def test_query_train_info_raises_for_multiple_candidates(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Ambiguous candidates are reported with the full candidate list."""
    from nonebot_plugin_cnrail import data_source

    api = (
        FakeRailGo()
        .route(GET_TRAIN_MAIN, status=400)
        .route(TRAIN_PRESELECT, json=["G2", "G3"])
        .install(monkeypatch)
    )

    with pytest.raises(data_source.MultipleTrainFoundError) as exc_info:
        await data_source.query_train_info("G1", TRAIN_DATE)

    assert exc_info.value.trains == ["G2", "G3"]
    assert api.queries(GET_TRAIN_MAIN) == [{"trainNum": "G1", "date": TRAIN_DATE}]


async def test_query_train_info_returns_none_without_candidates(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An unknown train code is reported as nothing to query."""
    from nonebot_plugin_cnrail import data_source

    api = (
        FakeRailGo()
        .route(GET_TRAIN_MAIN, status=400)
        .route(TRAIN_PRESELECT, json=[])
        .install(monkeypatch)
    )

    assert await data_source.query_train_info("G1", TRAIN_DATE) is None
    assert api.queries(GET_TRAIN_MAIN) == [{"trainNum": "G1", "date": TRAIN_DATE}]
    assert api.queries(GET_COACH_PIC) == []


async def test_query_train_info_returns_none_when_the_candidate_has_no_data(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A candidate that again has no data leaves the query empty handed."""
    from nonebot_plugin_cnrail import data_source

    api = (
        FakeRailGo()
        .route(GET_TRAIN_MAIN, status=400)
        .route(TRAIN_PRESELECT, json=["G2"])
        .install(monkeypatch)
    )

    assert await data_source.query_train_info("G1", TRAIN_DATE) is None
    assert api.queries(GET_TRAIN_MAIN) == [
        {"trainNum": "G1", "date": TRAIN_DATE},
        {"trainNum": "G2", "date": TRAIN_DATE},
    ]
    assert api.queries(GET_COACH_PIC) == []


async def test_query_train_info_survives_a_coach_pic_failure(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A coach picture that cannot be fetched only costs the serial number."""
    from nonebot_plugin_cnrail import data_source

    api = (
        FakeRailGo()
        .route(
            GET_TRAIN_MAIN,
            json=v2_envelope(train_main_payload(timetable=TWO_STATION_TIMETABLE)),
        )
        .route(GET_COACH_PIC, status=500)
        .install(monkeypatch)
    )

    info = await data_source.query_train_info("G1", TRAIN_DATE)

    assert info is not None
    assert info.sn is None
    assert info.search.train_number == "G1"
    assert info.detail.company_name == "北京局"
    assert api.queries(GET_COACH_PIC) == [{"train": "G1"}]
