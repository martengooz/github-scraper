import requests
from requests.auth import HTTPBasicAuth
from random import randint
import pause
import json
import time
import datetime

# Get token
f = open("token","r") 
username = f.readline()
token = f.readline()
f.close()

# Urls
baseurl = "https://api.github.com/"

## Write the json data to a file specified by `filename`
def writeJson(data, filename):
	f = open(filename,"a") 
	f.write(json.dumps(data, indent=2))
	f.close()


## Get a list of 100 random repos
def repList():
	pageparam = {	'since':randint(1, 83570000), # Seems like this is near the upper limit of repo ids right now
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
	if (requestsleft < 100):
		print "Pausing until " + datetime.datetime.fromtimestamp(resettime).strftime('%Y-%m-%d %H:%M:%S')
		pause.until(resettime + 10)
	print "Requests left: " + str(requestsleft)

## Remove unwanted repos
def filterRepos(repos):
	# Remove forks
	noforks = [repo for repo in repos if repo['fork'] == False]
	nonempty = []
	
	for repo in noforks:
		#Remove unnesseary keys from norepo
		keys = ["id","full_name","url", "commits_url"]
		res = { key: repo[key] for key in keys }

		# Get repo info
		r = requests.get(res['url'], auth=(username, token))
		repoinfo = json.loads(r.text)
		
		#Remove repos smaller than 500 bytes
		if repoinfo['size'] > 500:
			#Remove unnesseary keys from repoinfo
			keys = [ "size", "stargazers_count", "watchers_count", "language", "has_issues", "has_downloads", "has_pages", "forks_count", "open_issues_count", "forks", "open_issues", "watchers", "network_count", "subscribers_count", "created_at", "updated_at", "pushed_at"]
			notempty = { key: repoinfo[key] for key in keys }

			# Merge noforks info with repos not empty
			temp = res.copy()
			temp.update(notempty)

			nonempty.append(temp)

	res = nonempty

	
	return res, len(res)


## Main script
totalRepos = 0
for n in range(1,3):
	checkRateLimit()

	repos, numRepos = filterRepos(repList())
	totalRepos += numRepos
	print "Found " + str(totalRepos) + " repositories"

	writeJson(repos, "repos")
