__author__ = 'J'
import requests


if __name__ == '__main__':
    while True:
        requests.post("http://10.1.17.115:7070/unload", data='{"user": { "username": "bejbejpomp"}, "zones": [{ "arrival": "2015-04-21T11:42:11.000+02:00","departure": "2015-04-21T11:58:32.000+02:00", "latitude": 55.61592, "longitude": 12.987113, "material": "Dirt", "radius": 20}], "materials":["Dirt", "Dirt"],"unload": "2015-04-21T13:04:54.000+02:00"}')

    #requests.post("http://10.1.17.115:7070/onlinestatus", data='{"username": "bejbejpomp", "isHome": false, "ipAddress": "1.1.1.1"}')