#!/usr/bin/python

from __future__ import print_function
import pprint
import argparse
import requests
import json
import time
from ConfigParser import SafeConfigParser

def _refresh_token():

    cp = SafeConfigParser()
    cp.read('.box_config')
    try:
        refresh_token = cp.get('tokens', 'refresh_token').strip()
        client_id = cp.get('application', 'client_id').strip()
        client_secret = cp.get('application', 'client_secret').strip()
    except NoSectionError as e:
        print("Either you are missing '.box_config' or you are missing"
              " one of the required sections.\n{}".format(e), file=stderr)
        exit(1)

    url = 'https://app.box.com/api/oauth2/token'
    refresh_data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': client_id, 'client_secret': client_secret}

    api_key = requests.post(url, data=refresh_data)
    api_token = json.loads(api_key.text)

    access_token = api_token['access_token']
    refresh_token = api_token['refresh_token']
    expires_in = api_token['expires_in']

    curr_time = time.strftime('%s', time.gmtime())
    expire_time = int(curr_time) + int(expires_in)

    cp.set('tokens', 'access_token', access_token)
    cp.set('tokens', 'expire_time', str(expire_time))
    cp.set('tokens', 'refresh_token', refresh_token)
    fp = open('.box_config', 'w+')
    cp.write(fp)
    fp.close()

    return access_token

def _file_upload(filename):
    try:
        cp = SafeConfigParser()
        cp.read('.box_config')
        folder_id = cp.get('folders', 'folder_id').strip()
        access_token = _refresh_token()

        headers = {"Authorization": "Bearer " + access_token}

        data = {"name": "filename", "folder_id": folder_id}
        files = {'filename': (filename, open(filename, 'rb'))}
        url = 'https://upload.box.com/api/2.0/files/content'

        upload_info = requests.post(url, files=files, headers=headers,
                                    data=data)
        return upload_info

    except IOError:
        print("That file doesn't exist locally, try again.")


def _file_update(filename, file_id):
    try:
        cp = SafeConfigParser()
        cp.read('.box_config')
        folder_id = cp.get('folders', 'folder_id').strip()
        access_token = _refresh_token()

        headers = {"Authorization": "Bearer " + access_token}

        data = {"name": "filename", "folder_id": folder_id}
        files = {'filename': (filename, open(filename, 'rb'))}
        url = 'https://upload.box.com/api/2.0/files/{0}/content'.format(
            file_id)

        update_info = requests.post(url, files=files, headers=headers,
                                    data=data)
        return update_info

    except IOError:
        print("That file doesn't exist locally, try again.")


def _file_download(filename):
    try:
        cp = SafeConfigParser()
        cp.read('.box_config')
        folder_id = cp.get('folders', 'folder_id').strip()
        access_token = _refresh_token()

        headers = {"Authorization": "Bearer " + access_token}

        folder_list = _folder_list(folder_id)

        if filename in folder_list:
            file_id = folder_list[filename][0]
            with open(filename, 'wb') as temp_file:
                download_info = requests.get(
                    'https://api.box.com/2.0/files/{0}/content'.format(
                        file_id), headers=headers, stream=True)
                for block in download_info.iter_content(1024):
                    if not block:
                        break
                    temp_file.write(block)
        else:
            print("Couldn't find that file in Box, try again.")
    except IOError:
        print("That file doesn't exist, try again.")

def _file_delete(filename):
    try:
        cp = SafeConfigParser()
        cp.read('.box_config')
        folder_id = cp.get('folders', 'folder_id').strip()

        access_token = _refresh_token()
        headers = {"Authorization": "Bearer " + access_token}
        folder_list = _folder_list(folder_id)

        if filename in folder_list:
            file_id = folder_list[filename][0]
            url = 'https://api.box.com/2.0/files/{0}'.format(file_id)
            file_delete = requests.delete(url, headers=headers)
            if '20' in str(file_delete):
                print("File {0} deleted.".format(filename))
            else:
                print("Something went wrong with that request, try again")
        return file_delete

    except IOError:
        print("That file doesn't exist, try again.")

def _file_info(file_id):
    access_token = _refresh_token()
    headers = {"Authorization": "Bearer " + access_token}

    url = 'https://api.box.com/2.0/files/{0}'.format(file_id)
    file_info = requests.get(url, headers=headers).json()
    return file_info

def _folder_info():
    url = 'https://api.box.com/2.0/folders/0'
    folder_info = requests.get(url, headers=headers).json()
    return folder_info

def _folder_list(folder_id):
    file_list = {}
    access_token = _refresh_token()
    headers = {"Authorization": "Bearer " + access_token}
    url = 'https://api.box.com/2.0/folders/{0}/items'.format(folder_id)
    folder_list = requests.get(url, headers=headers).json()
    for entry in folder_list['entries']:
        file_id = entry['id']
        file_name = entry['name']
        file_type = entry['type']
        file_list[file_name] = [file_id, file_type]
    return file_list

def _folder_create(folder_name):
    access_token = _refresh_token()
    headers = {"Authorization": "Bearer " + access_token}

    cp = SafeConfigParser()
    cp.read('.box_config')
    folder_id = cp.get('folders', 'folder_id').strip()
    folder_list = _folder_list(folder_id)

    if folder_name in folder_list:
        folder_create = 'That folder exists in Box, try again'

    else:
        url = 'https://api.box.com/2.0/folders'
        data = json.dumps({'name': folder_name, 'parent': {'id': folder_id}})
        folder_create = requests.post(url, headers=headers, data=data)

    return folder_create

#def _folder_change(folder_name):
#    folder_list = _folder_list(folder_id)
#    access_token = _refresh_token()
#    headers = {"Authorization": "Bearer " + access_token}
#
#    cp = SafeConfigParser()
#    cp.read('.box_config')
#    folder_id = cp.get('folders', 'folder_id').strip()
#
#    if folder_name in folder_list:
#        folder_create = 'That folder exists in Box, try again'


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    filename = args.filename

    uploaded_info = _file_upload(filename)
    pprint.pprint(uploaded_info.text)
