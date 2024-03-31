"""Top-level package for pyimaprotect."""

__author__ = """Pierre COURBIN"""
__email__ = "pierre.courbin@gmail.com"
__version__ = "3.1.6"

import requests
import logging
import re
import json
import os
from jsonpath_ng import parse
from datetime import datetime
from .exceptions import IMAProtectConnectError

_LOGGER = logging.getLogger(__name__)


def invert_dict(current_dict: dict):
    return {v: k for k, v in current_dict.items()}


IMA_URL_ROOT = "https://www.imaprotect.com"
IMA_URL_PRELOGIN = IMA_URL_ROOT + "/fr/client/login"
RE_PRELOGIN_TOKEN = 'name="_csrf_token" value="(.*)" *>'
IMA_URL_LOGIN = IMA_URL_ROOT + "/fr/client/login_check"
IMA_URL_LOGOUT = IMA_URL_ROOT + "/fr/client/logout"
IMA_URL_STATUS = IMA_URL_ROOT + "/fr/client/management/status"
IMA_URL_CONTACTLIST = IMA_URL_ROOT + "/fr/client/contact/list"
IMA_URL_IMAGES = IMA_URL_ROOT + "/fr/client/management/captureList"
RE_ALARM_TOKEN = 'alarm-status token="(.*)"'
IMA_CONTACTLIST_JSONPATH = "$..contactList"
IMA_COOKIENAME_EXPIRE = "imainternational"

STATUS_IMA_TO_NUM = {"off": 0, "partial": 1, "on": 2}
STATUS_NUM_TO_IMA = invert_dict(STATUS_IMA_TO_NUM)
STATUS_NUM_TO_TEXT = {0: "OFF", 1: "PARTIAL", 2: "ON", -1: "UNKNOWN"}


class IMAProtect:
    """Class representing the IMA Protect Alarm and its API"""

    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._session = None
        self._token_login = None
        self._token_status = None
        self._expire = datetime.now()

    @property
    def username(self):
        """Return the username."""
        return self._username

    @property
    def status(self) -> int:
        self.login()
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
            raise IMAProtectConnectError(response.status_code, response.text)

        return status

    @status.setter
    def status(self, status: int):
        self.login()
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
        self.login()
        url = IMA_URL_CONTACTLIST
        response = self._session.get(url)
        return (
            parse(IMA_CONTACTLIST_JSONPATH).find(json.loads(response.content))[0].value
        )

    def get_images_list(self):
        capture_list = self._capture_list()
        response = {}
        for camera in capture_list:
            if camera["name"] not in response:
                response[camera["name"]] = []
            image = {}
            image["type"] = camera["type"]
            image["date"] = camera["date"]
            image["images"] = camera["images"]
            response[camera["name"]].append(image)
        return response

    def download_images(self, dest: str = "Images/"):
        capture_list = self._capture_list()
        for camera in capture_list:
            current_path = dest + camera["name"]
            os.makedirs(current_path, exist_ok=True)
            for image in camera["images"]:
                r = self._session.get(IMA_URL_ROOT + image, allow_redirects=True)
                if r.status_code == 200:
                    with open(
                        current_path
                        + "/"
                        + camera["type"]
                        + "_"
                        + os.path.splitext(os.path.basename(image))[0]
                        + ".jpg",
                        "wb",
                    ) as f:
                        f.write(r.content)

    def _capture_list(self) -> dict:
        self.login()
        url = IMA_URL_IMAGES
        response = self._session.get(url)
        response_json = json.loads(response.content)
        return response_json

    def login(self, force: bool = False):
        if force or self._session is None or self._expire < datetime.now():
            self._session = requests.Session()

            url = IMA_URL_PRELOGIN
            response = self._session.get(IMA_URL_PRELOGIN)
            if response.status_code == 200:
                token_search = re.findall(
                    RE_PRELOGIN_TOKEN,
                    re.sub(" +", " ", response.text),
                )
                if len(token_search) > 0:
                    self._token_login = token_search[0]
                else:
                    self._token_login = None
                    _LOGGER.error(
                        """Can't get the token to login, step 'Login/TokenLogin'.
                        Please, contact the developer."""
                    )
            else:
                self._session = None
                raise IMAProtectConnectError(response.status_code, response.text)

            if self._token_login is not None:
                url = IMA_URL_LOGIN
                login = {
                    "_username": self._username,
                    "_password": self._password,
                    "_csrf_token": self._token_login,
                }

                response = self._session.post(url, data=login)
                for cookie in self._session.cookies:
                    if cookie.name == IMA_COOKIENAME_EXPIRE:
                        self._expire = datetime.fromtimestamp(cookie.expires)

                if response.status_code == 400:
                    _LOGGER.error(
                        """Can't connect to the IMAProtect Website, step 'Login'.
                        Please, check your logins. You must be able to login on https://www.imaprotect.com."""
                    )
                    raise IMAProtectConnectError(response.status_code, response.text)
                elif response.status_code == 200:
                    token_search = re.findall(RE_ALARM_TOKEN, response.text)
                    if len(token_search) > 0:
                        self._token_status = token_search[0]
                    else:
                        self._token_status = None
                        _LOGGER.error(
                            """Can't get the token to read the status, step 'Login/TokenStatus'.
                            Please, check your logins. You must be able to login on https://www.imaprotect.com."""
                        )
                else:
                    self._session = None
                    raise IMAProtectConnectError(response.status_code, response.text)

        return self._session

    def logout(self):
        self.login()
        url = IMA_URL_LOGOUT
        response = self._session.get(url)
        if response.status_code == 200:
            self._session = None
        else:
            _LOGGER.error(
                """Can't disconnect to the IMAProtect Website, step 'Logout'."""
            )
            raise IMAProtectConnectError(response.status_code, response.text)
