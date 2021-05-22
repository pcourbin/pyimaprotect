#!/usr/bin/env python
"""Tests for `pyimaprotect` package."""
import logging
import os
import shutil
from os import path
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
            imastatus = ima.status
        except IMAProtectConnectError:
            connected = False
        except:
            connected = False

        assert connected
        assert imastatus is not None
        assert imastatus >= -1 and imastatus <= 3
        assert ima.username == IMA_USERNAME
        ima.logout()
    else:
        _LOGGER.warning(
            """No login/password defined in environement variable for IMA Protect Alarm.
Test 'connexion' not started."""
        )


def test_contact_list():
    """Test JSONSchema return by IMA Protect API."""
    if IMA_PASSWORD != "":
        ima = IMAProtect(IMA_USERNAME, IMA_PASSWORD)

        assert len(ima.get_contact_list()) > 0
        ima.logout()
    else:
        _LOGGER.warning(
            """No login/password defined in environement variable for IMA Protect Alarm.
Test 'contact_list' not started."""
        )


def test_images():
    """Test JSONSchema return by IMA Protect API."""
    if IMA_PASSWORD != "":
        ima = IMAProtect(IMA_USERNAME, IMA_PASSWORD)
        ima.download_images()
        assert path.exists("Images/")
        shutil.rmtree("Images/")
        ima.download_images("MyImages/")
        assert path.exists("MyImages/")
        shutil.rmtree("MyImages/")
        assert type(ima.get_images_list()) is dict
        ima.logout()
    else:
        _LOGGER.warning(
            """No login/password defined in environement variable for IMA Protect Alarm.
Test 'contact_list' not started."""
        )


def test_change_status():
    """Test JSONSchema return by IMA Protect API."""
    if IMA_PASSWORD != "":
        ima = IMAProtect(IMA_USERNAME, IMA_PASSWORD)
        current = ima.status
        ima.status = current
        assert ima.status == current
        ima.logout()

    else:
        _LOGGER.warning(
            """No login/password defined in environement variable for IMA Protect Alarm.
Test 'change_status' not started."""
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
