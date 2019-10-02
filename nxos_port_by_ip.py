#Import libraries
import json
import requests
import getpass

i=0

my_headers = {'content-type':'application/json-rpc'}
url = "https://10.24.7.102/ins"

#Get credentials need to add password check
print("\n")
username = input("Username: ")
password = getpass.getpass()
print("\n")
#ip_addr = input("IP Address of Device: ")

#request packages
requests.packages.urllib3.disable_warnings()

#JSON-RPC payload from sandbox
payload = [{"jsonrpc": "2.0",
			"method": "cli",
			"params": {"cmd": "sh int status",
						"version": 1},
			"id": 1}
			]

#Grab response off Nexus
response = requests.post(url, data=json.dumps(payload), headers=my_headers, auth=(username, password), verify=False).json()

#Print finding
d = response['result']['body']['TABLE_interface']['ROW_interface']

print(d[0])

	
