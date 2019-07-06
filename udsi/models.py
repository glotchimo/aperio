"""
udsi.bases
~~~~~~~~~~

This module implements UDSI model classes.
"""

import base64
import dataclasses


@dataclasses.dataclass
class UDSIFile:
    id: str
    name: str

    parents: list
    shared: bool

    data: str

    @property
    def asdict(self):
        return dataclasses.asdict(self)

    def export(self):
        """ Exports data to original file. """
        dec = base64.b64decode(self.data).decode()

        with open(self.name, 'w+') as f:
            f.write(dec)
