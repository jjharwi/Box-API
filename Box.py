#!/usr/bin/python

from __future__ import print_function
import pprint
import argparse
import os
import requests
import json
import time
from ConfigParser import SafeConfigParser

conf_file = os.path.expanduser('~/.box_config')

def _refresh_token():

    cp = SafeConfigParser()
    cp.read(conf_file)
    try:
        refresh_token = cp.get('tokens', 'refresh_token').strip()
        client_id = cp.get('application', 'client_id').strip()
        client_secret = cp.get('application', 'client_secret').strip()
    except NoSectionError as e:
        print("Either you are missing conf_file or you are missing"
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

    cp.set('tokens', 'access_token', access_token)
    cp.set('tokens', 'refresh_token', refresh_token)
    fp = open(conf_file, 'w+')
    cp.write(fp)
    fp.close()

    return access_token

def _get_folder_id():
    cp = SafeConfigParser()
    cp.read(conf_file)
    folder_id = cp.get('folders', 'folder_id').strip()

    return folder_id

def _file_upload(filename):
    try:

        folder_id = _get_folder_id()

        access_token = _refresh_token()
        headers = {"Authorization": "Bearer " + access_token}

        data = {"name": "filename", "folder_id": folder_id}
        files = {'filename': (filename, open(filename, 'rb'))}
        url = 'https://upload.box.com/api/2.0/files/content'

        upload_info = requests.post(url, files=files, headers=headers,
                                    data=data)

        if '20' not in str(upload_info):
            print('Something went wrong with that request')

        return upload_info

    except IOError:
        print("That file doesn't exist locally, try again.")


def _file_update(filename):
    try:

        folder_id = _get_folder_id()
        folder_list = _folder_list(folder_id)

        access_token = _refresh_token()
        headers = {"Authorization": "Bearer " + access_token}

        box_filename = filename.split('/')[-1]

        if box_filename in folder_list:
            file_id = folder_list[box_filename][0]
            data = {"name": "filename", "folder_id": folder_id}
            files = {'filename': (box_filename, open(filename, 'rb'))}
            url = 'https://upload.box.com/api/2.0/files/{0}/content'.format(
                file_id)

            update_info = requests.post(url, files=files, headers=headers,
                                        data=data)

            if '20' not in str(update_info):
                print('Something went wrong with that request')

        else:
            update_info =_file_upload(filename)

        return update_info

    except IOError:
        print("That file doesn't exist locally, try again.")


def _file_download(filename):
    try:

        folder_id = _get_folder_id()
        folder_list = _folder_list(folder_id)

        access_token = _refresh_token()
        headers = {"Authorization": "Bearer " + access_token}

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

        folder_id = _get_folder_id()
        folder_list = _folder_list(folder_id)

        access_token = _refresh_token()
        headers = {"Authorization": "Bearer " + access_token}

        if filename not in folder_list:
            file_delete = 'File not found in Box'
        elif filename in folder_list:
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

def _file_info(filename):

    folder_id = _get_folder_id()
    folder_list = _folder_list(folder_id)

    access_token = _refresh_token()
    headers = {"Authorization": "Bearer " + access_token}

    if filename not in folder_list:
        file_info = '404: File not found in Box'
    elif filename in folder_list:
        file_id = folder_list[filename][0]
        url = 'https://api.box.com/2.0/files/{0}'.format(file_id)
        file_info = requests.get(url, headers=headers).json()

    return file_info

def _folder_info(folder_name):

    folder_id =_get_folder_id()

    access_token = _refresh_token()
    headers = {"Authorization": "Bearer " + access_token}

    folder_list = _folder_list(folder_id)
    if folder_name in folder_list:
        folder_id = folder_list[folder_name][0]
    else:
        folder_id = 0

    url = 'https://api.box.com/2.0/folders/{0}'.format(folder_id)
    folder_info = requests.get(url, headers=headers).json()
    return folder_info

def _folder_list(folder_id):

    """What's in the baaaaux?!??"""

    try:
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

    except KeyError:
        box_folder_id = '0'
        cp1 = SafeConfigParser()
        cp1.read(conf_file)
        cp1.set('folders','folder_id',box_folder_id)
        fp = open(conf_file, 'w+')
        cp1.write(fp)
        fp.close()
        print("The folder in .box_config doesn't exist, returning home...")

def _folder_create(folder_name):

    folder_id = _get_folder_id()
    folder_list = _folder_list(folder_id)

    access_token = _refresh_token()
    headers = {"Authorization": "Bearer " + access_token}

    if folder_name in folder_list:
        folder_create = 'That folder exists in Box, try again'

    else:
        url = 'https://api.box.com/2.0/folders'
        data = json.dumps({'name': folder_name, 'parent': {'id': folder_id}})
        folder_create = requests.post(url, headers=headers, data=data)

    return folder_create

def _folder_change(folder_name):
    try:
        folder_id = _get_folder_id()
        folder_list = _folder_list(folder_id)

        access_token = _refresh_token()
        headers = {"Authorization": "Bearer " + access_token}

        if folder_name in folder_list:
            print('To return to your root folder, use "box_cd home"\n')
            box_folder_id = folder_list[folder_name][0]
            cp1 = SafeConfigParser()
            cp1.read(conf_file)
            cp1.set('folders','folder_id',box_folder_id)  
            fp = open(conf_file, 'w+')
            cp1.write(fp)
            fp.close()
        elif 'home' in folder_name:
            box_folder_id = '0'
            cp1 = SafeConfigParser()
            cp1.read(conf_file)
            cp1.set('folders','folder_id',box_folder_id)  
            fp = open(conf_file, 'w+')
            cp1.write(fp)
            fp.close()
        else:
            print("Folder {0} doesn't exist at this level".format(folder_name))
    except KeyError:
        box_folder_id = '0'
        cp1 = SafeConfigParser()
        cp1.read(conf_file)
        cp1.set('folders','folder_id',box_folder_id)
        fp = open(conf_file, 'w+')
        cp1.write(fp)
        fp.close()
        print("The folder in .box_config doesn't exist, returning home...")

def _folder_delete(folder_name):

    folder_id = _get_folder_id()
    folder_list = _folder_list(folder_id)

    access_token = _refresh_token()
    headers = {"Authorization": "Bearer " + access_token}

    if folder_name not in folder_list:
        folder_to_delete = 'Folder not found in Box'
    elif folder_name in folder_list:
        folder_to_delete = folder_list[folder_name][0]
        url = 'https://api.box.com/2.0/folders/{0}?recursive=true'.format(folder_to_delete)
        folder_to_delete = requests.delete(url, headers=headers)
        if '20' in str(folder_to_delete):
            print("Folder {0} deleted.".format(folder_name))
    else:
        print("Something went wrong with that request, try again")
    return folder_to_delete

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    filename = args.filename

    uploaded_info = _file_upload(filename)
    pprint.pprint(uploaded_info.text)
