"""
udsi.utils
~~~~~~~~~~

This module implements the core utility methods used in UDSI.
"""

import sys
import base64

from .models import UDSIFile


def build(name: str, **kwargs):
    """ Builds a UDSIFile object from a file.

    :param name: the name/path of an accessible file.

    :return file: a new UDSIFile object.
    """
    with open(name, 'rb') as f:
        raw = f.read()
        enc = base64.b64encode(raw).decode()

    file = UDSIFile(
        id='', name=name,
        data=enc)

    return file


def rebuild(sheet: dict, data: dict):
    """ Rebuilds a UDSIFile object from an API response.

    Data sent to `rebuild` must be dictionary responses
    from the `get_file` method.

    :param sheet: a dict of sheet metadata.
    :param data: a dict of sheet contents.

    :return file: a new UDSIFile object.
    """
    properties = sheet.get('properties')

    arrays = data.get('values')
    data = ''
    for array in arrays:
        block = ''.join(array)
        data = ''.join([data, block])

    file = UDSIFile(
        id=sheet.get('spreadsheetId'),
        name=properties.get('title')[5:],
        data=data)

    return file
