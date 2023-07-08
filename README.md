# efaciency

A package to simplify working with EFA days in the GB electricity trading system.

## Quick start

```python
import efaciency

sp_range = efaciency.settlement_period_range(
    from_efa_date=date(2023, 7, 1),
    to_efa_date=date(2023, 7, 2),
)
```