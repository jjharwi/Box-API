#!/usr/bin/python

from pprint import pprint as pp
from ConfigParser import SafeConfigParser
from Box_Folder import _folder_list

cp = SafeConfigParser()
cp.read('.box_config')
folder_id = cp.get('folders','folder_id').strip()

folder_list = _folder_list(folder_id)

pp(folder_list)
