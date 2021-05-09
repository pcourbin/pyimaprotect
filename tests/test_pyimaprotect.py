#!/usr/bin/env python
"""Tests for `pyimaprotect` package."""
import logging
import os
from pyimaprotect import cli
from pyimaprotect import IMAProtect
from pyimaprotect.exceptions import IMAProtectConnectError

from click.testing import CliRunner
from dotenv import load_dotenv

_LOGGER = logging.getLogger(__name__)
load_dotenv()

IMA_PASSWORD = os.environ.get("IMA_PASSWORD", "")
IMA_USERNAME = os.environ.get("IMA_USERNAME", "")


def test_connexion():
    """Test JSONSchema return by IMA Protect API."""
    connected = True
    if IMA_PASSWORD != "":
        ima = IMAProtect(IMA_USERNAME, IMA_PASSWORD)
        try:
            imastatus = ima.get_status()
        except IMAProtectConnectError:
            connected = False
        except:
            connected = False

        assert connected
        assert imastatus is not None
        assert imastatus >= -1 and imastatus <= 3
    else:
        _LOGGER.warning(
            """No login/password defined in environement variable for IMA Protect Alarm.
Test 'connexion' not started."""
        )


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert "pyimaprotect.cli.main" in result.output
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help  Show this message and exit." in help_result.output
