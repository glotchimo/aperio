"""
tests.test_client
~~~~~~~~~~~~~~~~~

This module implements the unit tests for the `client` module.
"""

import os
import json

from udsi.client import Client
from udsi.utils import build

from tests.utils import async_test, make_client, make_file, cleanup

from google.oauth2.service_account import Credentials


class TestClient:
    """ Test class for the `client` module. """
    @async_test
    async def test_upload_file(self):
        client = make_client()
        file, r = await make_file(client)

        assert type(r) is dict
        assert 'temp' in json.dumps(r)

        await cleanup(client, r.get('spreadsheetId'))

    @async_test
    async def test_get_file(self):
        client = make_client()
        file, r = await make_file(client)

        id = r.get('spreadsheetId')
        r, d = await client.get(id)

        assert type(r) is dict
        assert 'temp' in json.dumps(r)

        await cleanup(client, r.get('id'))

    @async_test
    async def test_list_files(self):
        client = make_client()
        file, r = await make_file(client)

        files = await client.list()

        assert type(files) is list
        assert 'temp' in json.dumps(files)

        await cleanup(client, r.get('spreadsheetId'))
