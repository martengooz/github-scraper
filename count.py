import json

with open('repos') as data_file:    
    data = json.load(data_file)

i = 0
for repo in data:
        i += 1
print "repos = " + str(i)

j = 0
for repo in data:
        for commit in repo['commit']:
                j+=1
print j

