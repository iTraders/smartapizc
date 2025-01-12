# -*- encoding: utf-8 -*-

"""
Client API Interface Object for Smart API ZC

Exposes the client object which serves as the brain/bridge between the
official API and interactive user interface for myself.
"""

import os

import pyotp
import getpass
import SmartApi

def get_client(totp : str = None, apikey : str = None) -> SmartApi.SmartConnect:
    """
    Returns the Client API Object for Smart API ZC

    The client is an object of type :attr:`SmartApi.SmartConnect`
    which can be used to execute orders, fetch historical data etc.
    using the Smart API.

    The parameters defined are fetched from the environment variables,
    or taken as an user input when the module is imported if the
    environment variables are not found.

    :type  totp: str
    :param totp: The Time-based One Time Password (TOTP) generated
        using the "Enable TOTP" option in the SmartAPI dashboard (more
        information at - https://smartapi.angelbroking.com/enable-totp).
        The TOTP changes everyday, and is a mandate by the SEBI.

    :type  apikey: str
    :param apikey: The API Key for the SmartAPI, which is generated
        when an application was created (more information at -
        https://smartapi.angelbroking.com/docs).

    Salient Parameters
    ------------------

    The other important salient parameters are controlled via the
    environment variables, or is taken as an user input on import.

    :type  username: str
    :param username: The username used for logging into the AngelOne
        broker account. This username should be defined as an
        environment variable named ``ANGELONE_USERNAME``, if not found
        then is taken as an user input.

    :type  password: str
    :param password: The "MPIN" used for logging into the AngelOne
        broker account. This password should be defined as an
        environment variable named ``ANGELONE_PASSWORD``, if not found
        then is taken as an user input.
    """

    username = os.getenv(
        "ANGELONE_USERNAME", 
        input("Enter the Username for AngelOne: ")
    )
    password = os.getenv(
        "ANGELONE_PASSWORD",
        getpass.getpass("Enter the Login MPIN for AngelOne: ")
    )

    # ! the totp and the apikey to be passed as the function arguments
    # but for security purpose (maybe during a demo) it is essential to
    # hide sensitive information, so the values are encapsulated
    totp = totp or getpass.getpass(
        "Enter the TOTP for SmartAPI"
        "(https://smartapi.angelbroking.com/enable-totp): "
    )

    apikey = apikey or getpass.getpass(
        "Enter the API Key for SmartAPI"
        "(https://smartapi.angelbroking.com/): "
    )

    totp = pyotp.TOTP(totp).now() # override with pyotp, today's totp
    client = SmartApi.SmartConnect(apikey)
    session = client.generateSession(username, password, totp)
    return client, session
