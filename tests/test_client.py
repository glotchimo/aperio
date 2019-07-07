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
    async def test_upload(self):
        client = make_client()
        file, sheet = await make_file(client)

        assert type(sheet) is dict
        assert 'temp' in json.dumps(sheet)

        await cleanup(client, sheet.get('spreadsheetId'))

    @async_test
    async def test_get(self):
        client = make_client()
        file, sheet = await make_file(client)

        id = sheet.get('spreadsheetId')
        sheet, data = await client.get(id)

        assert type(sheet) is dict
        assert 'temp' in json.dumps(sheet)

        await cleanup(client, sheet.get('spreadsheetId'))

    @async_test
    async def test_list(self):
        client = make_client()
        file, sheet = await make_file(client)

        files = await client.list()

        assert type(files) is list
        assert 'temp' in json.dumps(files)

        await cleanup(client, sheet.get('spreadsheetId'))
