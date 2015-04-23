#!/usr/bin/python

import requests
import pprint
import json
import argparse
from ConfigParser import SafeConfigParser
from Box_Refresh import _refresh_token

def _file_upload(filename):
    try:
        cp = SafeConfigParser()
        cp.read('.box_config')
        folder_id = cp.get('folders','folder_id').strip()
        access_token = _refresh_token()

        headers = {"Authorization": "Bearer " + access_token}

        data = {"name":"filename", "folder_id":folder_id}
        files = {'filename': (filename, open(filename, 'rb'))}
        url = 'https://upload.box.com/api/2.0/files/content'

        upload_info = requests.post(url,files=files,headers=headers,data=data)
        return upload_info

    except IOError:
        print "That file doesn't exist locally, try again."

def _file_update(filename,file_id):
    try:
        cp = SafeConfigParser()
        cp.read('.box_config')
        folder_id = cp.get('folders','folder_id').strip()
        access_token = _refresh_token()

        headers = {"Authorization": "Bearer " + access_token}

        data = {"name":"filename", "folder_id":folder_id}
        files = {'filename': (filename, open(filename, 'rb'))}
        url = 'https://upload.box.com/api/2.0/files/{0}/content'.format(file_id)

        update_info = requests.post(url,files=files,headers=headers,data=data)
        return update_info

    except IOError:
        print "That file doesn't exist locally, try again."

def _file_info(file_id):
    access_token = _refresh_token()
    headers = {"Authorization": "Bearer " + access_token}

    url = 'https://api.box.com/2.0/files/{0}'.format(file_id)
    file_info = requests.get(url,headers=headers).json()
    return file_info

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    filename = args.filename

    upload_info = _file_upload(filename)
    pprint.pprint(upload_info.text)
