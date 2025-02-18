"""Utility functions."""

from datetime import date, datetime, time, timedelta
from functools import cache
from zoneinfo import ZoneInfo

_gb_tz = ZoneInfo("Europe/London")


def convert_to_local(ts: datetime) -> datetime:
    if ts.tzinfo is None:
        return ts.replace(tzinfo=_gb_tz)
    return ts.astimezone(_gb_tz)


@cache
def dst_transition_dates() -> list[date]:
    """Get list of all DST transition dates for the timezone.

    Dates are only generated between 2000 and 10 years from today, assuming `efaciency` would not
    be used for any dates further in the past and/or future.

    This function is cached for performance.
    """
    from_date = date(2000, 1, 1)
    until_date = date.today() + timedelta(days=365 * 10)
    date_range = [from_date + timedelta(days=i) for i in range((until_date - from_date).days + 1)]
    offsets = {d: datetime.combine(d, time.min).astimezone(_gb_tz).utcoffset() for d in date_range}
    return [
        d0
        for d0, d1 in zip(date_range[:-1], date_range[1:], strict=True)
        if (offsets[d0] - offsets[d1]).seconds != 0
    ]
