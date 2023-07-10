"""efaciency settlement_period"""

from datetime import date, datetime, timedelta
from typing import List, Dict, Any

from efaciency.utils import (
    convert_to_local,
    convert_to_utc,
    get_efa_block,
    get_efa_date,
    get_settlement_date,
    get_settlement_period,
    get_ts,
)


class SettlementPeriod(Dict[str, Any]):
    def __init__(
        self,
        settlement_date: date = None,
        settlement_period: int = None,
        ts: datetime = None,
        efa_date: date = None,
        efa_block: date = None,
    ):
        """A settlement period object with all info regarding the corresponding half hour.

        Keyword Arguments:
            settlement_date -- settlement date (default: {None})
            settlement_period -- settlement period (default: {None})
            ts -- half hour datetime (default: {None})
        """
        super().__init__(
            settlement_date=settlement_date,
            settlement_period=settlement_period,
            ts=ts,
            efa_date=efa_date,
            efa_block=efa_block,
        )
        if self.__getitem__("ts") is not None:
            self.__setitem__("ts", convert_to_local(self.__getitem__("ts")))
        self._calculate()

    def _calculate(self):
        """Calculate any missing items based on provided arguments."""
        if self.__getitem__("ts") is not None:
            self.__setitem__(
                "settlement_date", get_settlement_date(self.__getitem__("ts"))
            )
            self.__setitem__(
                "settlement_period", get_settlement_period(self.__getitem__("ts"))
            )
            self.__setitem__("efa_date", get_efa_date(self.__getitem__("ts")))
            self.__setitem__("efa_block", get_efa_block(self.__getitem__("ts")))
        elif (
            self.__getitem__("settlement_date") is not None
            and self.__getitem__("settlement_period") is not None
        ):
            self.__setitem__(
                "ts",
                get_ts(
                    self.__getitem__("settlement_date"),
                    self.__getitem__("settlement_period"),
                ),
            )
            self.__setitem__("efa_date", get_efa_date(self.__getitem__("ts")))
            self.__setitem__("efa_block", get_efa_block(self.__getitem__("ts")))


def settlement_period_range(
    from_efa_date: date = None,
    to_efa_date: date = None,
    from_settlement_date: date = None,
    to_settlement_date: date = None,
    inclusive: bool = True,
) -> List[SettlementPeriod]:
    """Create a half-hourly range of settlement periods between two EFA or settlement dates.

    Arguments:
        from_efa_date -- from EFA date (default: {None})
        to_efa_date -- to EFA date (default: {None})
        from_settlement_date -- from settlement date (default: {None})
        to_settlement_date -- to settlement date (default: {None})

    Keyword Arguments:
        inclusive -- include to date in range (default: {True})

    Returns:
        list of settlement periods
    """
    if all(
        arg is None
        for arg in [
            from_efa_date,
            to_efa_date,
            from_settlement_date,
            to_settlement_date,
        ]
    ):
        raise ValueError("need to provide a start and end EFA or settlement date")
    if from_efa_date is not None:
        assert to_efa_date is not None
        assert from_settlement_date is None
        assert to_settlement_date is None
        start = datetime.combine(from_efa_date, datetime.min.time()) - timedelta(
            hours=1
        )
        if inclusive:
            end = datetime.combine(to_efa_date, datetime.min.time()) + timedelta(
                hours=23
            )
        else:
            end = datetime.combine(to_efa_date, datetime.min.time()) - timedelta(
                hours=1
            )
    if from_settlement_date is not None:
        assert to_settlement_date is not None
        assert from_efa_date is None
        assert to_efa_date is None
        start = datetime.combine(from_settlement_date, datetime.min.time())
        if inclusive:
            end = datetime.combine(to_settlement_date, datetime.min.time()) + timedelta(
                hours=24
            )
        else:
            end = datetime.combine(to_settlement_date, datetime.min.time())
    start = convert_to_utc(convert_to_local(start))
    end = convert_to_utc(convert_to_local(end))
    ts_list = [
        start + timedelta(minutes=i * 30)
        for i in range(0, int((end - start).total_seconds() / 1800))
    ]
    return [SettlementPeriod(ts=ts) for ts in ts_list]
