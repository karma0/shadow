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


def _test_cli_sim(tmpdir):
    """Test the CLI."""
    tmpfile = tmpdir.join("test.txt.tpl")
    runner = CliRunner()
    result = runner.invoke(cli.main, ['sim', 'test.txt.tpl'])
    #assert result.exit_code == 0
    assert 'Using current working directory.' in result.output


def test_cli_fax(tmpdir):
    """Test the CLI."""
    tmpsource = tmpdir.join('test.txt.tpl')
    print(f"{tmpsource}")
    tmpsource.write('asht {{test}}\n')
    tmpdest = tmpdir.join('test.txt')
    print(f"{tmpdest}")


    runner = CliRunner()
    result = runner.invoke(cli.main, ['fax', tmpsource])
    assert result == ''
    #assert result.exit_code == 0
    assert tmpdest.read() == 'asht '


def _test_cli_clean(tmpdir):
    """Test the CLI."""
    tmpfile = tmpdir.join("test.txt.tpl")
    runner = CliRunner()
    result = runner.invoke(cli.main, ['clean'])
    assert result.exit_code == 0
    assert 'Using current working directory.' in result.output
