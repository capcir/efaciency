"""Convert EFA blocks to and from timestamps."""

from datetime import date, datetime, time, timedelta

from efaciency.utils import GB_TIMEZONE, convert_to_local


class EFABlockInputError(Exception):
    """Incorrect EFA block input error."""

    def __init__(self, number: int) -> Exception:
        """Incorrect EFA block input error."""
        super().__init__(f"EFA block must be between 1 and 6, not {number}.")


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
    if not 1 <= efa_block <= 6:
        raise EFABlockInputError(efa_block)
    efa_date = efa_date or datetime.now(GB_TIMEZONE).date()
    t0 = datetime.combine(efa_date - timedelta(days=1), time(23), GB_TIMEZONE)
    return t0 + timedelta(hours=4 * (efa_block - 1))


def to_end_ts(efa_block: int, efa_date: date | None = None) -> datetime:
    """Get end timestamp for a given EFA block number and EFA date (if given).

    Args:
        efa_block (int): EFA block number
        efa_date (date, optional): EFA date. Defaults to None.

    Returns:
        datetime: end of the block 4 hour period
    """
    if not 1 <= efa_block <= 6:
        raise EFABlockInputError(efa_block)
    efa_date = efa_date or datetime.now(GB_TIMEZONE).date()
    t0 = datetime.combine(efa_date - timedelta(days=1), time(23), GB_TIMEZONE)
    return t0 + timedelta(hours=4 * efa_block)
