"""
udsi.client
~~~~~~~~~~~

This module implements the client for the Google API.
"""

import json

import requests

from .exceptions import APIError
from .models import UDSIFile

from google.auth.transport.requests import AuthorizedSession


BASE_URL = 'https://www.googleapis.com/drive/v3'
UPLOAD_URL = 'https://www.googleapis.com/upload/drive/v3'


class Client(object):
    """ Implement Google API handling.

    :param creds: a google-auth Credentials object.
    :param session: (optional) a session capable of making persistent
                    HTTP requests. Defaults to `requests.Session()`.
    """

    def __init__(self, creds):
        self.session = AuthorizedSession(creds)
        self.root = self._setup_root()

    def _setup_root(self):
        """ Get/create the `udsi_root` Drive folder. """
        q = 'properties has {key="udsi_root" and value="true"}'
        r = self.request(
            'get',
            f'{BASE_URL}/files?q={q}')
        data = json.loads(r.text)

        folders = data['files'] if 'files' in data else None
        if folders:
            root = folders[0]
        else:
            root = self.create_root()

        return root

    def request(self, method, url, **kwargs):
        """ Make a session request.

        Proper keyword arguments would be consistent with the keyword
        arguments used in the `Requests.request` base method.

        :param method: a valid HTTP method.
        :param url: a valid URL.
        """
        r = getattr(self.session, method)(url, **kwargs)
        if r.ok:
            return r
        else:
            raise APIError(r)

    def create_root(self):
        """ Create a `udsi_root` directory. """
        metadata = json.dumps({
            'name': 'udsi_root',
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [],
            'properties': {
                'udsi_root': True}})

        r = self.request(
            'post',
            f'{UPLOAD_URL}/files?uploadType=multipart',
            files={
                'metadata': (
                    'metadata.json', metadata, 'application/json'),
                'filedata': (
                    'filedata.json', '[]', 'application/json')})
        root = json.loads(r.text)

        return root

    def create_folder(self, name):
        """ Create a folder for a UDSI filedump.

        :param dump: a UDSIFile object generated from a file.
        """
        metadata = json.dumps({
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [],
            'properties': {
                'udsi_file': True}})

        r = self.request(
            'post',
            f'{UPLOAD_URL}/files?uploadType=multipart',
            files={
                'metadata': (
                    'metadata.json', metadata, 'application/json'),
                'filedata': (
                    'filedata.json', '[]', 'application/json')})
        folder = json.loads(r.text)

        return folder

    def upload_file(self, file, **kwargs):
        """ Upload a UDSI file.

        :param file: a complete UDSIFile object.
        """
        if type(file) is UDSIFile:
            filedata = file.asDict()

        for kwarg in kwargs:
            if kwarg not in ('id', 'name', 'parents'):
                kwargs.pop(kwarg)

        r = self.request(
            'post',
            f'{UPLOAD_URL}/files?uploadType=multipart',
            files={
                'metadata': {
                    'metadata.json',
                    json.dumps(kwargs), 'application/json'},
                'filedata': {
                    'filedata.json',
                    json.dumps(filedata),
                    'application/vnd.google-apps.file'}})
        data = json.loads(r.text)

        return data

    def get_file(self, gid):
        """ Get a UDSI file.

        :param fileid: a valid file ID.
        """
        r = self.request(
            'get',
            f'{BASE_URL}/files/{gid}')
        file = json.loads(r.text)

        return file

    def get_files(self, folder=None):
        """ Get all UDSI files in a UDSI directory.

        :param folder: (optional) defines whether or not UDSI should
                       get files from within a specified folder.
                       The value supplied here must be a valid folder.
                       Default folder is 'udsi_root'.
        """
        r = self.request(
            'get',
            '{}/files'.format(BASE_URL),
            data={
                'q': 'properties has {key="udsi" and value="true"} ',
                'parents': [folder or 'udsi_root'],
                'pageSize': 1000})
        data = r.text

        raw_files = data.get('files', [])
        files = []
        for rf in raw_files:
            props = rf.get('properties')
            files.append(UDSIFile(
                gid=rf.get('id'),
                name=rf.get('name'),
                mime=rf.get('mimeType'),
                parents=rf.get('parents'),
                size=rf.get('size'),
                nsize=props.get('size_numeric'),
                esize=props.get('encoded_size'),
                shared=props.get('shared'),
                data=None))

        return files

    def get_large_files(self, folder=None):
        """ Get all UDSI files in a large folder.

        This method serves the same function as `get_files`,
        but should be used for dump folders that contain over
        1000 files.

        :param folder: (optional) defines whether or not udsi
                       should get files from within a specified folder.
                       The value supplied here must be a valid
                       folder ID. Default folder is 'udsi_root'.
        """
        token = None
        dump = []
        while True:
            r = self.request(
                'get',
                f'{BASE_URL}/files',
                data={
                    'parents': [folder or 'udsi_root'],
                    'pageSize': 1000,
                    'pageToken': token,
                    'fields': 'nextPageToken, files(id, name, properties)'})
            data = json.loads(r.text)

            page = data.get('files')
            dump.append(page)

            token = data['nextPageToken']
            if not token:
                break

        return dump

    def export_file(self, gid):
        """ Export a UDSI file to plaintext.

        :param fileid: a valid file ID.
        """
        r = self.request(
            'get',
            f'{BASE_URL}/files/{gid}/export?mimeType="text/plain"')
        file = json.loads(r.text)

        return file

    def delete_file(self, gid):
        """ Delete a UDSI file.

        :param fileid: a valid file ID.
        """
        r = self.request('delete', f'{BASE_URL}/files/{gid}')

        return r

