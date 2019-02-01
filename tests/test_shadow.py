#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `shadow` package."""

import pytest

from click.testing import CliRunner

from shadow.shadow import Shadow
from shadow import cli


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'Usage: main ' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert 'Console script for shadow.' in help_result.output


def test_cli_sim():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main, ['sim'])
    assert result.exit_code == 0
    assert 'Using current working directory.' in result.output


def test_cli_fax():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main, ['fax'])
    assert result.exit_code == 0
    assert 'Using current working directory.' in result.output


def test_cli_clean():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main, ['clean'])
    assert result.exit_code == 0
    assert 'Using current working directory.' in result.output
