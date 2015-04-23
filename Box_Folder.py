#!/usr/bin/python

import requests
import pprint
import argparse
from Box_Refresh import _refresh_token

access_token = _refresh_token()
headers = {"Authorization": "Bearer " + access_token}

def _folder_info():
    url = 'https://api.box.com/2.0/folders/0'
    folder_info = requests.get(url,headers=headers).json()
    return folder_info

def _folder_list(folder_id):
    file_list = {}
    url = 'https://api.box.com/2.0/folders/{0}/items'.format(folder_id)
    folder_list = requests.get(url,headers=headers).json()
    for entry in folder_list['entries']:
        file_id = entry['id']
        file_name = entry['name']
        file_list[file_name] = file_id
    return file_list

if __name__ == "__main__":
    folder_info = _folder_info()
    pprint.pprint(folder_info)
