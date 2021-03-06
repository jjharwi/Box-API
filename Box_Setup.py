#!/usr/bin/python

from __future__ import print_function
from sys import exit, stderr
import json
import time
import os
import requests
from ConfigParser import SafeConfigParser

conf_file = os.path.expanduser('~/.box_config')

cp = SafeConfigParser()
try:
    cp.read(conf_file)
except Exception as e:
    print(".box_config either does not exist or is unreadable\n{}".format(e),
          file=stderr)
    exit(1)

client_id = cp.get('application', 'client_id').strip()
client_secret = cp.get('application', 'client_secret').strip()

print('Click here to authorize:'
      'https://racker.app.box.com/api/oauth2/authorize?response_type=code&'
      'client_id={0}&state=security_token%{1}'.format(
          client_id, client_secret))

access_token = raw_input(
    'Enter the security code (end of the URL that pops up): ')

url = 'https://app.box.com/api/oauth2/token'

data = {'grant_type': 'authorization_code', 'code': access_token, 'client_id':
        client_id, 'client_secret': client_secret}

api_key = requests.post(url, data=data)

api_token = json.loads(api_key.text)

access_token = api_token['access_token']
refresh_token = api_token['refresh_token']
expires_in = api_token['expires_in']

curr_time = time.strftime('%s', time.gmtime())
expire_time = int(curr_time) + int(expires_in)

cp = SafeConfigParser()
cp.add_section('tokens')
cp.set('tokens', 'access_token', access_token)
cp.set('tokens', 'expire_time', str(expire_time))
cp.set('tokens', 'refresh_token', refresh_token)
cp.add_section('folders')
cp.set('folders', 'folder_id', '0')
fp = open(conf_file, 'a')
cp.write(fp)
fp.close()

print('API token: ' + access_token)
print('Expires: ' + str(expire_time))
print('Refresh token: ' + refresh_token)

if int(cp.get('tokens',  'expire_time').strip()) < curr_time:
    print("Your token is still good")
    access_token = cp.get('tokens', 'access_token').strip()
    print("Use " + access_token)
