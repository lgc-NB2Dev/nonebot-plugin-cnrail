"""Tests for `parse_date` and the clock window it accepts."""

from datetime import date

import pytest

from tests_nbp_cnrail.utils.clock import freeze_clock


def test_parse_date_accepts_every_supported_spelling(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Equivalent month/day spellings resolve to the same date."""
    from nonebot_plugin_cnrail import __main__ as main

    freeze_clock(monkeypatch, main, "2024-12-15")

    expected = date(2024, 12, 20)
    spellings = ("12-20", "12/20", "12月20日", "12月20号", "12月20", "12 月 20 日")
    assert [main.parse_date(item) for item in spellings] == [expected] * len(spellings)


def test_parse_date_strips_whitespace_everywhere(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Whitespace is ignored anywhere inside the date string."""
    from nonebot_plugin_cnrail import __main__ as main

    freeze_clock(monkeypatch, main, "2024-12-15")

    expected = date(2024, 12, 20)
    padded = (" 12-20 ", "\t12-20\n", "1 2 - 2 0", "12 月 20 号 ")
    assert [main.parse_date(item) for item in padded] == [expected] * len(padded)


def test_parse_date_accepts_the_window_boundaries(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The inclusive window spans two days back to fourteen days ahead."""
    from nonebot_plugin_cnrail import __main__ as main

    freeze_clock(monkeypatch, main, "2024-12-15")

    assert main.parse_date("12-13") == date(2024, 12, 13)
    assert main.parse_date("12-29") == date(2024, 12, 29)


def test_parse_date_rejects_dates_outside_the_window(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Dates before the window start or after its end are rejected."""
    from nonebot_plugin_cnrail import __main__ as main

    freeze_clock(monkeypatch, main, "2024-12-15")

    with pytest.raises(ValueError):  # noqa: PT011 - `parse_date` raises a bare ValueError
        main.parse_date("12-12")
    with pytest.raises(ValueError):  # noqa: PT011 - `parse_date` raises a bare ValueError
        main.parse_date("12-30")


def test_parse_date_maps_a_recent_past_date_to_the_previous_year(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A year-end date that already passed resolves to the previous year."""
    from nonebot_plugin_cnrail import __main__ as main

    freeze_clock(monkeypatch, main, "2025-01-01")

    assert main.parse_date("12-31") == date(2024, 12, 31)


def test_parse_date_maps_an_upcoming_date_to_the_next_year(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A year-start date inside the window resolves to the next year."""
    from nonebot_plugin_cnrail import __main__ as main

    freeze_clock(monkeypatch, main, "2024-12-31")

    assert main.parse_date("01-05") == date(2025, 1, 5)


def test_parse_date_rejects_unparsable_input(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Empty, malformed and out-of-range strings are rejected."""
    from nonebot_plugin_cnrail import __main__ as main

    freeze_clock(monkeypatch, main, "2024-12-15")

    for garbage in ("", "abc", "13月40日", "12-32"):
        with pytest.raises(ValueError):  # noqa: PT011 - `parse_date` raises a bare ValueError
            main.parse_date(garbage)


def test_parse_date_accepts_a_leap_day_in_a_leap_year(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A leap day resolves inside a leap year."""
    from nonebot_plugin_cnrail import __main__ as main

    freeze_clock(monkeypatch, main, "2024-03-01")

    assert main.parse_date("02-29") == date(2024, 2, 29)


def test_parse_date_rejects_a_leap_day_outside_a_leap_year(
    cnrail_plugin: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A leap day no candidate year of the window can hold is rejected."""
    from nonebot_plugin_cnrail import __main__ as main

    freeze_clock(monkeypatch, main, "2023-03-01")

    with pytest.raises(ValueError):  # noqa: PT011 - `parse_date` raises a bare ValueError
        main.parse_date("02-29")
