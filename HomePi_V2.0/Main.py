from flask import Flask
from flask import request
from flask import Response
from threading import Thread
from time import sleep
import atexit
import json
import requests
import glob
import os

app = Flask(__name__)

class Zone:
    def __init__(self):
        self.arrival = "2015-04-21T11:42:11.000+02:00"
        self.departure = "2015-04-21T11:58:32.000+02:00"
        self.latitude = 55.61592
        self.longitude = 12.987113


class Inventory:
    def __init__(self):
        self.resources = ["Dirt", "Dirt", "Stone"]
        self.items = ["DiamondPickAxe", "WoodenAxe"]


class User:
    def __init__(self):
        self.username = 'Julian'
        zone = Zone()
        inventory = Inventory()
        self.zones = [zone.__dict__]
        self.inventory = inventory.__dict__


class UserData:
    def __init__(self):
        user = User()
        self.user = user.__dict__
        self.unload = "2015-04-21T13:04:54.000+02:00"


class JsonEncoder:
    def __init__(self, obj):
        self.userData = obj

    def Encode(self):
        result = json.dumps(self.userData.__dict__, sort_keys=True, indent=4)
        return result


class imHomeNow(object):
    username = ""
    isHome = ""
    ipAddress = ""


def as_isHomeNow(d):
    i = imHomeNow()
    i.__dict__.update(d)
    return i

def threadedFunction():
    mainRunning = True
    while mainRunning:
        loopPeople()
        sleep(10)


# loop through json files and make a list, the call the are you there method to check if they are still home
def loopPeople():
    fileList = glob.glob('*.json')
    if fileList:
        for fileNumber in range(0, len(fileList)):
            print "Opening file: " + fileList[fileNumber] + "..."
            AreYouThere(fileList[fileNumber])


#Method to ping the file from in Parameter
def AreYouThere(name):
    jsonData = open(name).read()
    o = json.loads(jsonData, object_hook=as_isHomeNow)
    address = o.ipAddress
    print "The address to ping: ", address
    if o.isHome == "true":
        res = os.system("ping -n 1 " + address)
        if res == 0:
            print "***Ping to ", address, " had a response, user is home***"
        else:
            print "***Ping to ", address, " failed!***"
            file = open('{0}.json'.format(o.username), "w")
            o.isHome = "false"
            x = json.dumps(o, default=lambda y: y.__dict__, indent=4, sort_keys=True)
            file.writelines(x)
            file.close()
            # r = requests.post("http://10.2.15.95:7070/data", data="o.isHome")
            #Update MainPi that the user is ot home anymore
    else:
        print "***The user with address : ", address, " is not home!***"


#Method for app to say I'm home
@app.route('/HoneyImHome', methods=['POST'])
def SaveUserState():
    try:
        s = request.data
        o = json.loads(s, object_hook=as_isHomeNow)
        parsed = json.loads(s)
        x = json.dumps(parsed, indent=4, sort_keys=True)
        file = open('{0}.json'.format(o.username), "w")
        file.writelines(x)
        file.close()
        return Response(status = 200)
    except:
        return Response(status = 500)
    # r = requests.post("http://10.2.15.95:7070/data", data="o.isHome")
    #Update Main Pi here that this user is home!!


#Sends JSON package from mobile app to Main Pi Server
@app.route('/unLoad', methods=['POST'])
def SendPackageToMainPi():
    r = requests.post("http://10.2.15.95:7070/data", data=request.data)
    print(r.status_code, r.reason)
    return Response(status=r.status_code)


def exit_handler():
    thread.mainRunning = False
    thread.Join()

atexit.register(exit_handler)

if __name__ == "__main__":
    app.debug = True
    thread = Thread(target = threadedFunction)
    thread.start()
    app.run(host="10.1.16.193", port=5000, debug=True, use_reloader=False)

