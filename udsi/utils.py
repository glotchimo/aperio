"""
udsi.utils
~~~~~~~~~~

This module implements the core utility methods used in UDSI.
"""

import sys
import base64

from .models import UDSIFile


def build(name: str, file, **kwargs):
    """ Builds a UDSIFile object from a TextIOWrapper object.

    Files sent to `build` must be opened in read-binary
    in order to be encoded to base64.

    :param file: a TextIOWrapper (`mode='rb'`).
    """
    raw = file.read(); file.close()
    enc = base64.b64encode(raw).decode()

    nsize = sys.getsizeof(raw)
    esize = sys.getsizeof(enc)

    file = UDSIFile(
        id='', name=name,
        shared=kwargs.get('shared', False),
        parents=kwargs.get('parents', []),
        data=enc)

    return file


def rebuild(r: dict, d: dict):
    """ Rebuilds a UDSIFile object from an API response.

    Files sent to `rebuild` must be dictionary responses
    from the `get_file` method.

    :param r: a dict of file data.
    :param d: a dict of sheet data.
    """
    arrays = d.get('values')
    data = ''
    for array in arrays:
        block = ''.join(array)
        data = ''.join([data, block])

    file = UDSIFile(
        id=r.get('spreadsheetId'), name=r.get('name'),
        shared=r.get('shared', False),
        parents=r.get('parents', []),
        data=data)

    return file
