"""Top-level package for pyimaprotect."""

__author__ = """Pierre COURBIN"""
__email__ = 'pierre.courbin@gmail.com'
__version__ = '1.2.0'

import requests
import time
import json
from jsonpath_ng import parse
import logging
_LOGGER = logging.getLogger(__name__)

IMA_URL_LOGIN = "https://pilotageadistance.imateleassistance.com/proxy/api/1.0/keychain/web-login/"
IMA_URL_ME = "https://pilotageadistance.imateleassistance.com/proxy/api/1.0/hss/me/?_=%s000&sessionid=%s"
IMA_URL_STATUS = "https://pilotageadistance.imateleassistance.com/proxy/api/1.0/hss/%s/status/?_=%s000&sessionid=%s"
IMA_PK_JSONPATH = '$..hss_pk'
IMA_STATUS_JSONPATH = '$..status'

STATUS_IMA_TO_NUM = {
    "off": 0,
    "partial": 1,
    "on": 2
}

STATUS_NUM_TO_TEXT = {
    0: "OFF",
    1: "PARTIAL",
    2: "ON",
    -1: "UNKNOWN"
}

DEFAULT_JSONPATH_PROPERTIES = {
    'first_name': '$..first_name',
    'last_name': '$..last_name',
    'email': '$..email',
    'offer': '$..offer',
    'contract_number': '$..contract_number',
    'alerts_enabled': '$..alerts_enabled',
}


class IMAProtect:
    """Class representing the IMA Protect Alarm and its API"""

    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._sessionid = None
        self._pk = None
        self._session = requests.Session()
        self._jsonpath_properties = DEFAULT_JSONPATH_PROPERTIES

    @property
    def username(self):
        """Return the username."""
        return self._username

    def get_all_info(self, retry=True):
        if (self._sessionid is None):
            self._update_sessionid()

        jsonresponse = {}
        url = IMA_URL_ME % (str(int(time.time())), str(self._sessionid))
        response = self._session.get(url)
        if (response.status_code == 200):
            jsonresponse = json.loads(response.content)
            self._update_info(jsonresponse)
        else:
            if (retry):
                self._update_sessionid()
                self.get_all_info(False)
            else:
                _LOGGER.error("Can't connect to the IMAProtect API, step 'ME'. Response code: %d" % (response.status_code))

        return jsonresponse

    def add_property(self, name, jsonpath):
        self._jsonpath_properties[name] = jsonpath

    def get_status(self, retry=True):
        if (self._pk is None):
            self.get_all_info()
        status = -1
        url = IMA_URL_STATUS % (str(self._pk), str(
            int(time.time())), str(self._sessionid))
        response = self._session.get(url)
        if (response.status_code == 200):
            status = STATUS_IMA_TO_NUM.get(parse(IMA_STATUS_JSONPATH).find(
                json.loads(response.content))[0].value)
        elif (response.status_code == 404):
            if (retry):
                self.get_all_info()
                status = self.get_status(False)
            else:
                _LOGGER.error("Can't connect to the IMAProtect API, step 'PK'. Response code: %d" % (response.status_code))
        else:
            _LOGGER.error("Can't connect to the IMAProtect API, step 'PK'. Response code: %d" % (response.status_code))

        return status

    def _update_sessionid(self):
        url = IMA_URL_LOGIN
        login = {'username': self._username, 'password': self._password}
        self._session = requests.Session()
        response = self._session.post(url, data=login)
        if (response.status_code == 200):
            self._sessionid = self._session.cookies.get_dict().get('sessionid')
        elif (response.status_code == 400):
            _LOGGER.error(
                """Can't connect to the IMAProtect API, step 'Login'.
                Please, check your logins. You must be able to login on https://pilotageadistance.imateleassistance.com.""")
        else:
            self._sessionid = None

    def _update_info(self, jsonresponse):
        self._pk = parse(IMA_PK_JSONPATH).find(jsonresponse)[0].value

        for att, jsonpath in self._jsonpath_properties.items():
            try:
                exec("self.{} = '{}'".format(att, parse(jsonpath).find(jsonresponse)[0].value))
            except:
                _LOGGER.error("Can't load %s property from the IMAProtect API (using '%s' jsonpath).", att, jsonpath)
