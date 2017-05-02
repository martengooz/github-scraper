import numpy
import json
import time
import datetime
from dateutil.relativedelta import *
import dateutil
import dateutil.parser
from scipy.stats.stats import pearsonr
import matplotlib.pyplot as plt
import scipy
from operator import truediv

with open('repos') as data_file:
    data = json.load(data_file)
popularitylist = []



#print stars
commitsPermonth = []
for repo in data:
	if repo['stargazers_count'] > 10 and repo['forks_count'] > 1 and repo['subscribers_count'] > 10 and len(repo['commit']) >100:
		lista = repo['commit']

		endtime = lista[0]
		starttime = lista[len(lista)-1]
		endtime = endtime['date']
		starttime = starttime['date']
		endtime = endtime.encode('ascii')
		starttime = starttime.encode('ascii')

		starttime = starttime[:-1]
		endtime = endtime[:-1]
		start =	dateutil.parser.parse(starttime)
		end = dateutil.parser.parse(endtime)


		#lista = lista[::-1]
		#currentmonth = start + relativedelta(months=+1)
		currentmonth = end - relativedelta(months=+1)

		commitsThismonth = 0

		for commit in lista:
			if dateutil.parser.parse(commit['date'].encode('ascii')[:-1]) > currentmonth:
				commitsThismonth += 1
			else:
				break
				commitsPermonth.append(commitsThismonth)

		#print longeststreak
		commitsThismonth = commitsThismonth/30.4368499 # convert to commits per hour
		commitsPermonth.append(commitsThismonth)

		#popularity = repo['forks_count']
		popularity = repo['stargazers_count']
		#popularity = repo['forks_count'] + repo['stargazers_count'] + repo['subscribers_count']
		popularitylist.append(popularity)


y = popularitylist
x = commitsPermonth
print "AVG = " + str(sum(x) / float(len(x)))
slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)
x = numpy.array(x)
predict_y = intercept + slope * x
plt.scatter(x, y)
plt.plot(x, predict_y, 'k-', color="g", label="r = " + "{0:.4f}".format(r_value) +"\n" + "p = " + "{0:.4f}".format(p_value))

print(str(r_value) +", " + str(p_value))
lims = plt.xlim()
plt.xlim([lims[0], lims[1]])
plt.xlabel("Commit/day")
plt.ylabel("Stars")
plt.title("Average daily commits last month (Stars)")
plt.legend()
plt.show()
