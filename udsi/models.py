"""
udsi.bases
~~~~~~~~~~

This module implements UDSI model classes.
"""

import base64
import dataclasses


@dataclasses.dataclass
class UDSIFile:
    gid: str
    name: str
    parents: list
    shared: bool

    msize: str
    nsize: int
    esize: int

    data: str

    @property
    def asdict(self):
        return dataclasses.asdict(self)

    def fromdict(self):
        """  """
