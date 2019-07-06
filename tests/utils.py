"""
tests.utils
~~~~~~~~~~~

This module implements utility methods for testing.
"""

import os
import json

from udsi.client import Client
from udsi.utils import build

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

    file = build('temp', raw)
    r = client.upload_file(file)

    return file, r


def cleanup(client, id):
    """ Deletes temporary test files. """
    os.remove('temp')
    r = client.delete_file(id)
