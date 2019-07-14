"""
tests.utils
~~~~~~~~~~~

This module implements utility methods for testing.
"""

import os
import json
import asyncio

from udsi.client import Client
from udsi.utils import build

from google.oauth2.service_account import Credentials


def async_test(f):
    def wrapper(*args, **kwargs):
        coro = asyncio.coroutine(f)
        future = coro(*args, **kwargs)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(future)

    return wrapper


def make_client():
    """ Instantiates an authenticated Client object. """
    credentials = Credentials.from_service_account_file(
        'credentials.json',
        scopes=[
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/spreadsheets'])
    client = Client(credentials)

    return client


async def make_file(client):
    """ Creates and uploads a temporary test file. """
    new = open('temp', mode='w+')
    new.write('temp')
    new.close()

    file = build('temp')
    sheet = await client.upload(file)

    return file, sheet


async def cleanup(client, id):
    """ Deletes temporary test files. """
    os.remove('temp')
    r = await client.delete(id)
