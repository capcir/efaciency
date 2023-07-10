from datetime import date, datetime

import pytest

from efaciency.utils import *

STR_FORMAT = "%Y-%m-%d %H:%M:%S%z"


def test_convert_to_local():
    assert (
        convert_to_local(datetime(2023, 1, 1, 11)).strftime(STR_FORMAT)
        == "2023-01-01 11:00:00+0000"
    )
    assert (
        convert_to_local(datetime(2023, 7, 1, 11)).strftime(STR_FORMAT)
        == "2023-07-01 11:00:00+0100"
    )
    assert (
        convert_to_local(datetime(2023, 10, 29, 1), is_dst=True).strftime(STR_FORMAT)
        == "2023-10-29 01:00:00+0100"
    )
    assert (
        convert_to_local(datetime(2023, 10, 29, 1), is_dst=False).strftime(STR_FORMAT)
        == "2023-10-29 01:00:00+0000"
    )
    assert (
        convert_to_local(datetime(2023, 10, 29, 2), is_dst=False).strftime(STR_FORMAT)
        == "2023-10-29 02:00:00+0000"
    )
    assert (
        convert_to_local(datetime(2023, 10, 29, 2), is_dst=False).strftime(STR_FORMAT)
        == "2023-10-29 02:00:00+0000"
    )
    assert (
        convert_to_local(datetime(2023, 3, 26, 2), is_dst=True).strftime(STR_FORMAT)
        == "2023-03-26 02:00:00+0100"
    )
    assert (
        convert_to_local(datetime(2023, 3, 26, 2), is_dst=False).strftime(STR_FORMAT)
        == "2023-03-26 02:00:00+0100"
    )
    with pytest.raises(ValueError) as e:
        convert_to_local(datetime(2023, 3, 26, 1))
    assert str(e.value) == "2023-03-26 01:00:00 does not exist in UK time."


def test_convert_to_utc():
    assert (
        convert_to_utc(convert_to_local(datetime(2023, 1, 1, 11))).strftime(STR_FORMAT)
        == "2023-01-01 11:00:00+0000"
    )
    assert (
        convert_to_utc(convert_to_local(datetime(2023, 7, 1, 11))).strftime(STR_FORMAT)
        == "2023-07-01 10:00:00+0000"
    )
    assert (
        convert_to_utc(
            convert_to_local(datetime(2023, 10, 29, 1), is_dst=True)
        ).strftime(STR_FORMAT)
        == "2023-10-29 00:00:00+0000"
    )
    assert (
        convert_to_utc(
            convert_to_local(datetime(2023, 10, 29, 1), is_dst=False)
        ).strftime(STR_FORMAT)
        == "2023-10-29 01:00:00+0000"
    )
    assert (
        convert_to_utc(
            convert_to_local(datetime(2023, 3, 26, 2), is_dst=True)
        ).strftime(STR_FORMAT)
        == "2023-03-26 01:00:00+0000"
    )
    assert (
        convert_to_utc(
            convert_to_local(datetime(2023, 3, 26, 2), is_dst=False)
        ).strftime(STR_FORMAT)
        == "2023-03-26 01:00:00+0000"
    )
    with pytest.raises(ValueError) as e:
        convert_to_utc(datetime(2023, 1, 1, 1))
    assert str(e.value) == "ts is timezone-unaware so cannot be converted to UTC."


def test_get_efa_date():
    assert get_efa_date(datetime(2023, 1, 1, 0)) == date(2023, 1, 1)
    assert get_efa_date(datetime(2023, 1, 1, 23)) == date(2023, 1, 2)


def test_get_efa_block():
    assert get_efa_block(datetime(2023, 1, 1, 23)) == 1
    for h in range(3):
        assert get_efa_block(datetime(2023, 1, 2, h)) == 1
    for h in range(3, 7):
        assert get_efa_block(datetime(2023, 1, 2, h)) == 2
    for h in range(7, 11):
        assert get_efa_block(datetime(2023, 1, 2, h)) == 3
    for h in range(11, 15):
        assert get_efa_block(datetime(2023, 1, 2, h)) == 4
    for h in range(15, 19):
        assert get_efa_block(datetime(2023, 1, 2, h)) == 5
    for h in range(19, 23):
        assert get_efa_block(datetime(2023, 1, 2, h)) == 6


def test_get_settlement_date():
    assert get_settlement_date(datetime(2023, 1, 1, 0)) == date(2023, 1, 1)
    assert get_settlement_date(datetime(2023, 1, 1, 23)) == date(2023, 1, 1)
    assert get_settlement_date(datetime(2023, 2, 1, 23)) == date(2023, 2, 1)


def test_get_settlement_period():
    assert get_settlement_period(datetime(2023, 1, 1, 11)) == 23
    assert get_settlement_period(datetime(2023, 7, 1, 11)) == 23
    assert get_settlement_period(datetime(2023, 10, 29, 11, tzinfo=UTC)) == 25
    assert get_settlement_period(datetime(2023, 3, 26, 11)) == 21


def test_get_ts():
    assert (
        get_ts(date(2023, 1, 1), 32).strftime(STR_FORMAT) == "2023-01-01 15:30:00+0000"
    )
    assert (
        get_ts(date(2023, 7, 1), 32).strftime(STR_FORMAT) == "2023-07-01 15:30:00+0100"
    )
    assert (
        get_ts(date(2023, 3, 26), 2).strftime(STR_FORMAT) == "2023-03-26 00:30:00+0000"
    )
    assert (
        get_ts(date(2023, 3, 26), 3).strftime(STR_FORMAT) == "2023-03-26 02:00:00+0100"
    )
    assert (
        get_ts(date(2023, 10, 29), 3).strftime(STR_FORMAT) == "2023-10-29 01:00:00+0100"
    )
    assert (
        get_ts(date(2023, 10, 29), 5).strftime(STR_FORMAT) == "2023-10-29 01:00:00+0000"
    )
    assert (
        get_ts(date(2023, 10, 29), 50).strftime(STR_FORMAT)
        == "2023-10-29 23:30:00+0000"
    )
    with pytest.raises(AssertionError) as e:
        get_ts(date(2022, 10, 30), 51)
    assert str(e.value) == "settlement_period must be a number between 1 and 50."
    with pytest.raises(AssertionError) as e:
        get_ts(date(2022, 3, 27), 47)
    assert str(e.value) == "settlement_period must be a number between 1 and 46."
    with pytest.raises(AssertionError) as e:
        get_ts(date(2023, 1, 29), 49)
    assert str(e.value) == "settlement_period must be a number between 1 and 48."


def test_get_efa_start_time():
    assert (
        get_efa_start_time(date(2023, 1, 1), 3).strftime(STR_FORMAT)
        == "2023-01-01 07:00:00+0000"
    )
    assert (
        get_efa_start_time(date(2023, 7, 1), 3).strftime(STR_FORMAT)
        == "2023-07-01 07:00:00+0100"
    )
    with pytest.raises(AssertionError) as e:
        get_efa_start_time(date(2022, 7, 1), 7)
    assert str(e.value) == "efa_block must be a number between 1 and 6."


def test_get_efa_end_time():
    assert (
        get_efa_end_time(date(2023, 1, 1), 3).strftime(STR_FORMAT)
        == "2023-01-01 11:00:00+0000"
    )
    assert (
        get_efa_end_time(date(2023, 7, 1), 3).strftime(STR_FORMAT)
        == "2023-07-01 11:00:00+0100"
    )
