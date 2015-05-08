__author__ = 'J'
import requests


if __name__ == '__main__':
    requests.post("http://10.1.16.193:5000/HoneyImHome", data='{ "username" : "James",   "isHome" : "true",  "ipAddress" : "10.1.2.12"}')
    requests.post("http://10.1.16.193:5000/HoneyImHome", data='{ "username" : "Paul",   "isHome" : "true",  "ipAddress" : "10.1.2.12"}')
    requests.post("http://10.1.16.193:5000/HoneyImHome", data='{ "username" : "Bill",   "isHome" : "true",  "ipAddress" : "10.1.16.193"}')

