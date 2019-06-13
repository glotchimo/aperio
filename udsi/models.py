"""
udsi.bases
~~~~~~~~~~

This module implements UDSI model classes.
"""

import base64
from dataclasses import dataclass


@dataclass
class UDSIFile:
    gid: str
    name: str
    parents: list
    shared: bool

    msize: str
    nsize: int
    esize: int

    data: str

