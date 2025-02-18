from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

import pytest

import efaciency

_tz = ZoneInfo("Europe/London")


def test_efa_block_from_ts():
    t0 = datetime.combine(date(2025, 1, 1), time(23))
    for i in range(24):
        ts = t0 + timedelta(hours=i)
        assert efaciency.block.from_ts(ts) == int(i / 4) + 1


def test_efa_block_to_start_ts():
    assert efaciency.block.to_start_ts(1) == datetime.combine(
        date.today() - timedelta(days=1), time(23)
    ).astimezone(_tz)
    assert efaciency.block.to_start_ts(2) == datetime.combine(date.today(), time(3)).astimezone(_tz)
    assert efaciency.block.to_start_ts(3) == datetime.combine(date.today(), time(7)).astimezone(_tz)
    assert efaciency.block.to_start_ts(4) == datetime.combine(date.today(), time(11)).astimezone(
        _tz
    )
    assert efaciency.block.to_start_ts(5) == datetime.combine(date.today(), time(15)).astimezone(
        _tz
    )
    assert efaciency.block.to_start_ts(6) == datetime.combine(date.today(), time(19)).astimezone(
        _tz
    )


def test_efa_block_to_end_ts():
    assert efaciency.block.to_end_ts(1) == datetime.combine(date.today(), time(3)).astimezone(_tz)
    assert efaciency.block.to_end_ts(2) == datetime.combine(date.today(), time(7)).astimezone(_tz)
    assert efaciency.block.to_end_ts(3) == datetime.combine(date.today(), time(11)).astimezone(_tz)
    assert efaciency.block.to_end_ts(4) == datetime.combine(date.today(), time(15)).astimezone(_tz)
    assert efaciency.block.to_end_ts(5) == datetime.combine(date.today(), time(19)).astimezone(_tz)
    assert efaciency.block.to_end_ts(6) == datetime.combine(date.today(), time(23)).astimezone(_tz)


def test_efa_block_to_ts_with_date():
    assert efaciency.block.to_start_ts(efa_block=1, efa_date=date(2025, 3, 30)) == datetime.combine(
        date(2025, 3, 29), time(23)
    ).astimezone(_tz)
    assert efaciency.block.to_end_ts(efa_block=1, efa_date=date(2025, 3, 30)) == datetime.combine(
        date(2025, 3, 30), time(3)
    ).astimezone(_tz)
    assert efaciency.block.to_start_ts(
        efa_block=1, efa_date=date(2025, 10, 26)
    ) == datetime.combine(date(2025, 10, 25), time(23)).astimezone(_tz)
    assert efaciency.block.to_end_ts(efa_block=1, efa_date=date(2025, 10, 26)) == datetime.combine(
        date(2025, 10, 26), time(3)
    ).astimezone(_tz)


def test_efa_block_to_ts_assertion_error():
    with pytest.raises(AssertionError) as e:
        efaciency.block.to_start_ts(efa_block=0)
    assert e.value.args[0] == "EFA block must be between 1 and 6."
    with pytest.raises(AssertionError) as e:
        efaciency.block.to_end_ts(efa_block=7)
    assert e.value.args[0] == "EFA block must be between 1 and 6."
