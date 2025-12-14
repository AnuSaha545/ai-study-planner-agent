"""Time utilities for building fixed-slot timetables."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import List, Tuple


def parse_hhmm(value: str) -> datetime:
    return datetime.strptime(value, "%H:%M")


def format_hhmm(dt: datetime) -> str:
    return dt.strftime("%H:%M")


def build_time_slots(
    start_time: str,
    daily_hours: float,
    slot_minutes: int = 60,
    break_minutes: int = 10,
) -> List[Tuple[str, str, float]]:
    """Build a list of slots with breaks between them.

    Returns list of (start, end, duration_hours).
    Breaks are inserted *between* slots and do not count towards duration.

    Example: start 07:00, daily_hours=3, slot=60, break=10 ->
      07:00-08:00, 08:10-09:10, 09:20-10:20
    """

    if daily_hours <= 0:
        return []

    # Round down to whole slots
    slots_count = int((daily_hours * 60) // slot_minutes)
    if slots_count <= 0:
        return []

    start_dt = parse_hhmm(start_time)
    slots: List[Tuple[str, str, float]] = []

    cur = start_dt
    for i in range(slots_count):
        end = cur + timedelta(minutes=slot_minutes)
        slots.append((format_hhmm(cur), format_hhmm(end), slot_minutes / 60.0))
        # add break after slot except the last
        if i < slots_count - 1:
            cur = end + timedelta(minutes=break_minutes)

    return slots
