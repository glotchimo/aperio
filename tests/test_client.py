"""
tests.test_client
~~~~~~~~~~~~~~~~~

This module implements the unit tests for the `client` module.
"""

import os
import json

from udsi.client import Client
from udsi.utils import build_file

from google.oauth2.service_account import Credentials


def make_client():
    """ Instantiates an authenticated Client object. """
    credentials = Credentials.from_service_account_file(
        'credentials.json',
        scopes=[
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/spreadsheets'])
    client = Client(credentials)

    return client


def make_file(client):
    """ Creates and uploads a temporary test file. """
    new = open('temp', mode='w+')
    new.write('temp')
    new.close()
    raw = open('temp', 'rb')

    file = build_file('temp', raw)
    r = client.upload_file(file)

    return file, r


def cleanup(client, id):
    """ Deletes temporary test files. """
    os.remove('temp')
    r = client.delete_file(id)


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
        file, r = make_file(client)

        assert type(r) is dict
        assert 'temp' in json.dumps(r)

        cleanup(client, r.get('spreadsheetId'))

    def test_get_file(self):
        client = make_client()
        file, r = make_file(client)

        id = r.get('spreadsheetId')
        r = client.get_file(id)

        assert type(r) is dict
        assert 'temp' in json.dumps(r)

        cleanup(client, r.get('spreadsheetId'))

    def test_list_files(self):
        client = make_client()
        file, r = make_file(client)

        files = client.list_files()

        assert type(files) is list
        assert 'temp' in json.dumps(files)

        cleanup(client, r.get('spreadsheetId'))
