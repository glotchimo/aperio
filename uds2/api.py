"""
uds2.api
~~~~~~~~

This module implements the uds2 interface class UDS2.
"""

import os

from .client import Client


class UDS2:
    """ Implement the UDS2 interface.
    
    :param auth: an OAuth2 credential object.
    :param session: (optional) a session capable of making persistent
    HTTP requests. Defaults to `requests.Session()`.
    """
    def __init__(self, auth, session=None):
        self.client = Client(auth, session=session)
    
    

