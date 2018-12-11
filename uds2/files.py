"""
uds2.files
~~~~~~~~~~

This module implements the base uds2 file classes.
"""

import base64
from dataclasses import dataclass


@dataclass
class UDS2File:
    gid: str
    name: str
    mime: str
    parents: list
    shared: bool
    
    size: str
    nsize: float
    esize: float
    
    data: bytes

