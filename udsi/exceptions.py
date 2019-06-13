"""
udsi.exceptions
~~~~~~~~~~~~~~~

Custom exceptions for UDSI.
"""


class APIError(Exception):
    """ Unknown API error. """
    def __init__(self, response):
        self.response = response
        self.status = response.status_code
        self.reason = response.reason
        self.text = response.text

    def __str__(self):
        return f"[ERROR {self.status}] - {self.reason} \n {self.text}"

