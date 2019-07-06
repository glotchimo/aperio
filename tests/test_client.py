"""
tests.test_client
~~~~~~~~~~~~~~~~~

This module implements the unit tests for the `client` module.
"""

import os
import json

from udsi.client import Client
from udsi.utils import build

from tests.utils import make_client, make_file, cleanup

from google.oauth2.service_account import Credentials


class TestClient:
    """ Test class for the `client` module. """
    def test_upload_file(self):
        client = make_client()
        file, r = make_file(client)

        assert type(r) is dict
        assert 'temp' in json.dumps(r)

        cleanup(client, r.get('spreadsheetId'))

    def test_get_file(self):
        client = make_client()
        file, r = make_file(client)

        id = r.get('spreadsheetId')
        r, d = client.get(id)

        assert type(r) is dict
        assert 'temp' in json.dumps(r)

        cleanup(client, r.get('id'))

    def test_list_files(self):
        client = make_client()
        file, r = make_file(client)

        files = client.list()

        assert type(files) is list
        assert 'temp' in json.dumps(files)

        cleanup(client, r.get('spreadsheetId'))
