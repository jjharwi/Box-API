#!/usr/bin/python

import pprint

import requests

from Box_Refresh import _refresh_token

access_token = _refresh_token()
headers = {"Authorization": "Bearer " + access_token}


def _folder_info():
    url = 'https://api.box.com/2.0/folders/0'
    folder_info = requests.get(url, headers=headers).json()
    return folder_info


def _folder_list(folder_id):
    file_list = {}
    url = 'https://api.box.com/2.0/folders/{0}/items'.format(folder_id)
    folder_list = requests.get(url, headers=headers).json()
    for entry in folder_list['entries']:
        file_id = entry['id']
        file_name = entry['name']
        file_type = entry['type']
        file_list[file_name] = [file_id, file_type]
    return file_list

if __name__ == "__main__":
    pprint.pprint(_folder_info())
