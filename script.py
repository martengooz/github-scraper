import requests
from requests.auth import HTTPBasicAuth

# Get token
f = open("token","r") 
username = f.readline()
token = f.readline()
f.close()

# Urls
baseurl = "https://api.github.com/"


r = requests.get(baseurl + "repositories", auth=(username, token))
print r.text