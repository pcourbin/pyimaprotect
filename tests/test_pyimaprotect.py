#!/usr/bin/env python

"""Tests for `pyimaprotect` package."""
from click.testing import CliRunner

from pyimaprotect import IMAProtect
from pyimaprotect import cli
import jsonschema
import json
import os
from dotenv import load_dotenv
import logging

_LOGGER = logging.getLogger(__name__)
load_dotenv()

IMA_PASSWORD = os.environ.get("IMA_PASSWORD", "")
IMA_USERNAME = os.environ.get("IMA_USERNAME", "")


def test_json_schema():
    """Test JSONSchema return by IMA Protect API."""
    if (IMA_PASSWORD != ""):
        ima = IMAProtect(IMA_USERNAME, IMA_PASSWORD)
        jsoninfo = ima.get_all_info()
        with open('./tests/jsonschema_imaprotect.json', 'r') as schema_file:
            schema_data = schema_file.read()
        schema_json = json.loads(schema_data)

        try:
            jsonschema.validate(instance=jsoninfo, schema=schema_json)
            jsonschema_validate = True
        except jsonschema.exceptions.ValidationError:
            jsonschema_validate = False
        assert jsonschema_validate
    else:
        _LOGGER.warning("""No login/password defined in environement variable for IMA Protect Alarm.
Test 'jsonschema' not started.""")


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'pyimaprotect.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
