#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `shadow` package."""

import pytest

from click.testing import CliRunner

from shadow import shadow
from shadow import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/karma0/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


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
    assert 'Using current working directory' in result.output


def test_cli_fax():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main, ['fax'])
    assert result.exit_code == 0
    assert 'Using current working directory' in result.output


def test_cli_clean():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main, ['clean'])
    assert result.exit_code == 0
    assert 'Using current working directory' in result.output
