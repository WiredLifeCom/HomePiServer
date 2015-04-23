from flask import Flask
from flask import jsonify
from flask.json import JSONEncoder
import json
import requests

app = Flask(__name__)

class UserData:
	def __init__(self):
		self.userName = 'Julian'
	def JSONEncode(self, userData):
		return json.dumps(self, default=lambda o: o.__dict__)

@app.route('/HoneyImHome/<userData>')
def WelcomeHome(userData):
	try:
		json.loads(userData)
		print 'json encode = success'
		SendPackageToMainPi(userData)
	except: 
		print 'json encode = fail'
		bPack = UserData()
		bPackDone = bPack.JSONEncode(userData)
		WelcomeHome(bPackDone)

		
#Sends JSON package to Main Pi Server
def SendPackageToMainPi(userData):
	print 'package sent'

#Testcases for JSON encoding
bPack = UserData()	
print 'pass 1'
WelcomeHome(bPack)
print 'pass 2'
bPackDone = bPack.JSONEncode(bPack)
print 'pass 3'
WelcomeHome(bPackDone)	
print 'pass 4'

#Testcases for WelcomeHome try except recursion	
userData = "Julian"
print 'json encode = fail expected, then succeed'
WelcomeHome(userData)

	
if __name__ == "__main__":
	app.debug = True
	app.run()


