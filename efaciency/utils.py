"""efaciency utils"""

from datetime import date, datetime, timedelta

import pytz

LOCAL_TZ = pytz.timezone("Europe/London")
UTC = pytz.utc
DST_DATES = [t.date() for t in LOCAL_TZ._utc_transition_times]


def convert_to_local(ts: datetime, is_dst: bool = None) -> datetime:
    """Convert timestamp to GB local time. If naive, then localize to GB local time."""
    if ts in LOCAL_TZ._utc_transition_times and ts.month == 3:
        raise ValueError(f"{ts} does not exist in UK time.")
    if ts.tzinfo is None:
        return LOCAL_TZ.localize(ts, is_dst)
    return ts.astimezone(LOCAL_TZ)


def convert_to_utc(ts: datetime) -> datetime:
    """Convert timestamp to UTC."""
    if ts.tzinfo is None:
        raise ValueError("ts is timezone-unaware so cannot be converted to UTC.")
    return ts.astimezone(UTC)


def get_efa_date(ts: datetime) -> date:
    """Get EFA date from datetime."""
    ts_local = convert_to_local(ts)
    return (ts_local + timedelta(hours=1)).date()


def get_efa_block(ts: datetime) -> int:
    """Get EFA block from datetime."""
    ts_local = convert_to_local(ts)
    return int((ts_local + timedelta(hours=1)).hour / 4) + 1


def get_settlement_date(ts: datetime) -> date:
    """Get settlement date from datetime."""
    ts_local = convert_to_local(ts)
    return ts_local.date()


def _get_settlement_period_on_utc_transition(ts: datetime) -> int:
    """Get settlement period from datetime on a day of DST change."""
    ts_local = convert_to_local(ts)
    if ts_local.date().month == 3:
        diff = int(ts_local.dst().total_seconds() / 1800)
    if ts_local.date().month == 10:
        diff = int(ts_local.dst().total_seconds() / 1800) - 2
    return ts_local.hour * 2 + int(ts_local.minute / 30) + 1 - diff


def get_settlement_period(ts: datetime) -> int:
    """Get settlement period from datetime."""
    if ts.date() in DST_DATES:
        return _get_settlement_period_on_utc_transition(ts)
    ts_local = convert_to_local(ts)
    return ts_local.hour * 2 + int(ts_local.minute / 30) + 1


def _get_ts_on_utc_transition(
    settlement_date: date, settlement_period: int
) -> datetime:
    """Get datetime from settlement date and settlement period on a day of DST change."""
    origin = datetime.combine(settlement_date, datetime.min.time())
    diff = 0
    is_dst = True
    if settlement_date.month == 3:
        assert settlement_period in range(
            1, 47
        ), "settlement_period must be a number between 1 and 46."
        if settlement_period > 2:
            diff = 2
    if settlement_date.month == 10:
        assert settlement_period in range(
            1, 51
        ), "settlement_period must be a number between 1 and 50."
        if settlement_period > 4:
            diff = -2
            is_dst = False
    return convert_to_local(
        origin + timedelta(hours=(settlement_period + diff - 1) / 2), is_dst
    )


def get_ts(settlement_date: date, settlement_period: int) -> datetime:
    """Get datetime from settlement date and settlement period."""
    origin = datetime.combine(settlement_date, datetime.min.time())
    if settlement_date in DST_DATES:
        return _get_ts_on_utc_transition(settlement_date, settlement_period)
    assert settlement_period in range(
        1, 49
    ), "settlement_period must be a number between 1 and 48."
    return convert_to_local(origin + timedelta(hours=(settlement_period - 1) / 2))


def _validate_efa_block_number(efa_block: int):
    """Check that a provided EFA block number is valid."""
    assert efa_block in range(1, 7), "efa_block must be a number between 1 and 6."


def get_efa_start_time(efa_date: date, efa_block: int) -> datetime:
    """Get EFA start time from EFA date and EFA block."""
    _validate_efa_block_number(efa_block)
    origin = datetime.combine(efa_date, datetime.min.time()) - timedelta(hours=1)
    return convert_to_local(origin + timedelta(hours=(efa_block - 1) * 4))


def get_efa_end_time(efa_date: date, efa_block: int) -> datetime:
    """Get EFA end time from EFA date and EFA block."""
    _validate_efa_block_number(efa_block)
    origin = datetime.combine(efa_date, datetime.min.time()) - timedelta(hours=1)
    return convert_to_local(origin + timedelta(hours=efa_block * 4))
