#!/usr/bin/env python

import os
import argparse
import Box

parser = argparse.ArgumentParser()
parser.add_argument("folder_name")
args = parser.parse_args()
folder_name = args.folder_name
folder_id = Box._get_folder_id()

box_folder_name = folder_name.split("/")[-1]

folder_list = Box._folder_list(folder_id)
print(folder_id)
if folder_id not in folder_list:
    Box._folder_create(box_folder_name)
    Box._folder_change(box_folder_name)
    for file in os.listdir(folder_name):
        filename = folder_name + '/' + file
        print('Uploading {0}...'.format(filename))
        Box._file_update(filename)

else:
    for file in os.listdir(folder_name):
        filename = folder_name + '/' + file
        print('Uploading {0}...'.format(filename))
        Box._file_update(filename)
    #    os.remove(filename)
