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
    time_parser.add_argument("time", type=time.fromisoformat)
    return parser.parse_args(args=args)


def cli(args: Sequence[str] | None = None) -> None:
    """CLI definition."""
    parsed_args = parse_args(args)
    msg = "Welcome to efaciency CLI! Run `efaciency --help` for more info."
    if "settlement_period" in parsed_args:
        ts = efaciency.sp.to_ts(settlement_period=parsed_args.settlement_period)
        msg = f"SP {parsed_args.settlement_period} - {ts.strftime('%H:%M')}"
    elif "efa_block" in parsed_args:
        start_ts = efaciency.block.to_start_ts(efa_block=parsed_args.efa_block)
        end_ts = efaciency.block.to_end_ts(efa_block=parsed_args.efa_block)
        start_time = start_ts.strftime("%H:%M")
        end_time = end_ts.strftime("%H:%M")
        msg = f"EFA {parsed_args.efa_block} - {start_time} to {end_time}"
    elif "time" in parsed_args:
        period = efaciency.sp.from_ts(
            ts := datetime.combine(datetime.now(GB_TIMEZONE).date(), parsed_args.time, GB_TIMEZONE)
        )
        efa = efaciency.block.from_ts(ts)
        msg = f"{parsed_args.time.strftime('%H:%M')} - SP {period} EFA {efa}"
    print(msg)  # noqa: T201
