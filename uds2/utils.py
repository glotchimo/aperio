"""
udsi.utils
~~~~~~~~~~

This module implements the core utility methods used in UDSI.
"""

import sys
import base64

from .bases import UDS2File


def build_file(name, file, **kwargs):
    """ Builds a UDS2File object from a TextIOWrapper object.

    Files sent to `build_file` must be opened in read-binary
    in order to be encoded to base64.

    :param file: a TextIOWrapper (`mode='rb'`).
    """
    raw = file.read()
    enc = base64.b64encode(raw).decode()

    nsize = sys.getsizeof(raw)
    esize = sys.getsizeof(enc)

    unit = 'B'
    msize = float(nsize)
    for s in ('KB', 'MB', 'GB', 'TB'):
        if msize / 1024.0 >= 1:
            msize /= 1024.0
            unit = s
        else:
            break
    msize = '{} {}'.format(str(round(msize, 1)), unit)

    file = UDS2File(
        gid='',
        name=name,
        parents=[],
        shared=True,
        msize=msize,
        nsize=nsize,
        esize=esize,
        data=enc)

    return file

