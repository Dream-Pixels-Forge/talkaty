"""Tests for talkaty CLI."""

from typer.testing import CliRunner
from talkaty.cli import app


def test_help():
    runner = CliRunner()
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "talkaty" in result.output


def test_voices():
    runner = CliRunner()
    result = runner.invoke(app, ["voices"])
    assert result.exit_code == 0
    # Rich tables don't render rows in non-TTY mode; assert header/title only.
    assert "talkaty voices" in result.output


def test_personas():
    runner = CliRunner()
    result = runner.invoke(app, ["personas"])
    assert result.exit_code == 0
    assert "talkaty voices" in result.output
