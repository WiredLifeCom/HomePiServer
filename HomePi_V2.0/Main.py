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


class JsonEncoder:
    def __init__(self, obj):
        self.userData = obj

    def Encode(self):
        result = json.dumps(self.userData.__dict__, sort_keys=True, indent=4)
        return result

class Zone(object):
    arrival = ""
    departure = ""
    radius = 0
    material = ""
    longitude = 0.0
    latitude = 0.0

class User(object):
    username = ""

class Unload(object):
    unload = ""
    materials = []
    user = User()
    zones = [Zone()]

def as_Unload(d):
    i = Unload()
    i.__dict__.update(d)
    return i

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
            print "Opening file: [ " + fileList[fileNumber] + " ] ..."
            AreYouThere(fileList[fileNumber])


# Method to ping the file from in Parameter
def AreYouThere(name):
    jsonObject = json.loads(open(name).read(), object_hook=as_isHomeNow)
    address = jsonObject.ipAddress
    print "The address to ping: { ", address + " }"
    if jsonObject.isHome == "true":
        res = os.system("ping -n 1 " + address)
        if res == 0:
            print "***Ping to { ", address, " } had a response, user is home***"
        else:
            print "***Ping to { ", address, " } failed!***"
            fileManager = open('{0}.json'.format(jsonObject.username), "w")
            jsonObject.isHome = "false"
            fileManager.writelines(json.dumps(jsonObject, default=lambda y: y.__dict__, indent=4, sort_keys=True))
            fileManager.close()
            # r = requests.post("http://10.2.15.95:7070/onlinestatus", data="o.isHome")

            # Update MainPi that the user is ot home anymore
    else:
        print "***The user with address : { ", address, " } is not home!***"


#Method for app to say I'm home
#@app.route('/HoneyImHome', methods=['POST'])
def SaveUserState(updateuser):
        print "Save user state got this ***", updateuser
        jsonObject = json.loads(updateuser, object_hook=as_isHomeNow)
        fileManager= open('{0}.json'.format(jsonObject.username), "w")
        fileManager.writelines(json.dumps(json.loads(updateuser), indent=4, sort_keys=True))
        fileManager.close()
        #r = requests.post("http://10.2.15.95:7070/onlinestatus", data=updateuser)
        #return Response(status=r.status_code)
        return ""

#Sends JSON package from mobile app to Main Pi Server
@app.route('/unload', methods=['POST'])
def SendPackageToMainPi():
    jsonObject = json.loads(request.data, object_hook=as_Unload)
    if jsonObject.materials is None:
        return Response(status=422)
    print "unload *** ", request.data
    #r = requests.post("http://10.1.17.115:7070/unload", data=request.data)
    #print(r.status_code, r.reason)
    print "Unload *** This is ip", request.remote_addr
    SaveUserState(json.dumps({"username": jsonObject.user.username,
                              "isHome": "true", "ipAddress": request.remote_addr}))
    #return Response(status=r.status_code)
    return ""



def exit_handler():
    thread.mainRunning = False


atexit.register(exit_handler)

if __name__ == "__main__":
    app.debug = True
    thread = Thread(target=threadedFunction)
    #thread.start()
    app.run(host="10.1.16.193", port=5000, debug=True, use_reloader=False)

