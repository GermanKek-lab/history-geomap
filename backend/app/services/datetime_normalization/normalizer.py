from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date

MONTHS = {
    "января": 1,
    "февраля": 2,
    "марта": 3,
    "апреля": 4,
    "мая": 5,
    "июня": 6,
    "июля": 7,
    "августа": 8,
    "сентября": 9,
    "октября": 10,
    "ноября": 11,
    "декабря": 12,
}

SEASONS = {
    "весной": (3, 1, 5, 31),
    "летом": (6, 1, 8, 31),
    "осенью": (9, 1, 11, 30),
    "зимой": (12, 1, 2, 28),
}

QUALIFIER_MONTHS = {
    "начале": (1, 1, 4, 30),
    "середине": (5, 1, 8, 31),
    "конце": (9, 1, 12, 31),
}

ROMAN = {"I": 1, "V": 5, "X": 10}


@dataclass(slots=True)
class NormalizedDate:
    start: date | None
    end: date | None
    label: str | None
    precision: str


def roman_to_int(value: str) -> int:
    total = 0
    previous = 0
    for symbol in reversed(value.upper()):
        current = ROMAN[symbol]
        if current < previous:
            total -= current
        else:
            total += current
            previous = current
    return total


def _end_of_month(year: int, month: int) -> int:
    if month == 2:
        return 29 if year % 4 == 0 else 28
    if month in {4, 6, 9, 11}:
        return 30
    return 31


def normalize_time_expression(value: str | None) -> NormalizedDate:
    if not value or not value.strip():
        return NormalizedDate(start=None, end=None, label=None, precision="unknown")

    raw = value.strip().lower()

    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw):
        parsed = date.fromisoformat(raw)
        return NormalizedDate(start=parsed, end=parsed, label=None, precision="day")

    full_date = re.search(r"(\d{1,2})\s+([а-яё]+)\s+(\d{4})\s+года", raw)
    if full_date:
        day = int(full_date.group(1))
        month = MONTHS[full_date.group(2)]
        year = int(full_date.group(3))
        parsed = date(year, month, day)
        return NormalizedDate(start=parsed, end=parsed, label=None, precision="day")

    qualifier_year = re.search(r"в\s+(начале|середине|конце)\s+(\d{4})\s+года", raw)
    if qualifier_year:
        qualifier = qualifier_year.group(1)
        year = int(qualifier_year.group(2))
        start_month, start_day, end_month, end_day = QUALIFIER_MONTHS[qualifier]
        return NormalizedDate(
            start=date(year, start_month, start_day),
            end=date(year, end_month, end_day),
            label=f"{qualifier.capitalize()} {year} года",
            precision="range",
        )

    season_year = re.search(r"(весной|летом|осенью|зимой)\s+(\d{4})\s+года", raw)
    if season_year:
        season = season_year.group(1)
        year = int(season_year.group(2))
        start_month, start_day, end_month, end_day = SEASONS[season]
        end_year = year if season != "зимой" else year + 1
        return NormalizedDate(
            start=date(year, start_month, start_day),
            end=date(end_year, end_month, end_day),
            label=f"{season.capitalize()} {year} года",
            precision="season",
        )

    century = re.search(r"(?:в\s+)?(начале|середине|конце)\s+([ivx]+)\s+века", raw, flags=re.IGNORECASE)
    if century:
        qualifier = century.group(1)
        century_number = roman_to_int(century.group(2))
        start_year = (century_number - 1) * 100 + 1
        end_year = century_number * 100
        if qualifier == "начале":
            end_year = start_year + 32
        elif qualifier == "середине":
            start_year += 33
            end_year = start_year + 32
        else:
            start_year += 66
        return NormalizedDate(
            start=date(start_year, 1, 1),
            end=date(end_year, 12, 31),
            label=f"{qualifier.capitalize()} {century.group(2).upper()} века",
            precision="century-range",
        )

    year_only = re.search(r"(\d{4})\s+года|\b(\d{4})\b", raw)
    if year_only:
        year = int(year_only.group(1) or year_only.group(2))
        return NormalizedDate(
            start=date(year, 1, 1),
            end=date(year, 12, 31),
            label=str(year),
            precision="year",
        )

    return NormalizedDate(start=None, end=None, label=value, precision="unknown")
