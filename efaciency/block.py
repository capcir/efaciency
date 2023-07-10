"""efaciency block"""

from datetime import date, datetime, timedelta
from typing import List, Dict, Any

from efaciency.utils import (
    convert_to_local,
    get_efa_block,
    get_efa_date,
    get_efa_start_time,
    get_efa_end_time,
)


class EFABlock(Dict[str, Any]):
    def __init__(
        self,
        efa_date: date = None,
        efa_block: date = None,
        start_ts: datetime = None,
        end_ts: datetime = None,
    ):
        """An EFA block object with all info regarding the corresponding block.

        Keyword Arguments:
            efa_date -- EFA date (default: {None})
            efa_block -- EFA block number (default: {None})
            start_ts -- start of the EFA block datetime (default: {None})
            end_ts -- end of the EFA block datetime (default: {None})
        """
        super().__init__(
            efa_date=efa_date,
            efa_block=efa_block,
            start_ts=start_ts,
            end_ts=end_ts,
        )
        for key in ["start_ts", "end_ts"]:
            if self.__getitem__(key) is not None:
                self.__setitem__(key, convert_to_local(self.__getitem__(key)))
        self._calculate()

    def _calculate(self):
        """Calculate any missing items based on provided arguments."""
        if (
            self.__getitem__("efa_date") is not None
            and self.__getitem__("efa_block") is not None
        ):
            self.__setitem__(
                "start_ts",
                get_efa_start_time(
                    self.__getitem__("efa_date"),
                    self.__getitem__("efa_block"),
                ),
            )
            self.__setitem__(
                "end_ts",
                get_efa_end_time(
                    self.__getitem__("efa_date"),
                    self.__getitem__("efa_block"),
                ),
            )
        elif self.__getitem__("start_ts") is not None:
            self.__setitem__("efa_date", get_efa_date(self.__getitem__("start_ts")))
            self.__setitem__("efa_block", get_efa_block(self.__getitem__("start_ts")))
            self.__setitem__(
                "end_ts",
                get_efa_end_time(
                    self.__getitem__("efa_date"),
                    self.__getitem__("efa_block"),
                ),
            )


def efa_block_range(
    from_efa_date: date, to_efa_date: date, inclusive: bool = True
) -> List[EFABlock]:
    """Create a range of EFA blocks between two EFA dates.

    Arguments:
        from_efa_date -- from EFA date
        to_efa_date -- to EFA date

    Keyword Arguments:
        inclusive -- include to_efa_date in range (default: {True})

    Returns:
        list of settlement periods
    """
    start = datetime.combine(from_efa_date, datetime.min.time()) - timedelta(hours=1)
    if inclusive:
        end = datetime.combine(to_efa_date, datetime.min.time()) + timedelta(hours=23)
    else:
        end = datetime.combine(to_efa_date, datetime.min.time()) - timedelta(hours=1)
    ts_list = [
        start + timedelta(hours=i * 4)
        for i in range(0, int((end - start).total_seconds() / (3600 * 4)))
    ]
    return [EFABlock(start_ts=ts) for ts in ts_list]
