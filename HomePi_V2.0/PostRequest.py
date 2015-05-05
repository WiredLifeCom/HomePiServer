__author__ = 'J'
import requests


if __name__ == '__main__':
    requests.post("http://10.1.2.12:5000/HoneyImHome", data='{ "username" : "James",   "isHome" : "true",  "ipAddress" : "10.1.2.12"}')

