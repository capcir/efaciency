"""Command-line interface."""

import argparse
from collections.abc import Sequence
from datetime import datetime, time

import efaciency
from efaciency.utils import GB_TIMEZONE


def parse_args(args: Sequence[str] | None = None) -> argparse.Namespace:
    """Arguments parser for CLI."""
    parser = argparse.ArgumentParser(
        prog="efaciency",
        description="CLI tool for EFA blocks and settlement periods.",
    )
    subparsers = parser.add_subparsers()
    sp_parser = subparsers.add_parser("sp", help="Get the time of a settlement period.")
    sp_parser.add_argument("settlement_period", type=int)
    efa_parser = subparsers.add_parser("efa", help="Get the start and end time of an EFA block.")
    efa_parser.add_argument("efa_block", type=int)
    time_parser = subparsers.add_parser("time", help="Get the SP and EFA block of a time.")
    time_parser.add_argument("time", type=lambda s: time.fromisoformat(s))
    return parser.parse_args(args=args)


def cli(args: Sequence[str] | None = None) -> None:
    """CLI definition."""
    args = parse_args(args)
    msg = "Welcome to efaciency CLI! Run `efaciency --help` for more info."
    if "settlement_period" in args:
        ts = efaciency.sp.to_ts(settlement_period=args.settlement_period)
        msg = f"SP {args.settlement_period} - {ts.strftime('%H:%M')}"
    elif "efa_block" in args:
        start_ts = efaciency.block.to_start_ts(efa_block=args.efa_block)
        end_ts = efaciency.block.to_end_ts(efa_block=args.efa_block)
        msg = f"EFA {args.efa_block} - {start_ts.strftime('%H:%M')} to {end_ts.strftime('%H:%M')}"
    elif "time" in args:
        period = efaciency.sp.from_ts(
            ts := datetime.combine(datetime.now(GB_TIMEZONE).date(), args.time, GB_TIMEZONE)
        )
        efa = efaciency.block.from_ts(ts)
        msg = f"{args.time.strftime('%H:%M')} - SP {period} EFA {efa}"
    print(msg)  # noqa: T201
