# -*- encoding: utf-8 -*-

"""
Interface of the Angel One Brokerage's Smart API for Zentih Clown (ZC)

The official API is modeled for personal usages, and the configuration
is made computer specific. This package is not meant for public use,
but can be considered as an inspiration for other developers.

@author: Debmalya Pramanik
@copywright: 2024; Debmalya Pramanik
"""

# ? package follows https://peps.python.org/pep-0440/
# ? https://python-semver.readthedocs.io/en/latest/advanced/convert-pypi-to-semver.html
__version__ = "v0.0.1.dev0"

# init-time options registrations
from smartapizc import client
from smartapizc import errors
from smartapizc import history

# config directory is to be made available as a global variable for module
import os

CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config")
