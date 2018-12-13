"""
tests.test_utils
~~~~~~~~~~~~~~~~~

This module implements the unit tests for the `utils` module.
"""

from uds2 import utils
from uds2.bases import UDS2File


class TestUtils:
    """ Test class for the `utils` module. """
    def test_build_file(self):
        original = open('test.txt', 'rb')
        parsed = utils.build_file('test', original)
        
        assert type(parsed) is UDS2File
        assert parsed.name == 'test'
        assert parsed.msize == '484.0 B'
        assert parsed.nsize == 484
        assert parsed.esize == 653

