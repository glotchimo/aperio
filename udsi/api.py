"""
udsi.udsi
~~~~~~~~~

This module implements the UDSI interface class.
"""

import os

from .client import Client


class UDSI:
    """ Implement the UDSI interface.

    :param creds: a google-auth Credentials object.
    """
    def __init__(self, creds):
        self.client = Client(creds)
