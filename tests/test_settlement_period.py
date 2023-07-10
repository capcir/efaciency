from datetime import date, datetime

import pytest

import efaciency

STR_FORMAT = "%Y-%m-%d %H:%M:%S%z"


def test_settlement_period_creation():
    sp1 = efaciency.SettlementPeriod(
        settlement_date=date(2023, 7, 1),
        settlement_period=23,
    )
    sp2 = efaciency.SettlementPeriod(ts=datetime(2023, 7, 1, 11))
    assert sp1 == sp2


def test_settlement_period_creation_spring_dst():
    sp = efaciency.SettlementPeriod(
        settlement_date=date(2023, 3, 26),
        settlement_period=2,
    )
    assert sp["ts"].strftime(STR_FORMAT) == "2023-03-26 00:30:00+0000"
    sp = efaciency.SettlementPeriod(
        settlement_date=date(2023, 3, 26),
        settlement_period=3,
    )
    assert sp["ts"].strftime(STR_FORMAT) == "2023-03-26 02:00:00+0100"


def test_settlement_period_creation_autumn_dst():
    sp = efaciency.SettlementPeriod(
        settlement_date=date(2023, 10, 29),
        settlement_period=3,
    )
    assert sp["ts"].strftime(STR_FORMAT) == "2023-10-29 01:00:00+0100"
    sp = efaciency.SettlementPeriod(
        settlement_date=date(2023, 10, 29),
        settlement_period=5,
    )
    assert sp["ts"].strftime(STR_FORMAT) == "2023-10-29 01:00:00+0000"


def test_settlement_period_range_from_efa_dates():
    spr = efaciency.settlement_period_range(
        from_efa_date=date(2023, 7, 1),
        to_efa_date=date(2023, 7, 2),
    )
    assert len(spr) == 48 * 2
    spr = efaciency.settlement_period_range(
        from_efa_date=date(2023, 7, 1), to_efa_date=date(2023, 7, 2), inclusive=False
    )
    assert len(spr) == 48


def test_settlement_period_range_error():
    with pytest.raises(ValueError) as e:
        efaciency.settlement_period_range()
    assert "need to provide a start and end EFA or settlement date" in str(e)


def test_settlement_period_range_from_settlement_dates():
    spr = efaciency.settlement_period_range(
        from_settlement_date=date(2023, 7, 1),
        to_settlement_date=date(2023, 7, 2),
    )
    assert len(spr) == 48 * 2
    spr = efaciency.settlement_period_range(
        from_settlement_date=date(2023, 7, 1),
        to_settlement_date=date(2023, 7, 2),
        inclusive=False,
    )
    assert len(spr) == 48


def test_settlement_period_range_spring_dst():
    spr = efaciency.settlement_period_range(
        from_settlement_date=date(2023, 3, 26),
        to_settlement_date=date(2023, 3, 26),
    )
    assert len(spr) == 46


def test_settlement_period_range_autumn_dst():
    spr = efaciency.settlement_period_range(
        from_settlement_date=date(2023, 10, 29),
        to_settlement_date=date(2023, 10, 29),
    )
    assert len(spr) == 50
