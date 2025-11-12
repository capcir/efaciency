import argparse
from datetime import time

import pytest

from efaciency import cli


def test_cli_argument_parser():
    args = cli.parse_args(["sp", "1"])
    assert args.settlement_period == 1
    args = cli.parse_args(["efa", "1"])
    assert args.efa_block == 1
    args = cli.parse_args(["time", "11:00"])
    assert args.time == time(11)


def test_cli_welcome_message(capsys, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(cli, "parse_args", lambda _: argparse.Namespace())
    cli.cli()
    out, error = capsys.readouterr()
    assert out == "Welcome to efaciency CLI! Run `efaciency --help` for more info.\n"
    assert error == ""


def test_cli_sp(capsys, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(cli, "parse_args", lambda _: argparse.Namespace(settlement_period=1))
    cli.cli()
    out, error = capsys.readouterr()
    assert out == "SP 1 - 00:00\n"
    assert error == ""


def test_cli_efa(capsys, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(cli, "parse_args", lambda _: argparse.Namespace(efa_block=1))
    cli.cli()
    out, error = capsys.readouterr()
    assert out == "EFA 1 - 23:00 to 03:00\n"
    assert error == ""


def test_cli_time(capsys, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(cli, "parse_args", lambda _: argparse.Namespace(time=time(0, 0)))
    cli.cli()
    out, error = capsys.readouterr()
    assert out == "00:00 - SP 1 EFA 1\n"
    assert error == ""
