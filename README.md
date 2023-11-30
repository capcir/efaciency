# efaciency

![Tests](https://github.com/github/docs/actions/workflows/test.yml/badge.svg)
![PyPi](https://img.shields.io/pypi/v/efaciency)


A package to simplify working with [EFA](https://en.wikipedia.org/wiki/Electricity_Forward_Agreement) blocks and settlement periods in the GB electricity trading system.

## Installation

This package can be installed via pip:
```bash
$ pip install efaciency
```

## Examples

### Settlement periods

Define a settlement period and get the corresponding half-hour datetime.
```python
>>> from datetime import date
>>> from efaciency import SettlementPeriod
>>> sp = SettlementPeriod(settlement_date=date(2023, 7, 1), settlement_period=24)
>>> sp["ts"]
datetime.datetime(2023, 7, 1, 11, 30, tzinfo=<DstTzInfo 'Europe/London' BST+1:00:00 DST>)
```

Get the corresponding EFA information and settlement information for a given timestamp.
```python
>>> from datetime import datetime
>>> from efaciency import SettlementPeriod
>>> sp = SettlementPeriod(ts=datetime(2023, 7, 1, 11, 30))
>>> sp
{
    'settlement_date': datetime.date(2023, 7, 1)
    'settlement_period': 24,
    'ts': datetime.datetime(2023, 7, 1, 11, 30, tzinfo=<DstTzInfo 'Europe/London' BST+1:00:00 DST>),
    'efa_date': datetime.date(2023, 7, 1),
    'efa_block': 4,
}
```

Create half-hourly range for all SPs in between two dates.
```python
>>> from datetime import date
>>> from efaciency import settlement_period_range
>>> sp_range = settlement_period_range(
...     from_efa_date=date(2023, 7, 1),
...     to_efa_date=date(2023, 7, 2),
... )
>>> sp_range[0]
{
    'settlement_date': datetime.date(2023, 6, 30)
    'settlement_period': 47,
    'ts': datetime.datetime(2023, 6, 30, 23, 0, tzinfo=<DstTzInfo 'Europe/London' BST+1:00:00 DST>),
    'efa_date': datetime.date(2023, 7, 1),
    'efa_block': 1
}
```

### EFA blocks

Define EFA blocks and get the corresponding start and end datetimes.
```python
>>> from datetime import date
>>> from efaciency import EFABlock
>>> efa = EFABlock(efa_date=date(2023, 7, 1), efa_block=3)
>>> efa["start_ts"].strftime("%Y-%m-%d %H:%M")
'2023-07-01 07:00'
>>> efa["end_ts"].strftime("%Y-%m-%d %H:%M")
'2023-07-01 11:00'
```

Create a range of all EFA blocks between two dates.
```python
>>> from datetime import date
>>> from efaciency import efa_block_range
>>> efa_range = efa_block_range(date(2023, 7, 1), date(2023, 7, 2))
>>> efa_range[0]
{
    'efa_date': datetime.date(2023, 7, 1),
    'efa_block': 1,
    'start_ts': datetime.datetime(2023, 6, 30, 23, 0, tzinfo=<DstTzInfo 'Europe/London' BST+1:00:00 DST>),
    'end_ts': datetime.datetime(2023, 7, 1, 3, 0, tzinfo=<DstTzInfo 'Europe/London' BST+1:00:00 DST>),
}
```

## Contribution

Please make a pull request or log an issue on GitHub.

## License

Code is released as free software under the MIT License (see `LICENSE` file).
