"""Top-level package for pyimaprotect."""

__author__ = """Pierre COURBIN"""
__email__ = "pierre.courbin@gmail.com"
__version__ = "3.2.0"

import requests
import logging
import re
import json
import os
from jsonpath_ng import parse
from datetime import datetime
from .exceptions import IMAProtectConnectError

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

_LOGGER = logging.getLogger(__name__)

def invert_dict(current_dict: dict):
    return {v: k for k, v in current_dict.items()}

USER_AGENT = 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'

IMA_URL_ROOT = "https://www.imaprotect.com"
IMA_URL_PRELOGIN = IMA_URL_ROOT + "/fr/client/login"
RE_PRELOGIN_TOKEN = 'name="_csrf_token" value="(.*)" *>'
IMA_URL_LOGIN = IMA_URL_ROOT + "/fr/client/login_check"
IMA_URL_LOGOUT = IMA_URL_ROOT + "/fr/client/logout"
IMA_URL_STATUS = IMA_URL_ROOT + "/fr/client/management/status"
IMA_URL_CONTACTLIST = IMA_URL_ROOT + "/fr/client/contract"
IMA_URL_IMAGES = IMA_URL_ROOT + "/fr/client/management/captureList"
RE_ALARM_TOKEN = 'alarm-status token="(.*)"'
IMA_CONTACTLIST_JSONPATH = "$..persons"
IMA_COOKIENAME_EXPIRE = "imainternational"
IMA_URL_CHANGE_CONTRACT = IMA_URL_ROOT + "/fr/client/change-contract/{}"

STATUS_IMA_TO_NUM = {"off": 0, "partial": 1, "on": 2}
STATUS_NUM_TO_IMA = invert_dict(STATUS_IMA_TO_NUM)
STATUS_NUM_TO_TEXT = {0: "OFF", 1: "PARTIAL", 2: "ON", -1: "UNKNOWN"}


class IMAProtect:
    """Class representing the IMA Protect Alarm and its API"""

    def __init__(self, username, password, contract_number=None):
        self._username = username
        self._password = password
        self._contract_number = contract_number
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

            options = Options()
            options.add_argument("--headless")  # Remove this if you want to see the browser (Headless makes the Firefox driver not have a GUI)
            options.add_argument("--window-size=1920,1080")
            options.add_argument(f'--user-agent={USER_AGENT}')
            options.add_argument('--no-sandbox')
            options.add_argument("--disable-extensions")

            driver = webdriver.Firefox(options=options)

            try:
                driver.get(IMA_URL_PRELOGIN)
                try:
                    elem = driver.find_element(By.NAME, "_csrf_token")
                    self._token_login = elem.get_attribute("value")
                    if not self._token_login:
                        _LOGGER.error("CSRF token found but without value on the pre-login page.")
                except Exception:
                    self._token_login = None
                    _LOGGER.error("CSRF token not found on the pre-login page. Check that the page loaded correctly or increase the timeout.")

                username = driver.find_element(By.NAME, "_username")
                username.send_keys(self._username)

                password = driver.find_element(By.NAME, "_password")
                password.send_keys(self._password)

                # submit the login form
                driver.find_element(By.CLASS_NAME, "form-signin").submit()

                # wait for URL to change with 15 seconds timeout
                WebDriverWait(driver, 15).until(EC.url_changes(IMA_URL_PRELOGIN))

                if (driver.current_url == IMA_URL_PRELOGIN) or (self._token_login is None):
                    raise IMAProtectConnectError(400, "Login failed. Please check your credentials. Can't connect to the IMAProtect Website, step 'Login'. Please, check your logins. You must be able to login on https://www.imaprotect.com.")

                # Navigate to change contract page if contract number is provided
                if self._contract_number is not None:
                    driver.get(IMA_URL_CHANGE_CONTRACT.format(self._contract_number))

                # Create a requests session and transfer cookies from Selenium
                self._session = requests.Session()
                headers = {
                    "User-Agent": USER_AGENT,
                }
                self._session.headers.update(headers)
                for cookie in driver.get_cookies():
                    c = {cookie["name"]: cookie["value"]}
                    self._session.cookies.update(c)
                    if cookie["name"] == IMA_COOKIENAME_EXPIRE:
                        try:
                            self._expire = datetime.fromtimestamp(cookie["expiry"])
                        except Exception as e:
                            _LOGGER.error(f"Error parsing session expiry: {e}")

                # Get the status token from the page source
                response = self._session.get(driver.current_url)
                if (response.status_code == 200):
                    token_search = re.findall(RE_ALARM_TOKEN, response.text)
                    if len(token_search) > 0:
                        self._token_status = token_search[0]
                    else:
                        self._token_status = None
                        _LOGGER.error(
                            """Can't get the token to read the status, step 'Login/TokenStatus'.
                            Please, check your logins. You must be able to login on https://www.imaprotect.com."""
                        )
            except Exception as e:
                self._session = None
                raise IMAProtectConnectError(0, str(e))
            finally:
                try:
                    driver.quit()
                except Exception:
                    pass

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
