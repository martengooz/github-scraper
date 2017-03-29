import requests
import pause
import json
import time
import datetime
import re
import grequests
import sys
import os

page = "hej"
baseurl = "https://api.github.com/"

# Get token
f = open("token","r")
username = f.readline()
token = f.readline().rstrip('\n')
f.close()


#read data
with open('reposfinal') as data_file:
	data = json.load(data_file)

def printProgressBar (i):
	sys.stdout.write("\r%d%% " % i)
	sys.stdout.flush()

def writeJson(data, filename):
	print "\tSaving to file " + filename
	f = open(filename,"a+")
	f.write(json.dumps(data, indent=2))
	f.close()

def checkRateLimit():
	ratelimit = json.loads(requests.get(baseurl + "rate_limit", auth=(username, token)).text)
	requestsleft = ratelimit['rate']['remaining']
	resettime = ratelimit['rate']['reset']
	if (requestsleft < 10):
		print "Pausing until " + datetime.datetime.fromtimestamp(resettime).strftime('%Y-%m-%d %H:%M:%S')
		pause.until(resettime + 10)
	return str(requestsleft)

def getPage(url, n):
	global page
	checkRateLimit()
	page = requests.get(url, params={'per_page': 100, 'page': n}, auth=(username, token)).text
	if page == "[]":
		print "dis is empty"
	return page

donerepos = []
with open('saved', 'a+') as saveddata:
	saveddata.write("")
	save = json.load(saveddata)
	for saverepo in save:
		donerepos.append(saverepo['full_name'])
		print "Aleady exists " + saverepo['full_name']

f = open("saved","a+") 
f.seek(-2, os.SEEK_END)
f.truncate()
f.write(",")
f.close()

try:
	z = 1
	for repo in data:
		printProgressBar(z/len(data))
		z += 1
		if repo['full_name'] in donerepos:
			continue
		if (len(repo['commit']) == 30):
			n = 1
			lista = []

			while getPage(repo['url'] + "/commits", n) != "[]":
				jason = json.loads(page)
				for commit in jason:
					cleancommit = { 'sha': commit['sha'], 'date': commit['commit']['committer']['date']}
					lista.append(cleancommit)
					n += 1

			repo['commit'] = lista
			print "\tDone with" + repo['full_name']
			writeJson(repo, "saved")
			f = open("saved","a") 
			f.write(",\n")
			f.close()

		else:   
			writeJson(repo, "saved")
			f = open("saved","a") 
			f.write(",\n")
			f.close()

except KeyboardInterrupt:
	f = open("saved","a+") 
	f.seek(-2, os.SEEK_END)
	f.truncate()
	f.write("]")
	f.close()
	pass
