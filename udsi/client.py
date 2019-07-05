"""
udsi.client
~~~~~~~~~~~

This module implements the client for the Google API.
"""

import time
import json
import uuid
from textwrap import wrap

from .models import UDSIFile

from google.oauth2.service_account import Credentials
from google.auth.transport.requests import AuthorizedSession
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class Client(object):
    """ Implement Google API handling.

    :param creds: a google-auth Credentials object.
    :param session: (optional) a session capable of making persistent
                    HTTP requests. Defaults to `requests.Session()`.
    """

    def __init__(self, creds: Credentials):
        self.drive = build('drive', 'v3', credentials=creds)
        self.sheets = build('sheets', 'v4', credentials=creds)

    def create_folder(self, name: str, parents: list = None):
        """ Create a folder for a UDSI filedump.

        :param name: the name of the folder.
        :param parents: (optional) a list of parent directories under which
                        the given file should be stored.
        """
        body = {
            'name': f'udsi-{name}',
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': parents or []}
        r = self.drive.files() \
            .create(
                body=body,
                fields='id') \
            .execute()

        return r

    def upload_file(self, file: UDSIFile, **kwargs):
        """ Upload a UDSI file.

        A spreadsheet and folder are created, data is chunked,
        and pushed row-by-row to that sheet.

        :param file: a complete UDSIFile object.
        """
        parent = self.create_folder(file.name)

        body = {
            'properties': {
                'title': f'udsi-{file.name}'}}
        sheet = self.sheets.spreadsheets() \
            .create(body=body) \
            .execute()
        sheet_id = sheet.get('spreadsheetId')

        self.drive.files() \
            .update(
                fileId=sheet_id,
                addParents=parent.get('folderId')) \
            .execute()

        def split(seq: list, n: int):
            while seq:
                yield seq[:n]
                seq = seq[n:]

        blocks = wrap(file.data, 50000)
        arrays = list(split(blocks, 10))

        for i, array in enumerate(arrays):
            row = i + 1
            range = f'Sheet1!A{row}:J{row}'
            body = {'values': [array]}

            try:
                r = self.sheets.spreadsheets().values() \
                    .update(
                        spreadsheetId=sheet_id,
                        range=range,
                        valueInputOption='USER_ENTERED',
                        body=body) \
                    .execute()
            except HttpError as e:
                print('Failed to upload array, cooling and retrying...')
                time.sleep(10)
                i -= 1; continue

        sheet = self.sheets.spreadsheets() \
            .get(spreadsheetId=sheet_id) \
            .execute()

        return sheet

    def get_file(self, id: str):
        """ Get a UDSI file.

        :param id: a valid file ID.
        """
        r = self.sheets.spreadsheets() \
            .get(
                spreadsheetId=id,
                includeGridData=True) \
            .execute()

        return r

    def list_files(self, folder: str = None):
        """ List all UDSI files in a UDSI directory.

        :param folder: (optional) the ID of the folder from which
                       files should be fetched.
        """
        q = 'name contains "udsi-"'
        if folder:
            qa = f'parents in {repr(folder)}'
            q = ' and '.join([q, qa])

        r = self.drive.files() \
            .list(
                q=q,
                pageSize=1000,
                fields=(
                    'nextPageToken, files(id, name, properties, mimeType)')) \
            .execute()
        files = r.get('files', [])

        return files

    def delete_file(self, id: str):
        """ Delete a UDSI file.

        :param id: a valid file ID.
        """
        r = self.drive.files() \
            .delete(fileId=id) \
            .execute()

        return r
