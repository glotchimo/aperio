"""
aperio.utils
~~~~~~~~~~~~

This module implements the core utility methods used in Aperio.
"""

import base64

from .models import AperioFile


def build(name: str, **kwargs) -> AperioFile:
    """ Builds a AperioFile object from a file.

    :param name: the name/path of an accessible file.

    :return file: a new AperioFile object.
    """
    with open(name, "rb") as f:
        raw = f.read()
        enc = base64.b64encode(raw).decode()

    file = AperioFile(id="", name=name, data=enc)

    return file


def rebuild(sheet: dict, data: dict) -> AperioFile:
    """ Rebuilds a AperioFile object from an API response.

    Data sent to `rebuild` must be dictionary responses
    from the `get_file` method.

    :param sheet: a dict of sheet metadata.
    :param data: a dict of sheet contents.

    :return file: a new AperioFile object.
    """
    properties = sheet.get("properties")

    arrays = data.get("values")
    data = ""
    for array in arrays:
        block = "".join(array)
        data = "".join([data, block])

    file = AperioFile(
        id=sheet.get("spreadsheetId"),
        name=properties.get("title")[7:],
        data=data,
    )

    return file
