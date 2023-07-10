from datetime import date, datetime

import efaciency


def test_efa_block_creation():
    b1 = efaciency.EFABlock(
        efa_date=date(2023, 7, 1),
        efa_block=3,
    )
    b2 = efaciency.EFABlock(start_ts=datetime(2023, 7, 1, 7))
    assert b1 == b2


def test_efa_block_range():
    ebr = efaciency.efa_block_range(
        from_efa_date=date(2023, 7, 1),
        to_efa_date=date(2023, 7, 2),
    )
    assert len(ebr) == 6 * 2
    ebr = efaciency.efa_block_range(
        from_efa_date=date(2023, 7, 1), to_efa_date=date(2023, 7, 2), inclusive=False
    )
    assert len(ebr) == 6


def test_efa_block_range_spring_dst():
    ebr = efaciency.efa_block_range(
        from_efa_date=date(2023, 3, 26),
        to_efa_date=date(2023, 3, 26),
    )
    assert len(ebr) == 6


def test_efa_block_range_autumn_dst():
    ebr = efaciency.efa_block_range(
        from_efa_date=date(2023, 10, 29),
        to_efa_date=date(2023, 10, 29),
    )
    assert len(ebr) == 6
