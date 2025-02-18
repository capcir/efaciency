# efaciency

![Tests](https://github.com/github/docs/actions/workflows/test.yml/badge.svg)
![PyPi](https://img.shields.io/pypi/v/efaciency)
![Coverage](https://img.shields.io/badge/coverage-100-green)

A package to simplify working with [EFA](https://en.wikipedia.org/wiki/Electricity_Forward_Agreement) blocks and settlement periods in the GB electricity trading system.

## Installation

This package can be installed via pip:

```bash
$ pip install efaciency
```

## Examples

### Settlement periods

Get the starting timestamp for a settlement period.

```python
>>> from datetime import date, datetime
>>> import efaciency

>>> efaciency.sp.to_ts(settlement_period=4)  # defaults to today as settlement date
datetime.datetime(2025, 2, 18, 1, 30, tzinfo=<DstTzInfo 'Europe/London' GMT0:00:00 STD>)

>>> efaciency.sp.to_ts(settlement_period=13, settlement_date=date(2025, 5, 23))
datetime.datetime(2025, 5, 23, 6, 0, tzinfo=<DstTzInfo 'Europe/London' BST+1:00:00 DST>)
```

You can also get the settlement for a given timestamp:

```python
>>> efaciency.sp.from_ts(ts=datetime(2025, 1, 12, 17, 30))
36
```

### EFA blocks

Get the starting and ending timestamp for an EFA block.

```python
>>> from datetime import date, datetime
>>> import efaciency

>>> efaciency.block.to_start_ts(efa_block=3)  # defaults to today as EFA date
datetime.datetime(2025, 2, 18, 7, 0, tzinfo=<DstTzInfo 'Europe/London' GMT0:00:00 STD>)

>>> efaciency.block.to_start_ts(efa_block=1, efa_date=date(2025, 5, 23))
datetime.datetime(2025, 5, 22, 23, 0, tzinfo=<DstTzInfo 'Europe/London' BST+1:00:00 DST>)
```

You can also get the EFA block for a given timestamp:

```python
>>> efaciency.block.from_ts(ts=datetime(2025, 1, 12, 17, 30))
5
```

### What about clock change?

If no timezone is provided, `efaciency` always assumes `Europe/London` timezone.

On clock change days, a tz-aware datetime must be passed or the `fold` [parameter](https://docs.python.org/3/library/datetime.html#datetime.datetime.fold) must be used.

```python
>>> efaciency.sp.from_ts(datetime(2025, 10, 26, 1))
3

>>> efaciency.sp.from_ts(datetime(2025, 10, 26, 1).replace(fold=1))
5
```

## Contribution

Please make a pull request or log an issue on GitHub.

## License

Code is released as free software under the MIT License (see `LICENSE` file).
