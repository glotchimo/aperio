"""
udsi.udsi
~~~~~~~~~

This module implements the UDSI interface class.
"""

import os

from .client import Client


class UDSI:
    """ Implement the UDSI interface.

    :param auth: an OAuth2 credential object.
    :param session: (optional) a session capable of making persistent
                    HTTP requests. Defaults in client to
                    `requests.Session()`.
    """
    def __init__(self, auth, session=None):
        self.client = Client(auth, session=session)
