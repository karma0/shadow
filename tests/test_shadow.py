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
    assert 'Console script for shadow.' in help_result.output
    assert help_result.exit_code == 0


def test_cli_sim(tmpdir):
    """Test the CLI."""
    tmpfile = tmpdir.join("test.txt.tpl")
    tmpfile.write('asht {{test}}\n')

    runner = CliRunner()
    result = runner.invoke(cli.main, ['sim', str(tmpfile)])
    assert f"Generating template: {str(tmpfile)}" in result.output
    assert result.exit_code == 0


def test_cli_fax(tmpdir):
    """Test the CLI."""
    tmpsource = tmpdir.join('test.txt.tpl')
    tmpsource.write('asht {{test}}\n')
    tmpdest = tmpdir.join('test.txt')

    runner = CliRunner()
    result = runner.invoke(cli.main, ['fax', '-C', '{"test": "thsa"}', str(tmpsource)])
    assert tmpdest.read() == 'asht thsa'
    assert result.exit_code == 0


def test_cli_clean(tmpdir):
    """Test the CLI."""
    tmpsource = tmpdir.join('test.txt.tpl')
    tmpsource.write('asht {{test}}\n')
    tmpdest = tmpdir.join('test.txt')

    runner = CliRunner()
    result = \
        runner.invoke(cli.main,
                ['fax', '-C', '{"test": "thsa"}', str(tmpsource)])
    assert tmpdest.read() == 'asht thsa'
    assert result.exit_code == 0

    runner = CliRunner()
    result = runner.invoke(cli.main, ['clean', str(tmpsource)])
    assert f"Cleaning generated file: {str(tmpdest)}" in result.output
    assert result.exit_code == 0

    assert tmpsource.exists()
    assert not tmpdest.exists()
