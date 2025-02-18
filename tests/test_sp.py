from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

import pytest

import efaciency

_tz = ZoneInfo("Europe/London")


def test_sp_from_ts():
    t0 = datetime.combine(date(2025, 1, 1), time(0))
    for i in range(1, 49):
        ts = t0 + timedelta(minutes=30 * (i - 1))
        assert efaciency.sp.from_ts(ts) == i


def test_sp_to_ts():
    t0 = datetime.combine(date.today(), time(0))
    for i in range(1, 49):
        ts = t0 + timedelta(minutes=30 * (i - 1))
        assert efaciency.sp.to_ts(i) == ts.astimezone(_tz)


def test_sp_to_ts_with_date():
    assert efaciency.sp.to_ts(3, date(2025, 3, 30)) == datetime.combine(
        date(2025, 3, 30), time(2)
    ).astimezone(_tz)
    assert efaciency.sp.to_ts(46, date(2025, 3, 30)) == datetime.combine(
        date(2025, 3, 30), time(23, 30)
    ).astimezone(_tz)
    assert efaciency.sp.to_ts(3, date(2025, 10, 26)) == datetime.combine(
        date(2025, 10, 26), time(1)
    ).astimezone(_tz)
    assert efaciency.sp.to_ts(6, date(2025, 10, 26)) == datetime.combine(
        date(2025, 10, 26), time(1, 30)
    ).replace(fold=1).astimezone(_tz)
    assert efaciency.sp.to_ts(50, date(2025, 10, 26)) == datetime.combine(
        date(2025, 10, 26), time(23, 30)
    ).astimezone(_tz)


def test_sp_to_ts_assertion_errors():
    with pytest.raises(AssertionError) as e:
        efaciency.sp.to_ts(0)
    assert e.value.args[0] == "SP must be between 1 and 48."
    with pytest.raises(AssertionError) as e:
        efaciency.sp.to_ts(47, date(2025, 3, 30))
    assert e.value.args[0] == "SP must be between 1 and 46 (spring DST transition)."
    with pytest.raises(AssertionError) as e:
        efaciency.sp.to_ts(51, date(2025, 10, 26))
    assert e.value.args[0] == "SP must be between 1 and 50 (autumn DST transition)."


def test_sp_from_ts_on_dst_transitions():
    assert efaciency.sp.from_ts(datetime(2025, 3, 30, 1)) == 3
    assert efaciency.sp.from_ts(datetime(2025, 3, 30, 23, 30)) == 46
    assert efaciency.sp.from_ts(datetime(2025, 10, 26, 1)) == 3
    assert efaciency.sp.from_ts(datetime(2025, 10, 26, 1).replace(fold=1)) == 5
    assert efaciency.sp.from_ts(datetime(2025, 10, 26, 23)) == 49
