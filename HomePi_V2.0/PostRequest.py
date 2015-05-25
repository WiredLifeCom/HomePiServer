__author__ = 'J'
import requests


if __name__ == '__main__':
    requests.post("http://10.1.16.193:5000/unload", data='{"user": { "username": "TestUser"}, "zones": [{ "arrival": "2015-04-21T11:42:11.000+02:00","departure": "2015-04-21T11:58:32.000+02:00", "latitude": 55.61592, "longitude": 12.987113, "material": "Dirt", "radius": 20}],"unload": "2015-04-21T13:04:54.000+02:00"}')

