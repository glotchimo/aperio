"""
aperio.client
~~~~~~~~~~~~~

This module implements the client for the Google API.
"""

import time
from textwrap import wrap

from .models import AperioFile

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class Client(object):
    """ Implement Google API handling.

    :param creds: a google-auth Credentials object.
    """

    def __init__(self, creds: Credentials):
        self.drive = build("drive", "v3", credentials=creds)
        self.sheets = build("sheets", "v4", credentials=creds)

        self.root = self._setup_root()

    def _setup_root(self):
        """ Gets or creates the root Aperio folder. """
        q = 'name = "aperio-root-folder"'
        r = self.drive.files().list(q=q, fields=("files(id, name)")).execute()

        files = r.get("files", [])
        root = files[0] if files else self.create_folder("root")

        return root

    def create_folder(self, name: str, parents: list = None) -> dict:
        """ Create a folder for a Aperio filedump.

        :param name: the name of the folder.
        :param parents: (optional) a list of parent directories under which
                        the given file should be stored.
        """
        body = {
            "name": f"aperio-{name}-folder",
            "mimeType": "application/vnd.google-apps.folder",
            "parents": parents,
        }
        r = self.drive.files().create(body=body, fields="id, name").execute()

        return r

    async def upload(self, file: AperioFile, **kwargs) -> dict:
        """ Uploads a Aperio file.

        A spreadsheet and folder are created, data is chunked,
        and pushed row-by-row to that sheet.

        :param file: a complete AperioFile object.

        :return sheet: a dict representing the new sheet.
        """
        body = {"properties": {"title": f"aperio-{file.name}"}}
        sheet = self.sheets.spreadsheets().create(body=body).execute()
        sheet_id = sheet.get("spreadsheetId")

        self.drive.files().update(fileId=sheet_id).execute()

        def split(seq: list, n: int):
            while seq:
                yield seq[:n]
                seq = seq[n:]

        blocks = wrap(file.data, 50000)
        arrays = list(split(blocks, 26))

        for i, array in enumerate(arrays):
            row = i + 1
            range = f"Sheet1!A{row}:Z{row}"
            body = {"values": [array]}

            try:
                self.sheets.spreadsheets().values().update(
                    spreadsheetId=sheet_id,
                    range=range,
                    valueInputOption="USER_ENTERED",
                    body=body,
                ).execute()
            except HttpError:
                print("Failed to upload array, cooling and retrying...")
                time.sleep(10)
                i -= 1
                continue

        sheet = self.sheets.spreadsheets().get(spreadsheetId=sheet_id).execute()

        return sheet

    async def get(self, id: str) -> (dict, dict):
        """ Gets a Aperio file.

        :param id: a valid file ID.

        :return sheet: a dict of sheet metadata.
        :return data: a dict of sheet contents.
        """
        sheet = self.sheets.spreadsheets().get(spreadsheetId=id).execute()

        nrows = sheet["sheets"][0]["properties"]["gridProperties"]["rowCount"]

        data = (
            self.sheets.spreadsheets()
            .values()
            .get(spreadsheetId=id, range=f"A1:Z{nrows}")
            .execute()
        )

        return sheet, data

    async def list(self, folder: str = None) -> list:
        """ Lists all Aperio files in a Aperio directory.

        :param folder: (optional) the ID of the folder from which
                       files should be fetched.

        :return files: a dict containing metadata and a list of files.
        """
        q = 'name contains "aperio-"'
        if folder:
            qa = f"parents in {repr(folder)}"
            q = " and ".join([q, qa])

        r = (
            self.drive.files()
            .list(
                q=q,
                pageSize=1000,
                fields=("nextPageToken, files(id, name, properties, mimeType)"),
            )
            .execute()
        )
        files = r.get("files", [])

        return files

    async def delete(self, id: str):
        """ Deletes a Aperio file.

        :param id: a valid file ID.
        """
        self.drive.files().delete(fileId=id).execute()
