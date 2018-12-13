"""
uds2.bases
~~~~~~~~~~

This module implements the base uds2 file classes.
"""

import base64
from dataclasses import dataclass


@dataclass
class UDS2File:
    gid: str
    name: str
    parents: list
    shared: bool
    
    msize: str
    nsize: int
    esize: int
    
    data: str

