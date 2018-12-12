"""
uds2.client
~~~~~~~~~~~

This module implements the Client for the Google API.
"""

import json

import requests

from .exceptions import APIError
from .bases import UDS2File


BASE_URL = 'https://www.googleapis.com/drive/v3'
UPLOAD_URL = 'https://www.googleapis.com/upload/drive/v3'

class Client(object):
    """ Implement Google API handling.

    :param auth: an OAuth2 credential object.
    :param session: (optional) a session capable of making persistent
    HTTP requests. Defaults to `requests.Session()`.
    """

    def __init__(self, auth, session=None):
        self.auth = auth
        self.session = session or requests.Session()

        self.root = self.setup_root()
    
    def login(self):
        """ Authorize client. """
        if not self.auth.access_token \
            or (hasattr(self.auth, 'access_token_expired')
                and self.auth.access_token_expired):
            
            import httplib2; http = httplib2.Http()
            self.auth.refresh(http)
    
        self.session.headers.update({
            'Authorization': 'Bearer {}'.format(self.auth.access_token)})

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

    def setup_root(self):
        """ Get/create the `uds2_root` Drive folder. """
        q = 'properties has {key="uds2_root" and value="true"}'
        r = self.request(
            'get',
            '{}/files?q={}'.format(BASE_URL, q))
        data = json.loads(r.text)

        folders = data['files'] if 'files' in data else None
        if folders:
            root = folders[0]
        else:
            root = self.create_root()

        return root
    
    def create_root(self):
        """ Create a `uds2_root` directory. """
        metadata = json.dumps({
            'name': 'uds2_root',
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [],
            'properties': {
                'uds2_root': True}})

        r = self.request(
            'post',
            '{}/files?uploadType=multipart'.format(UPLOAD_URL),
            files={
                'metadata': (
                    'metadata.json', metadata, 'application/json'),
                'filedata': (
                    'filedata.json', '[]', 'application/json')})
        root = json.loads(r.text)
        
        return root
    
    def create_folder(self, name):
        """ Create a folder for a uds2 filedump.

        :param dump: a UDS2File object generated from a file.
        """
        metadata = json.dumps({
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [],
            'properties': {
                'uds2_file': True}})

        r = self.request(
            'post',
            '{}/files?uploadType=multipart'.format(UPLOAD_URL),
            files={
                'metadata': (
                    'metadata.json', metadata, 'application/json'),
                'filedata': (
                    'filedata.json', '[]', 'application/json')})
        folder = json.loads(r.text)
        
        return folder

    def upload_file(self, file, **kwargs):
        """ Upload a uds2 file.
        
        :param file: a complete UDS2File object.
        """
        # make the UDS2File dataclass HTTPable
        if type(file) is UDS2File:
            filedata = file.asDict()
        
        # scrub kwargs for metadata
        for kwarg in kwargs:
            if kwarg not in ('id', 'name', 'parents'):
                kwargs.pop(kwarg)
        
        r = self.request(
            'post',
            '{}/files?uploadType=multipart',
            files={
                'metadata': {
                    'metadata.json', json.dumps(kwargs), 'application/json'},
                'filedata': {
                    'filedata.json', json.dumps(filedata), 'application/vnd.google-apps.file'}})
        data = json.loads(r.text)

        return data

    def get_file(self, gid):
        """ Get a uds2 file.
        
        :param fileid: a valid file ID.
        """
        r = self.request(
            'get',
            '{}/files/{}'.format(BASE_URL, gid))
        file = json.loads(r.text)
        
        return file
    
    def get_files(self, folder=None):
        """ Get all uds2 files in a uds2 directory.
        
        :param folder: (optional) defines whether or not uds2 should get
        files from within a specified folder. The value supplied
        here must be a valid folder. Default folder is 'uds2_root'.
        """
        r = self.request(
            'get',
            '{}/files'.format(BASE_URL),
            data={
                'q': 'properties has {key="uds2" and value="true"} ',
                'parents': [folder or 'uds2_root'],
                'pageSize': 1000})
        data = r.text
        
        raw_files = data.get('files', [])
        files = []
        for rf in raw_files:
            props = rf.get('properties')
            files.append(UDS2File(
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
        """ Get all uds2 files in a large folder.

        This method serves the same function as `get_files`,
        but should be used for dump folders that contain over
        1000 files.

        :param folder: (optional) defines whether or not uds2 should get
        files from within a specified folder. The value supplied
        here must be a valid folder ID. Default folder is 'uds2_root'.
        """
        token = None
        dump = []
        while True:
            r = self.request(
                'get',
                '{}/files'.format(BASE_URL),
                data={
                    'parents': [folder or 'uds2_root'],
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
        """ Export a uds2 file to plaintext.

        :param fileid: a valid file ID.        
        """
        r = self.request(
            'get',
            '{}/files/{}/export?mimeType="text/plain"'.format(BASE_URL, gid))
        file = json.loads(r.text)
        
        return file

    def delete_file(self, gid):
        """ Delete a uds2 file.
        
        :param fileid: a valid file ID.
        """
        r = self.request('delete', '{}/files/{}'.format(BASE_URL, gid))
        
        return r

