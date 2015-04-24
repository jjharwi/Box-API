#!/usr/bin/python

from __future__ import print_function
import argparse

from ConfigParser import SafeConfigParser

import Box

parser = argparse.ArgumentParser()
parser.add_argument("filename")
args = parser.parse_args()
filename = args.filename

cp = SafeConfigParser()
cp.read('.box_config')
folder_id = cp.get('folders', 'folder_id').strip()

folder_list = Box._folder_list(folder_id)

if filename in folder_list:
    file_id = folder_list[filename][0]
    update_info = Box._file_update(filename, file_id)
    if '20' in str(update_info):
        print('File {0} was updated in Box.'.format(filename))
    else:
        print(update_info)

else:
    file_upload = Box._file_upload(filename)
    if '20' in str(file_upload):
        print('File {0} was created in Box.'.format(filename))
    else:
        print(update_info)
