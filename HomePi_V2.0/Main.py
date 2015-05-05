from flask import Flask
from flask import request
from flask import Response
import json
import requests
import subprocess
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


# loop through json files and make a list, the call the are you there method to check if they are still home
def loopPeople():
    fileList = glob.glob('*.json')
    for fileNumber in range(0, len(fileList)):
        print fileList[fileNumber]
        AreYouThere(fileList[fileNumber])


#Method to ping the file from in Parameter
def AreYouThere(name):
    jsonData = open(name).read()
    print "Here is the jsonData", jsonData
    o = json.loads(jsonData, object_hook=as_isHomeNow)
    address = o.ipAddress
    print "The address we are pinging is", address
    if o.isHome == "true":
        #res = subprocess.call(['ping', '-c', '3', address])
        res = os.system("ping -n 1 " + address)
        if res == 0:
            print "ping to ", address, " OK"
        else:
            print "ping to ", address, " failed!"
            #Here too!!
    else:
        print "The user ", address, "is not home, I will not ping it"


#Method for app to say I'm home
@app.route('/HoneyImHome', methods=['POST'])
def SaveUserState():
    s = request.data
    o = json.loads(s, object_hook=as_isHomeNow)
    parsed = json.loads(s)
    x = json.dumps(parsed, indent=4, sort_keys=True)
    file = open('{0}.json'.format(o.username), "w")
    file.writelines(x)
    file.close()
    #Update Main Pi here that this user is home!!


#Sends JSON package to Main Pi Server
@app.route('/WelcomeHome', methods=['POST'])
def SendPackageToMainPi():
    #encoder = JsonEncoder(request.data)
    r = requests.post("http://10.2.15.95:7070/data", data=request.data)
    print(r.status_code, r.reason)
    return Response(status=r.status_code)


if __name__ == "__main__":
    app.debug = True
    loopPeople()
    app.run(host="10.1.2.12", port=5000)

