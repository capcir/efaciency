from datetime import date, datetime

import efaciency


def test_settlement_period_creation():
    sp1 = efaciency.SettlementPeriod(
        settlement_date=date(2023, 7, 1),
        settlement_period=23,
    )
    sp2 = efaciency.SettlementPeriod(ts=datetime(2023, 7, 1, 11))
    assert sp1 == sp2
    assert (
        sp2.__repr__()
        == "SettlementPeriod(ts=2023-07-01T11:00, settlement_date=2023-07-01, settlement_period=23, efa_date=2023-07-01, efa_block=4)"
    )


def test_settlement_period_range():
    spr = efaciency.settlement_period_range(
        from_efa_date=date(2023, 7, 1),
        to_efa_date=date(2023, 7, 2),
    )
    assert len(spr) == 48 * 2
    spr = efaciency.settlement_period_range(
        from_efa_date=date(2023, 7, 1), to_efa_date=date(2023, 7, 2), inclusive=False
    )
    assert len(spr) == 48
