#!/usr/bin/env python3
"""Duty counter: switch to FREE after Monday 2027-08-02 at 07:00."""
from datetime import datetime, timedelta
from pathlib import Path
from xml.etree import ElementTree as ET

FIRST = datetime(2026, 11, 19, 7)
LAST = datetime(2027, 8, 2, 7)
EVENTS = []
t = FIRST
while t <= LAST:
    EVENTS.append(t)
    t += timedelta(days=4)
assert len(EVENTS) == 65 and EVENTS[-1] == LAST

def oracle(now):
    n = sum(event > now for event in EVENTS)
    return str(n) if n else "FREE"

def wff_mirror(now):
    y, d, h = now.year, now.timetuple().tm_yday, now.hour
    free = y > 2027 or (y == 2027 and (d > 214 or (d == 214 and h >= 7)))
    if free: return "FREE"
    if y < 2026: return "65"
    days = d - 323 if y == 2026 else 42 + d
    decrements = (days + (4 if h >= 7 else 3)) // 4
    return str(max(0, min(65, 65 - decrements)))

day = datetime(2026, 1, 1)
while day < datetime(2028, 1, 1):
    for hour in range(24):
        t = day.replace(hour=hour)
        assert wff_mirror(t) == oracle(t), (t, wff_mirror(t), oracle(t))
    day += timedelta(days=1)
for t in EVENTS:
    before = t - timedelta(minutes=1)
    assert wff_mirror(before) == oracle(before)
    assert wff_mirror(t) == oracle(t)
for t,v in [
    (datetime(2026,11,16,19),"65"),
    (datetime(2026,11,19,6,59),"65"),
    (datetime(2026,11,19,7),"64"),
    (datetime(2026,11,23,7),"63"),
    (datetime(2026,11,27,7),"62"),
    (datetime(2027,7,29,7),"1"),
    (datetime(2027,8,1,23,59),"1"),
    (datetime(2027,8,2,6,59),"1"),
    (datetime(2027,8,2,7),"FREE")
]:
    assert oracle(t) == v, (t,oracle(t),v)

root=ET.parse(Path(__file__).resolve().parents[1] / "watchface/src/main/res/raw/watchface.xml")
count_params=[n.attrib["expression"] for n in root.iter("Parameter")
              if "[DAY_OF_YEAR]" in n.attrib.get("expression", "")]
assert len(count_params)==2 and count_params[0]==count_params[1]
assert "65 - floor" in count_params[0]
conditions=[(n.attrib.get("name"),(n.text or "").strip()) for n in root.iter("Expression")]
free_conditions=[e for name,e in conditions if name in ("freeReachedActive","freeReachedAmbient")]
assert len(free_conditions)==2 and free_conditions[0]==free_conditions[1]
assert "[DAY_OF_YEAR] > 214" in free_conditions[0]
assert sum(1 for n in root.iter("Font") if (n.text or "").strip()=="FREE")==2
print("OK: 65 service completions at 07:00 every 4 days; FREE after 2027-08-02 07:00")
