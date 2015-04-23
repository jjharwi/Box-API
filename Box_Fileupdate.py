#!/usr/bin/python

from pprint import pprint as pp
import argparse
from ConfigParser import SafeConfigParser
import Box_File
from Box_Folder import _folder_list

parser = argparse.ArgumentParser()
parser.add_argument("filename")
args = parser.parse_args()
filename = args.filename

cp = SafeConfigParser()
cp.read('.box_config')
folder_id = cp.get('folders','folder_id').strip()

folder_list = _folder_list(folder_id)

if filename in folder_list:
    file_id = folder_list[filename]
    update_info = Box_File._file_update(filename,file_id)
    if '20' in str(update_info):
        print 'File {0} was updated in Box.'.format(filename)

else:
    file_upload = Box_File._file_upload(filename)
    if '20' in str(file_upload):
        print 'File {0} was created in Box.'.format(filename)
