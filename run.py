import config
import json
import random
import requests
import time

import spotipy
import spotipy.util as util

from functools import wraps
from datetime import datetime

t_key = config.timeular_key
t_secret = config.timeular_secret

s_id = config.spotify_id
s_secret = config.spotify_secret

def check_token(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if self._access_token == None:
            return False
        return f(self, *args, **kwargs)

    return wrapper


def get_current_time():
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]


class API(object):
    _METHODS = ['get', 'post', 'patch', 'delete']
    _CLASS_STATUS_CODES = (200, 226) # https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#2xx_Success

    _access_token = None
    _base_url = None

    def __init__(self, base_url, access_token=None):
        self._base_url = base_url
        self._access_token = access_token

    def _make_response(self, route='', method='get', json={}, need_auth=True, headers={}):
        if method not in self._METHODS:
            print('[%s] is not allowed' % method)
            return False
        url = self._base_url + route
        if need_auth:
            headers['Authorization'] = 'Bearer ' + self._access_token
        response = getattr(requests, method)(url, json=json, headers=headers)
        if response.status_code < self._CLASS_STATUS_CODES[0] or response.status_code > self._CLASS_STATUS_CODES[1]:
            print('code error: %d' % response.status_code)
            print('_make_response error for url [%s]: %s' % (url, response.text))
            return False
        return response.json()


class Timeular(API):
    activities = None
    devices = None
    tracking = None
    time_entries = None
    _api_key = None
    _api_secret = None

    def __init__(self, base_url='https://api.timeular.com/api/v2', api_key='', api_secret=''):
        super(Timeular, self).__init__(base_url)
        self._api_key = api_key
        self._api_secret = api_secret
        if not self.get_access_token():
            raise ValueError('Check base_url and the route to get your access token')
        self.activities = Activities(base_url, self._access_token)
        self.devices = Devices(base_url, self._access_token)
        self.tracking = Tracking(base_url, self._access_token)

    def set_api_key(self, api_key):
        self._api_key = api_key

    def set_api_secret(self, api_secret):
        self._api_secret = api_secret

    def get_access_token(self):
        result = self._make_response('/developer/sign-in', method="post", json={'apiKey': self._api_key, 'apiSecret': self._api_secret}, need_auth=False)
        if not result:
            return False
        self._access_token = result['token']
        return result


class Activities(API):
    _BASE_URL = '/activities'

    def __init__(self, base_url, access_token):
        super(Activities, self).__init__(base_url + self._BASE_URL, access_token)

    @check_token
    def get(self):
        return self._make_response()


class Devices(API):
    _BASE_URL = '/devices'

    def __init__(self, base_url, access_token):
        super(Devices, self).__init__(base_url + self._BASE_URL, access_token)

    @check_token
    def get(self):
        return self._make_response()

class Tracking(API):
    _BASE_URL = '/tracking'

    def __init__(self, base_url, access_token):
        super(Tracking, self).__init__(base_url + self._BASE_URL, access_token)

    @check_token
    def get(self):
        return self._make_response()


scope = "user-modify-playback-state"
token = util.prompt_for_user_token(config.username, scope, config.spotify_id, config.spotify_secret, "http://localhost:8888/callback")

if token:
    sp = spotipy.Spotify(auth=token)
else:
    print ("Can't get token for" + username)

with open("playlists.json") as f:
    data = json.load(f)

activity_name = ""
while activity_name != "Off":
    api = Timeular(api_key=t_key, api_secret=t_secret)

    tracking = api.tracking.get()["currentTracking"]
    activity = tracking["activity"]

    if activity_name != activity["name"]:
        activity_name = activity["name"]

        if activity_name in data:
            sp.start_playback(device_id=config.device, context_uri=data[activity_name])
        elif activity_name == "Random":
            activity_name_rand, uri = random.choice(list(data.items()))
            sp.start_playback(device_id=config.device, context_uri=data[activity_name_rand])

    time.sleep(3)
