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


page = "hej"

# Get token
f = open("token","r") 
username = f.readline()
token = f.readline().rstrip('\n')
f.close()

#read data
with open('repos') as data_file:    
    data = json.load(data_file)

def writeJson(data, filename):
	print "\tSaving to file " + filename
	f = open(filename,"a") 
	f.write(json.dumps(data, indent=2))
	f.close()

def getPage(url, n):
	global page
	page = requests.get(url, params={'per_page': 100, 'page': n}, auth=(username, token)).text
	if page == "[]":
		print "dis is empty"
	return page

for repo in data:
	if (len(repo['commit']) == 30):
		n = 1

		lista = []

		while getPage(repo['url'] + "/commits", n) != "[]":
			jason = json.loads(page)
			for commit in jason:
				print commit
				cleancommit = { 'sha': commit['sha'], 'date': commit['commit']['committer']['date'], 'stats':commit['stats']}
				lista.append(cleancommit)
			n += 1

		repo['commit'] = lista
		writeJson(repo, "saved")
		f = open("saved","a") 
		f.write(",\n")
		f.close()

	else:
		writeJson(repo, "saved")
		f = open("saved","a") 
		f.write(",\n")
		f.close()

