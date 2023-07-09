"""efaciency utils"""

from datetime import date, datetime, timedelta

import pytz

LOCAL_TZ = pytz.timezone("Europe/London")


def convert_to_local(ts: datetime) -> datetime:
    """Convert timestamp to GB local time. If naive, then localize to GB local time."""
    if ts.tzinfo is None:
        return LOCAL_TZ.localize(ts)
    return ts.astimezone(LOCAL_TZ)


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


def get_settlement_period(ts: datetime) -> int:
    """Get settlement period from datetime."""
    ts_local = convert_to_local(ts)
    return ts_local.hour * 2 + int(ts_local.minute / 30) + 1


def get_ts(settlement_date: date, settlement_period: int) -> datetime:
    """Get datetime from settlement date and settlement period."""
    origin = convert_to_local(datetime.combine(settlement_date, datetime.min.time()))
    return origin + timedelta(hours=(settlement_period - 1) / 2)


def get_efa_start_time(efa_date: date, efa_block: int) -> datetime:
    """Get EFA start time from EFA date and EFA block."""
    origin = convert_to_local(
        datetime.combine(efa_date, datetime.min.time())
    ) - timedelta(hours=1)
    return origin + timedelta(hours=(efa_block - 1) * 4)


def get_efa_end_time(efa_date: date, efa_block: int) -> datetime:
    """Get EFA end time from EFA date and EFA block."""
    origin = convert_to_local(
        datetime.combine(efa_date, datetime.min.time())
    ) - timedelta(hours=1)
    return origin + timedelta(hours=efa_block * 4)
