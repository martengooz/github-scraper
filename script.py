import requests
from requests.auth import HTTPBasicAuth
from random import randint
import pause
import json
import time
import datetime
import re
import grequests
import sys

# Get token
f = open("token","r") 
username = f.readline()
token = f.readline().rstrip('\n')
f.close()

# Urls
baseurl = "https://api.github.com/"

def printProgressBar (i):
    sys.stdout.write("\r%d%% " % i)
    sys.stdout.flush()

def asyncRequest(urls, param):
	rs = (grequests.get(u, params = param, auth=(username, token)) for u in urls)
	return grequests.map(rs) 

## Write the json data to a file specified by `filename`
def writeJson(data, filename):
	print "\tSaving to file " + filename
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
	return str(requestsleft)

## Remove unwanted repos
def filterRepos(repos):
	print "Filtering repos"
	# Remove forks
	noforks = [repo for repo in repos if repo['fork'] == False]
	nonempty = []
	i = 0
	numnoforks = len(noforks)
	for repo in noforks:
		i+= 1
		printProgressBar((i*100/numnoforks))
		#Remove unnesseary keys from norepo
		keys = ["id","full_name","url", "commits_url"]
		res = { key: repo[key] for key in keys }

		# Get repo info
		r = requests.get(res['url'], auth=(username, token))
		repoinfo = json.loads(r.text)
		
		if repoinfo.has_key('message'):
			print "Abort mission"
			continue
			
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


def getcommits(repos):
	combase = 'https://api.github.com/repositories/'
	totalcommits = 0
	print "\tGathering " + repo['full_name'] + " commits"
	r = requests.get(repo['url'] + "/commits", auth=(username, token))
	commits = json.loads(r.text)
	cleancommits = []
	while(True):
		checkRateLimit()
		headers = r.headers
		commits = json.loads(r.text)

		urls = [commit['url'] for commit in commits]
		rs = asyncRequest(urls, [])

		for resp in rs:
			totalcommits += 1
			commitjson = json.loads(resp.text)
			cleancommit = { 'sha': commitjson['sha'], 'date': commitjson['commit']['committer']['date'], 'stats':commitjson['stats']}
			cleancommits.append(cleancommit)
			printProgressBar(totalcommits)
		
		if 'link' in headers:
			link = headers['link']
			m = re.search('rel="next"',link)
			if m != None:
				m = re.search("\d+\/commits\?page=\d+", link)
				comurl = m.group(0)
				r = requests.get(combase + comurl, params={'per_page': 100}, auth=(username, token))				
			else:
				break
		else:
			break
	repo['commit'] = cleancommits
	repo['num_commits'] = len(cleancommits)
	print "\tdone"
	return repo
## Main script
totalRepos = 0
while(True):
	print "\n\nRequests left: " + str(checkRateLimit())

	repos, numRepos = filterRepos(repList())
	totalRepos += numRepos
	print "Found " + str(totalRepos) + " repositories\n"

	for repo in repos: 
		commits = getcommits(repo)
		writeJson(commits, "repos")
		f = open("repos","a") 
		f.write(",\n")
		f.close()
