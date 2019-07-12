"""
udsi.client
~~~~~~~~~~~

This module implements the client for the Google API.
"""

import time
import string
from textwrap import wrap

from .models import UDSIFile

from google.oauth2.service_account import Credentials
from google.auth.transport.requests import AuthorizedSession
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class Client(object):
    """ Implement Google API handling.

    :param creds: a google-auth Credentials object.
    """
    def __init__(self, creds: Credentials):
        self.drive = build('drive', 'v3', credentials=creds)
        self.sheets = build('sheets', 'v4', credentials=creds)

    async def upload(self, file: UDSIFile, **kwargs) -> dict:
        """ Uploads a UDSI file.

        A spreadsheet and folder are created, data is chunked,
        and pushed row-by-row to that sheet.

        :param file: a complete UDSIFile object.

        :return sheet: a dict representing the new sheet.
        """
        body = {
            'properties': {
                'title': f'udsi-{file.name}'}}
        sheet = self.sheets.spreadsheets() \
            .create(body=body) \
            .execute()
        sheet_id = sheet.get('spreadsheetId')

        self.drive.files() \
            .update(
                fileId=sheet_id) \
            .execute()

        def split(seq: list, n: int):
            while seq:
                yield seq[:n]
                seq = seq[n:]

        blocks = wrap(file.data, 50000)
        arrays = list(split(blocks, 26))

        for i, array in enumerate(arrays):
            row = i + 1
            range = f'Sheet1!A{row}:Z{row}'
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

    async def get(self, id: str) -> (dict, dict):
        """ Gets a UDSI file.

        :param id: a valid file ID.

        :return sheet: a dict of sheet metadata.
        :return data: a dict of sheet contents.
        """
        sheet = self.sheets.spreadsheets() \
            .get(spreadsheetId=id) \
            .execute()

        nrows = sheet \
            ['sheets'][0] \
            ['properties']['gridProperties'] \
            ['rowCount']

        data = self.sheets.spreadsheets().values() \
            .get(spreadsheetId=id, range=f'A1:Z{nrows}') \
            .execute()

        return sheet, data

    async def list(self, folder: str = None) -> list:
        """ Lists all UDSI files in a UDSI directory.

        :param folder: (optional) the ID of the folder from which
                       files should be fetched.

        :return files: a dict containing metadata and a list of files.
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

    async def delete(self, id: str):
        """ Deletes a UDSI file.

        :param id: a valid file ID.
        """
        r = self.drive.files() \
            .delete(fileId=id) \
            .execute()
