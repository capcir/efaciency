"""Utility functions."""

import itertools
from datetime import date, datetime, time, timedelta
from functools import cache
from zoneinfo import ZoneInfo

GB_TIMEZONE = ZoneInfo("Europe/London")


def convert_to_local(ts: datetime) -> datetime:
    """Convert to local time (Europe/London)."""
    if ts.tzinfo is None:
        return ts.replace(tzinfo=GB_TIMEZONE)
    return ts.astimezone(GB_TIMEZONE)


@cache
def dst_transition_dates() -> list[date]:
    """Get list of all DST transition dates for the timezone.

    Dates are only generated between 2000 and 10 years from today, assuming `efaciency` would not
    be used for any dates further in the past and/or future.

    This function is cached for performance.
    """
    from_date = datetime(2000, 1, 1, tzinfo=GB_TIMEZONE).date()
    until_date = datetime.now(GB_TIMEZONE).date() + timedelta(days=365 * 10)
    date_range = [from_date + timedelta(days=i) for i in range((until_date - from_date).days + 1)]
    offsets = {d: datetime.combine(d, time.min, GB_TIMEZONE).utcoffset() for d in date_range}
    return [
        d0 for d0, d1 in itertools.pairwise(date_range) if (offsets[d0] - offsets[d1]).seconds != 0
    ]
