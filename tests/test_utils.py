"""
tests.test_utils
~~~~~~~~~~~~~~~~~

This module implements the unit tests for the `utils` module.
"""

import os

from udsi.utils import build, rebuild
from udsi.models import UDSIFile

from tests.utils import make_client, make_file, cleanup


class TestUtils:
    """ Test class for the `utils` module. """
    def test_build(self):
        new = open('temp', mode='w+')
        new.write('temp')
        new.close()
        raw = open('temp', 'rb')

        file = build('temp', raw)

        assert type(file) is UDSIFile
        assert file.name == 'temp'

        os.remove('temp')

    def test_rebuild(self):
        client = make_client()
        file, r = make_file(client)
        r, d = client.get_file(r.get('spreadsheetId'))

        built = rebuild(r, d)

        assert type(built) is UDSIFile
        assert built.name == 'udsi-temp'

        cleanup(client, r.get('id'))
