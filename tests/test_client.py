"""
tests.test_client
~~~~~~~~~~~~~~~~~

This module implements the unit tests for the `client` module.
"""

import os

from udsi.client import Client
from udsi.utils import build_file

from google.oauth2.service_account import Credentials


def make_client():
    credentials = Credentials.from_service_account_file(
        'credentials.json',
        scopes=[
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/spreadsheets'])
    client = Client(credentials)

    return client


class TestClient:
    """ Test class for the `client` module. """
    def test_init(self):
        client = make_client()

        assert type(client) is Client

    def test_create_folder(self):
        client = make_client()

        r = client.create_folder('test folder')

        assert type(r) is dict

    def test_upload_file(self):
        client = make_client()

        new = open('temp', mode='w+')
        new.write('temp')
        new.close()
        raw = open('temp', 'rb')

        file = build_file('Test File', raw)
        r = client.upload_file(file)

        assert type(r) is dict

        os.remove('temp')
        client.delete_file(r.get('spreadsheetId'))

    def test_get_file(self):
        client = make_client()

        new = open('temp', mode='w+')
        new.write('temp')
        new.close()
        raw = open('temp', 'rb')

        file = build_file('Test File', raw)
        r = client.upload_file(file)
        id = r.get('spreadsheetId')

        r = client.get_file(id)

        assert type(r) is dict

        os.remove('temp')
        client.delete_file(r.get('spreadsheetId'))
