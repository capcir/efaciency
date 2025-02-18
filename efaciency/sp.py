"""Convert settlement periods to and from timestamps."""

from datetime import date, datetime, time, timedelta
from functools import cache
from zoneinfo import ZoneInfo

_gb_tz = ZoneInfo("Europe/London")


def from_ts(ts: datetime) -> int:
    """Get settlement period number from a given timestamp.

    On spring DST dates, SPs only go to 46. On autumn DST dates, SPs go to 50.

    Args:
        ts (datetime): timestamp

    Returns:
        int: SP number (1-50)
    """
    local_ts = ts.astimezone(_gb_tz)
    if local_ts.date() in _dst_transition_dates():
        utcoffset = local_ts.utcoffset().seconds / 3600
        if local_ts.date().month > 6 and utcoffset == 0:
            return int(local_ts.hour * 2 + local_ts.minute / 30 + 3)
        if local_ts.date().month < 6 and utcoffset == 1:
            return int(local_ts.hour * 2 + local_ts.minute / 30 - 1)
    return int(local_ts.hour * 2 + local_ts.minute / 30 + 1)


def to_ts(settlement_period: int, settlement_date: datetime | None = None) -> datetime:
    """Get timestamp from a given settlement period and settlement date (if given).

    Args:
        settlement_period (int): settlement period number
        settlement_date (date, optional): settlement date. Defaults to None.

    Returns:
        datetime: start of the settlement period half-hour
    """
    settlement_date = settlement_date or date.today()
    offset = timedelta(0)
    if settlement_date in _dst_transition_dates():
        if settlement_date.month > 6:
            assert 1 <= settlement_period <= 50, (
                "SP must be between 1 and 50 (autumn DST transition)."
            )
            if settlement_period >= 5:
                offset = -timedelta(hours=1)
        else:
            assert 1 <= settlement_period <= 46, (
                "SP must be between 1 and 46 (spring DST transition)."
            )
            if settlement_period >= 3:
                offset = timedelta(hours=1)
    else:
        assert 1 <= settlement_period <= 48, "SP must be between 1 and 48."
    t0 = datetime.combine(settlement_date, time.min).astimezone(_gb_tz)
    sp_ts = t0 + timedelta(minutes=30 * (settlement_period - 1))
    return sp_ts + offset


@cache
def _dst_transition_dates() -> list[date]:
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
