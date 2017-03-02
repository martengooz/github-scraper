import requests
from requests.auth import HTTPBasicAuth
from random import randint
import pause
import json
import time
# Get token
f = open("token","r") 
username = f.readline()
token = f.readline()
f.close()

# Urls
baseurl = "https://api.github.com/"

## Get a list of 100 random repos
def repList():
	pageparam = {	'since':randint(1, 83570000), 
					'page':randint(1,5),
					'per_page':100 } 

	r = requests.get(baseurl + "repositories",params=pageparam, auth=(username, token))
	res = json.loads(r.text)
	if res == []: # if we recieved an empty page
		repList()
	return res

## Halt program until rate limit reset
def checkRateLimit():
	ratelimit = json.loads(requests.get(baseurl + "rate_limit", auth=(username, token)).text)
	requestsleft = ratelimit['rate']['remaining']
	resettime = ratelimit['rate']['reset']
	if (requestsleft > 10):
		pause.until(resettime + 10)


print repList()
