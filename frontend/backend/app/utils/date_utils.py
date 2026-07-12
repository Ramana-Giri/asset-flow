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

NOTE: This file is a structural skeleton only. Method/function bodies are
intentionally left as `pass` (no business logic / SQL / validation code),
per generation scope. Docstrings describe what each piece IS responsible
for once implemented.
"""

from datetime import date, datetime


def is_overdue(expected_return_date: date | None) -> bool:
    """Return True if expected_return_date is in the past relative to today."""
    pass


def is_within_next_days(target_date: date, days: int) -> bool:
    """Return True if target_date falls within [today, today + days]."""
    pass


def ranges_overlap(start1: datetime, end1: datetime, start2: datetime, end2: datetime) -> bool:
    """
    Half-open interval overlap check: [start1, end1) intersects [start2, end2).
    Mirrors the Postgres EXCLUDE constraint semantics (excl_no_overlapping_bookings)
    so a 10:00-11:00 booking does NOT conflict with an existing 9:00-10:00 booking.
    """
    pass
