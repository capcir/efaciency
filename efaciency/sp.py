"""Convert settlement periods to and from timestamps."""

from datetime import datetime, time, timedelta

from efaciency.utils import GB_TIMEZONE, convert_to_local, dst_transition_dates


class SettlementPeriodInputError(Exception):
    """Incorrect settlement period] input error."""

    def __init__(self, number: int, message: str | None = None) -> Exception:
        """Incorrect settlement period] input error."""
        message = message or "SP must be between 1 and 48"
        super().__init__(f"{message}, not {number}.")


class AutumnClockChangeError(SettlementPeriodInputError):
    """Incorrect settlement period] input error during autumn clock change."""

    def __init__(self, number: int) -> SettlementPeriodInputError:
        """Incorrect settlement period] input error during autumn clock change."""
        super().__init__(message="SP must be between 1 and 50", number=number)


class SpringClockChangeError(SettlementPeriodInputError):
    """Incorrect settlement period] input error during spring clock change."""

    def __init__(self, number: int) -> SettlementPeriodInputError:
        """Incorrect settlement period] input error during spring clock change."""
        super().__init__(message="SP must be between 1 and 46", number=number)


def from_ts(ts: datetime) -> int:
    """Get settlement period number from a given timestamp.

    On spring DST dates, SPs only go to 46. On autumn DST dates, SPs go to 50.

    Args:
        ts (datetime): timestamp

    Returns:
        int: SP number (1-50)
    """
    local_ts = convert_to_local(ts)
    if local_ts.date() in dst_transition_dates():
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
    settlement_date = settlement_date or datetime.now(GB_TIMEZONE).date()
    offset = timedelta(0)
    fold = 0
    if settlement_date in dst_transition_dates():
        if settlement_date.month > 6:
            if not 1 <= settlement_period <= 50:
                raise AutumnClockChangeError(settlement_period)
            if settlement_period >= 5:
                offset = -timedelta(hours=1)
            if settlement_period in [5, 6]:
                fold = 1
        else:
            if not 1 <= settlement_period <= 46:
                raise SpringClockChangeError(settlement_period)
            if settlement_period >= 3:
                offset = timedelta(hours=1)
    elif not 1 <= settlement_period <= 48:
        raise SettlementPeriodInputError(settlement_period)
    t0 = datetime.combine(settlement_date, time.min, GB_TIMEZONE)
    sp_ts = t0 + timedelta(minutes=30 * (settlement_period - 1))
    return (sp_ts + offset).replace(fold=fold)
