#!/usr/bin/python
from __future__ import print_function

import Box

file_id = '29128934794'
file_info = Box._file_info(file_id)

ctime = file_info['content_created_at']
mtime = file_info['content_modified_at']
owner = file_info['owned_by']['name']
name = file_info['name']
id = file_info['id']

print('ID: {0}\nFILENAME: {1}\nOWNER: {2}\nMODIFIED: {3}\nCREATED:'
      '{4}'.format(id, name, owner, mtime, ctime))