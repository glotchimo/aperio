"""
uds2.exceptions
~~~~~~~~~~~~~~~

Custom exceptions for uds2.
"""


class UDS2Exception(Exception):
    """ Base uds2 exception. """


class APIError(Exception):
    """ Unknown API error. """
    def __init__(self, response):
        self.response = response.text

