#!/usr/bin/python

from __future__ import print_function

from ConfigParser import SafeConfigParser

from Box import _folder_list

cp = SafeConfigParser()
cp.read('.box_config')
folder_id = cp.get('folders', 'folder_id').strip()

folder_list = _folder_list(folder_id)

print('************Folder Listing***********')
print('ID\t\tType\t\tName')
print('*************************************')
for k, v in folder_list.items():
    print('{1}\t{2}\t{0}'.format(k, v[0], v[1]))
