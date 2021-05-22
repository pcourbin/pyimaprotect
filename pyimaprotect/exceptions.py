"""Exceptions for IMAProtect Alarm."""


class IMAProtectConnectError(Exception):
    """Exception to indicate an error in connection."""

    def __init__(self, status_code, text):
        super(IMAProtectConnectError, self).__init__(
            "Invalid response"
            ", status code: {0} - Data: {1}".format(status_code, text)
        )
        self.status_code = status_code
        self.text = text
