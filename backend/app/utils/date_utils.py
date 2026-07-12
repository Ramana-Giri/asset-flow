"""
Date Calculation Helpers

Purpose
-------
Shared date/time helpers for overdue detection, booking windows, and audit cycle date ranges.

Responsibilities
-----------------
- is_overdue(expected_return_date): compare against current date.
- is_within_next_days(date, days): used for 'Upcoming Returns' KPI (e.g. next 7 days).
- ranges_overlap(start1, end1, start2, end2): half-open interval overlap check, mirroring the DB EXCLUDE constraint semantics.

Interacts With
--------------
- services/allocation_service.py -> overdue detection.
- services/booking_service.py -> overlap pre-check.
- services/dashboard_service.py -> KPI windows.
"""

from datetime import date, datetime, timedelta
from typing import Optional


def is_overdue(expected_return_date: Optional[date]) -> bool:
    """Return True if expected_return_date is in the past relative to today."""
    if expected_return_date is None:
        return False
    return expected_return_date < date.today()


def is_within_next_days(target_date: date, days: int) -> bool:
    """Return True if target_date falls within [today, today + days]."""
    today = date.today()
    return today <= target_date <= today + timedelta(days=days)


def ranges_overlap(start1: datetime, end1: datetime, start2: datetime, end2: datetime) -> bool:
    """
    Half-open interval overlap check: [start1, end1) intersects [start2, end2).
    Mirrors the Postgres EXCLUDE constraint semantics (excl_no_overlapping_bookings)
    so a 10:00-11:00 booking does NOT conflict with an existing 9:00-10:00 booking.
    """
    return start1 < end2 and start2 < end1