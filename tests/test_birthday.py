from datetime import date

import pytest

from birthday import (
    calculate_age,
    create_birth_date,
    is_leap_year,
    render_date,
    weekday_ru,
)


def test_create_birth_date_accepts_valid_date():
    assert create_birth_date(29, 2, 2000, today=date(2026, 9, 7)) == date(2000, 2, 29)


def test_create_birth_date_rejects_impossible_date():
    with pytest.raises(ValueError, match="не существует"):
        create_birth_date(31, 2, 2020, today=date(2026, 9, 7))


def test_create_birth_date_rejects_future_date():
    with pytest.raises(ValueError, match="будущем"):
        create_birth_date(8, 9, 2026, today=date(2026, 9, 7))


def test_weekday_is_returned_in_russian():
    assert weekday_ru(date(2000, 2, 29)) == "вторник"


@pytest.mark.parametrize(
    ("year", "expected"),
    [(2000, True), (1900, False), (2024, True), (2025, False)],
)
def test_leap_year_uses_gregorian_rules(year, expected):
    assert is_leap_year(year) is expected


@pytest.mark.parametrize(
    ("born", "today", "expected"),
    [
        (date(2000, 9, 7), date(2026, 9, 7), 26),
        (date(2000, 9, 8), date(2026, 9, 7), 25),
        (date(2000, 9, 6), date(2026, 9, 7), 26),
    ],
)
def test_calculate_age_counts_full_years(born, today, expected):
    assert calculate_age(born, today) == expected


def test_render_date_has_five_equal_rows_and_stars():
    rows = render_date(date(2000, 2, 29)).splitlines()
    assert len(rows) == 5
    assert all("*" in row for row in rows)
    assert len({len(row) for row in rows}) == 1


def test_render_date_contains_visual_spaces_between_date_parts():
    first_row = render_date(date(2000, 2, 29)).splitlines()[0]
    assert "     " in first_row
