#!/usr/bin/env python3
"""Regression tests for 4-day work-duty completion at 07:00 local time."""
from datetime import datetime, timedelta
from pathlib import Path
from xml.etree import ElementTree as ET

FIRST = datetime(2026, 11, 19, 7, 0)
END = datetime(2027, 8, 1, 0, 0)
EVENTS = []
t = FIRST
while t < END:
    EVENTS.append(t)
    t += timedelta(days=4)
assert len(EVENTS) == 64, len(EVENTS)
assert EVENTS[-1] == datetime(2027, 7, 29, 7, 0)
assert EVENTS[1] == datetime(2026, 11, 23, 7, 0)
assert EVENTS[2] == datetime(2026, 11, 27, 7, 0)


def remaining_reference(now: datetime) -> int:
    """Oracle: enumerate services already completed, independent of formula."""
    return sum(t > now for t in EVENTS)


def remaining_wff_formula(now: datetime) -> int:
    """Mirror WFF date-plus-clock expression, including New Year's rollover."""
    year = now.year
    if year < 2026:
        return 64
    if year > 2027:
        return 0
    day_serial = (now.timetuple().tm_yday - 323) if year == 2026 else (42 + now.timetuple().tm_yday)
    completed = (day_serial + (4 if now.hour >= 7 else 3)) // 4
    return max(0, min(64, 64 - completed))


# Check all hours of every day throughout the two target years.
now = datetime(2026, 1, 1)
while now < datetime(2028, 1, 1):
    for hour in range(24):
        x = now.replace(hour=hour)
        assert remaining_wff_formula(x) == remaining_reference(x), (x, remaining_wff_formula(x), remaining_reference(x))
    now += timedelta(days=1)

for t in EVENTS:
    before = t - timedelta(minutes=1)
    assert remaining_wff_formula(before) == remaining_reference(before)
    assert remaining_wff_formula(t) == remaining_reference(t)
    assert remaining_wff_formula(t) == remaining_wff_formula(before) - 1

assert remaining_wff_formula(datetime(2026, 11, 16, 19)) == 64
assert remaining_wff_formula(datetime(2026, 11, 19, 6, 59)) == 64
assert remaining_wff_formula(datetime(2026, 11, 19, 7, 0)) == 63
assert remaining_wff_formula(datetime(2026, 11, 23, 7)) == 62
assert remaining_wff_formula(datetime(2027, 7, 29, 6, 59)) == 1
assert remaining_wff_formula(datetime(2027, 7, 29, 7)) == 0
assert remaining_wff_formula(END) == 0

# Prevent regressions where the actual watch face uses a different formula.
face = ET.parse(Path(__file__).resolve().parents[1] / "watchface/src/main/res/raw/watchface.xml")
counter_exprs = [
    node.attrib["expression"]
    for node in face.iter("Parameter")
    if "[DAY_OF_YEAR]" in node.attrib.get("expression", "")
]
assert len(counter_exprs) == 2, counter_exprs
assert counter_exprs[0] == counter_exprs[1]
for piece in ("[HOUR_0_23]", "[DAY_OF_YEAR] - 323", "42 + [DAY_OF_YEAR]", "64 - floor"):
    assert piece in counter_exprs[0], (piece, counter_exprs[0])

print("OK: 64 duty decrements, first 2026-11-19 07:00, last 2027-07-29 07:00")
