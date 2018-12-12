"""
uds2.exceptions
~~~~~~~~~~~~~~~

Custom exceptions for uds2.
"""


class APIError(Exception):
    """ Unknown API error. """
    def __init__(self, response):
        self.response = response
        self.status = response.status_code
        self.reason = response.reason
        self.text = response.text
    
    def __str__(self):
        return ('[ERROR {}] - {} \n {}'
                .format(self.status, self.reason, self.text))

