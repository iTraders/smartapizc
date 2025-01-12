# -*- encoding: utf-8 -*-

"""
Error Codes & Descriptions for AngelOne's Smart API

The SmartAPI service provides certain error codes and descriptions
which are defined here for the user's reference. The descriptions are
modified for better understanding and readability.
"""

import os
import json

class AngelOneError(Exception):
    """
    AngelOne API's Internal Exception are Documented Here

    A total list of exceptions are available at the official API
    https://smartapi.angelbroking.com/docs/Exceptions. The exceptions
    are raised when the API is unable to process the request.

    :type  code: str
    :param code: The error code returned by the AngelOne API, which
        is a six digit alphanumeric code.
    """

    def __init__(self, code : int, message : str = None) -> None:
        self.code = code
        self.cmessage = message # custom/additional message

        self.imessage = self.get_message(code)
        super().__init__(self.imessage)


    @staticmethod
    def get_message(code : str) -> str:
        from smartapizc import CONFIG_DIR
        
        errormessages = json.load(
            open(os.path.join(CONFIG_DIR, "angeloneerror.json"), "r")
        )

        return errormessages.get(code, "Unknown Error")


    def _format_message(self, i : str, c : str) -> str:
        """
        The Error Message is Custom Formatted and Returned

        The error message so defined by the AngelOne is defined as
        :attr:`i` which is the internal message by the client, and any
        additional information is defined as :attr:`c` - which is the
        custom message send by the :mod:`smartapizc` module.
        """
        return f"Error Code: {self.code}\n" + \
            f"  >> Internal Message Description: {i}\n" + \
            f"  >> Custom Message Description: {c}"
