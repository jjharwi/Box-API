#!/usr/bin/python

from __future__ import print_function
from ConfigParser import SafeConfigParser
from Box_Folder import _folder_list

cp = SafeConfigParser()
cp.read('.box_config')
folder_id = cp.get('folders', 'folder_id').strip()

folder_list = _folder_list(folder_id)

print('*******Folder Listing******')
print('Name\t\tID')
print('***************************')
for k, v in folder_list.items():
    print('{0}\t{1}'.format(k, v))
