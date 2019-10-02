#Import libraries
import json
import getpass
import base64
import requests

#Set device IP and API path
device = input("enter url of ASA: ")
api_path = "/api/cli"
url = device + api_path

#CLI Commands to run 
post_data = {
  "commands": [
    "sh ver | i System image|Hardware|Model Id",
	"sh nameif"
  ]
}

#Content header for requests
my_headers = {'Content-Type':'application/json'}

#disable warning
requests.packages.urllib3.disable_warnings()

#Get credentials need to add password check
print(device, "...")
print("\n")
username = input("Username: ")
password = getpass.getpass()
print("\n")
#start mark
print("////////// Commands Run & Response //////////")
print("\n")

#get response from ASA API 
response = requests.post(url, json.dumps(post_data), headers=my_headers, auth=(username, password), verify=False).json()

#Grab dictionary containing body of typical output
response = response['response']

for i in range(len(response)):
	print('----- %s -----' % post_data['commands'][i])
	print('\n')
	print(response[i])
	print("\n")
#End mark
print("//////////        COMPLETE         //////////") 
print('\n')

