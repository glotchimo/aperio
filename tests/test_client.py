"""
tests.test_client
~~~~~~~~~~~~~~~~~

This module implements the unit tests for the `client` module.
"""

from uds2.client import Client

from requests import Session
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import AuthorizedSession


def make_client():
    credentials = Credentials.from_service_account_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/drive'])
    session = AuthorizedSession(credentials)

    client = Client(credentials, session=session)
    return client

class TestClient:
    """ Test class for the `client` module. """
    def test_init(self):
        client = make_client()

        assert type(client) is Client
        assert type(client.auth) is Credentials
        assert type(client.session) is AuthorizedSession
    
    def test_create_folder(self):
        client = make_client()

        assert type(client.create_folder('Test')) is dict

