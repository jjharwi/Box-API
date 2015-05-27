#!/usr/bin/python

from __future__ import print_function

from ConfigParser import SafeConfigParser

from Box import _folder_list, _get_folder_id

folder_id = _get_folder_id()
folder_list = _folder_list(folder_id)

try:
    print('************Folder Listing***********')
    print('ID\t\tType\t\tName')
    print('*************************************')
    for k, v in folder_list.items():
        print('{1}\t{2}\t{0}'.format(k, v[0], v[1]))
except AttributeError:
    print("This folder no longer exists, returning home...")
