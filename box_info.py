#!/usr/bin/python
from __future__ import print_function
import argparse
import Box

parser = argparse.ArgumentParser()
parser.add_argument("filename")
args = parser.parse_args()
filename = args.filename

file_info = Box._file_info(filename)
path = '/'
ctime = file_info['content_created_at']
mtime = file_info['content_modified_at']
size = file_info['size']
owner = file_info['owned_by']['name']
name = file_info['name']
id = file_info['id']
for folder in file_info['path_collection']['entries']:
    path += folder['name'] + '/'

print('ID:\t\t{0}\nFILENAME:\t{1}\nOWNER:\t\t{2}\nMODIFIED:\t{3}\nCREATED:\t'
      '{4}\nPATH:\t\t{5}\nSIZE:\t\t{6}'.format(id, name, owner, mtime, ctime, path, size))
