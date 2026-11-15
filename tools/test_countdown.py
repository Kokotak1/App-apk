#!/usr/bin/env python3
"""Local-date, 4-day duty-cycle regression checks."""
from datetime import date, timedelta

FIRST = date(2026, 11, 18)
END = date(2027, 10, 1)


def remaining(day: date) -> int:
    if day < FIRST:
        return 80
    if day >= END:
        return 0
    days_since = (day - FIRST).days
    return max(0, min(80, 80 - (days_since + 3) // 4))


duties = [FIRST + timedelta(days=4 * n) for n in range(80)]
assert len(duties) == 80 and duties[-1] == date(2027, 9, 30)
for day, expected in [
    (date(2026, 11, 15), 80),
    (date(2026, 11, 17), 80),
    (date(2026, 11, 18), 80),
    (date(2026, 11, 19), 79),
    (date(2026, 11, 22), 79),
    (date(2026, 11, 23), 78),
    (date(2027, 9, 30), 1),
    (date(2027, 10, 1), 0),
]:
    assert remaining(day) == expected, (day, remaining(day), expected)
print("OK: 80 shifts, 2026-11-18 to 2027-09-30; 0 on 2027-10-01")
