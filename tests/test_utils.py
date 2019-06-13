"""
tests.test_utils
~~~~~~~~~~~~~~~~~

This module implements the unit tests for the `utils` module.
"""

from udsi import utils
from udsi.models import UDSIFile


class TestUtils:
    """ Test class for the `utils` module. """
    def test_build_file(self):
        original = open('test.txt', 'rb')
        parsed = utils.build_file('test', original)

        assert type(parsed) is UDSIFile
        assert parsed.name == 'test'
        assert parsed.msize == '478.0 B'
        assert parsed.nsize == 478
        assert parsed.esize == 645

