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
pageparam = {'since':randint(1, 3)}

## Main Loop

def reqList():
	r = requests.get(baseurl + "repositories", auth=(username, token))
	res = json.loads(r.text)


def checkRateLimit():
	ratelimit = json.loads(requests.get(baseurl + "rate_limit", auth=(username, token)).text)
	requestsleft = ratelimit['rate']['remaining']
	resettime = ratelimit['rate']['reset']
	if (requestsleft > 10):
		pause.until(resettime + 10)
