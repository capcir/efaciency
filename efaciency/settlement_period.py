"""efaciency settlement_period"""

from datetime import date, datetime, timedelta
from typing import List

from efaciency.utils import (
    convert_to_local,
    get_efa_block,
    get_efa_date,
    get_settlement_date,
    get_settlement_period,
    get_ts,
)


class SettlementPeriod:
    def __init__(
        self,
        settlement_date: date = None,
        settlement_period: int = None,
        ts: datetime = None,
    ):
        """A settlement period object with all info regarding the corresponding half hour.

        Keyword Arguments:
            settlement_date -- settlement date (default: {None})
            settlement_period -- settlement period (default: {None})
            ts -- half hour datetime (default: {None})
        """
        self.settlement_date = settlement_date
        self.settlement_period = settlement_period
        self.ts = ts
        if self.ts is not None:
            self.ts = convert_to_local(self.ts)
        self.efa_date: date
        self.efa_block: int
        self.calculate()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self) -> str:
        return (
            f"SettlementPeriod(ts={self.ts.strftime('%Y-%m-%dT%H:%M')}, "
            + f"settlement_date={self.settlement_date}, "
            + f"settlement_period={self.settlement_period}, "
            + f"efa_date={self.efa_date}, "
            + f"efa_block={self.efa_block})"
        )

    def calculate(self):
        """Set all attributes based on __init__ args."""
        if self.ts is not None:
            self.settlement_date = get_settlement_date(self.ts)
            self.settlement_period = get_settlement_period(self.ts)
            self.efa_date = get_efa_date(self.ts)
            self.efa_block = get_efa_block(self.ts)
        elif self.settlement_date is not None and self.settlement_period is not None:
            self.ts = get_ts(self.settlement_date, self.settlement_period)
            self.efa_date = get_efa_date(self.ts)
            self.efa_block = get_efa_block(self.ts)


def settlement_period_range(
    from_efa_date: date, to_efa_date: date, inclusive: bool = True
) -> List[SettlementPeriod]:
    """Create a half-hourly range of settlement periods between two EFA dates.

    Arguments:
        from_efa_date -- from EFA date
        to_efa_date -- to EFA date

    Keyword Arguments:
        inclusive -- include to_efa_date in range (default: {True})

    Returns:
        list of settlement periods
    """
    start = convert_to_local(
        datetime.combine(from_efa_date, datetime.min.time()) - timedelta(hours=1)
    )
    if inclusive:
        end = convert_to_local(
            datetime.combine(to_efa_date, datetime.min.time()) + timedelta(hours=23)
        )
    else:
        end = convert_to_local(
            datetime.combine(to_efa_date, datetime.min.time()) - timedelta(hours=1)
        )
    ts_list = [
        start + timedelta(minutes=i * 30)
        for i in range(0, int((end - start).total_seconds() / 1800))
    ]
    return [SettlementPeriod(ts=ts) for ts in ts_list]
