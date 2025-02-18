"""Convert EFA blocks to and from timestamps."""

from datetime import date, datetime, time, timedelta

from efaciency.utils import convert_to_local


def from_ts(ts: datetime) -> int:
    """Get EFA block number from a given timestamp.

    Args:
        ts (datetime): timestamp

    Returns:
        int: EFA block number (1-6)
    """
    return int((convert_to_local(ts) + timedelta(hours=1)).hour / 4) + 1


def to_start_ts(efa_block: int, efa_date: date | None = None) -> datetime:
    """Get starting timestamp for a given EFA block number and EFA date (if given).

    Args:
        efa_block (int): EFA block number
        efa_date (date, optional): EFA date. Defaults to None.

    Returns:
        datetime: start of the block 4 hour period
    """
    assert 1 <= efa_block <= 6, "EFA block must be between 1 and 6."
    efa_date = efa_date or date.today()
    t0 = convert_to_local(datetime.combine(efa_date - timedelta(days=1), time(23)))
    return t0 + timedelta(hours=4 * (efa_block - 1))


def to_end_ts(efa_block: int, efa_date: date | None = None) -> datetime:
    """Get end timestamp for a given EFA block number and EFA date (if given).

    Args:
        efa_block (int): EFA block number
        efa_date (date, optional): EFA date. Defaults to None.

    Returns:
        datetime: end of the block 4 hour period
    """
    assert 1 <= efa_block <= 6, "EFA block must be between 1 and 6."
    efa_date = efa_date or date.today()
    t0 = convert_to_local(datetime.combine(efa_date - timedelta(days=1), time(23)))
    return t0 + timedelta(hours=4 * efa_block)
