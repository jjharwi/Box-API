#!/usr/bin/python

from __future__ import print_function

import argparse
import Box

parser = argparse.ArgumentParser()
parser.add_argument("folder_name")
args = parser.parse_args()
folder_name = args.folder_name

folder_created = Box._folder_create(folder_name)

if '20' in str(folder_created):
    print('Folder created')
elif 'exists'in str(folder_created):
    print('Folder exists')
else:
    print('Something went wrong with that request, try again')
