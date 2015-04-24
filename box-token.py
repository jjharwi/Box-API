#!/usr/bin/python

from __future__ import print_function
import json
import requests
from ConfigParser import SafeConfigParser
import time

cp = SafeConfigParser()
cp.read('.box_config')
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
fp = open('.box_config', 'a')
cp.write(fp)
fp.close()

print('API token: ' + access_token)
print('Expires: ' + str(expire_time))
print('Refresh token: ' + refresh_token)

if int(cp.get('tokens',  'expire_time').strip()) < curr_time:
    print("Your token is still good")
    access_token = cp.get('tokens', 'access_token').strip()
    print("Use " + access_token)
