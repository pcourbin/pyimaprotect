"""Top-level package for pyimaprotect."""

__author__ = """Pierre COURBIN"""
__email__ = "pierre.courbin@gmail.com"
__version__ = "2.0.0"

import requests
import logging
from .exceptions import IMAProtectConnectError

_LOGGER = logging.getLogger(__name__)

IMA_URL_LOGIN = "https://www.imaprotect.com/fr/client/login_check"
IMA_URL_STATUS = "https://www.imaprotect.com/fr/client/management/status"

STATUS_IMA_TO_NUM = {"off": 0, "partial": 1, "on": 2}

STATUS_NUM_TO_TEXT = {0: "OFF", 1: "PARTIAL", 2: "ON", -1: "UNKNOWN"}


class IMAProtect:
    """Class representing the IMA Protect Alarm and its API"""

    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._session = None

    @property
    def username(self):
        """Return the username."""
        return self._username

    def get_status(self):
        self._session_login()
        status = -1
        url = IMA_URL_STATUS

        try:
            response = self._session.get(url)
            if response.status_code == 200:
                status = STATUS_IMA_TO_NUM.get(
                    str(response.content.decode().replace('"', ""))
                )
            else:
                _LOGGER.error(
                    "Can't connect to the IMAProtect API. Response code: %d"
                    % (response.status_code)
                )
        except:
            _LOGGER.error(
                "Can't connect/read to the IMAProtect API. Response code: %d"
                % (response.status_code)
            )
            raise IMAProtectConnectError

        return status

    def _session_login(self):
        url = IMA_URL_LOGIN
        login = {"_username": self._username, "_password": self._password}
        self._session = requests.Session()
        response = self._session.post(url, data=login)
        if response.status_code == 400:
            _LOGGER.error(
                """Can't connect to the IMAProtect Website, step 'Login'.
                Please, check your logins. You must be able to login on https://www.imaprotect.com."""
            )
        elif response.status_code != 200:
            self._session = None

        return self._session
