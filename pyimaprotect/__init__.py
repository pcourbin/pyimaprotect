"""Top-level package for pyimaprotect."""

__author__ = """Pierre COURBIN"""
__email__ = "pierre.courbin@gmail.com"
__version__ = "3.0.0"

import requests
import logging
import re
import json
import os
from jsonpath_ng import parse
from .exceptions import IMAProtectConnectError

_LOGGER = logging.getLogger(__name__)


def invert_dict(current_dict: dict):
    return {v: k for k, v in current_dict.items()}


IMA_URL_LOGIN = "https://www.imaprotect.com/fr/client/login_check"
IMA_URL_STATUS = "https://www.imaprotect.com/fr/client/management/status"
IMA_URL_CONTACTLIST = "https://www.imaprotect.com/fr/client/contact/list"
IMA_URL_IMAGES = "https://www.imaprotect.com/fr/client/management/captureList"
RE_ALARM_TOKEN = 'alarm-status ref="myAlarm" data-token="(.*)"'
IMA_CONTACTLIST_JSONPATH = "$..contactList"

STATUS_IMA_TO_NUM = {"off": 0, "partial": 1, "on": 2}
STATUS_NUM_TO_IMA = invert_dict(STATUS_IMA_TO_NUM)
STATUS_NUM_TO_TEXT = {0: "OFF", 1: "PARTIAL", 2: "ON", -1: "UNKNOWN"}


class IMAProtect:
    """Class representing the IMA Protect Alarm and its API"""

    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._session = None
        self._token_status = None

    @property
    def username(self):
        """Return the username."""
        return self._username

    @property
    def status(self) -> int:
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

    @status.setter
    def status(self, status: int):
        self._session_login()
        url = IMA_URL_STATUS
        update_status = {
            "status": STATUS_NUM_TO_IMA.get(status),
            "token": self._token_status,
        }
        response = self._session.post(url, data=update_status)
        if response.status_code != 200:
            _LOGGER.error(
                """Can't change the status, step 'SetStatus'.
                Please, check your logins. You must be able to login on https://www.imaprotect.com."""
            )

    def get_contact_list(self):
        self._session_login()
        url = IMA_URL_CONTACTLIST
        response = self._session.get(url)
        return (
            parse(IMA_CONTACTLIST_JSONPATH).find(json.loads(response.content))[0].value
        )

    def download_images(self, dest: str = "Images/"):
        self._session_login()
        url = IMA_URL_IMAGES
        response = self._session.get(url)
        response_json = json.loads(response.content)
        for camera in response_json:
            current_path = dest + camera["name"]
            os.makedirs(current_path, exist_ok=True)
            for image in camera["images"]:
                r = self._session.get(image, allow_redirects=True)
                if r.status_code == 200:
                    with open(
                        current_path
                        + "/"
                        + camera["type"]
                        + "_"
                        + os.path.basename(image),
                        "wb",
                    ) as f:
                        f.write(r.content)

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
        elif response.status_code == 200:
            token_search = re.findall(RE_ALARM_TOKEN, response.text)
            if len(token_search) > 0:
                self._token_status = token_search[0]
            else:
                self._token_status = None
                _LOGGER.error(
                    """Can't get the token to change the status, step 'Login/TokenStatus'.
                    Please, check your logins. You must be able to login on https://www.imaprotect.com."""
                )
        else:
            self._session = None

        return self._session
