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

def writeJson(data, filename):
	f = open(filename,"w") 
	f.write(json.dumps(data))
	f.close()


## Get a list of 100 random repos
def repList():
	pageparam = {	'since':randint(1, 83570000), # Seems like this is near the upper limit of repo ids right now
					'page':randint(1,5),
					'per_page':25 } 

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
	if (requestsleft < 100):
		pause.until(resettime + 10)
	print "Requests left: " + str(requestsleft)
	

def filterRepos(repos):
	# Remove forks
	res = [repo for repo in repos if repo['fork'] == False]
	nonempty = []
	
	# Remove all empty repos
	for repo in res:
		r = requests.get(repo['url'], auth=(username, token))
		repoinfo = json.loads(r.text)
		#Remove repos smaller than 500 bytes
		if repoinfo['size'] > 500:
			nonempty.append(repo)

	res = nonempty
	print "Found " + str(len(res)) + " repositories"
	return res

repos = repList()
filterRepos(repos)

print 
checkRateLimit()