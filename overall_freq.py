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
frequencylist = []
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

		nummonths = relativedelta(end,start).years*365 + \
		relativedelta(end,start).months*30 + \
		relativedelta(end,start).weeks*7 + \
		relativedelta(end,start).days

		frequency = float(len(lista)) / float(nummonths)

		#if frequency > 2 :
		#	continue

		frequencylist.append(frequency)
		popularity = repo['forks_count']
		#popularity = repo['stargazers_count']
		#popularity = repo['forks_count'] + repo['stargazers_count'] + repo['subscribers_count']
		popularitylist.append(popularity)


y = popularitylist
x = frequencylist

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
plt.ylabel("Forks")
plt.title("Average daily commits in repo lifetime (Forks)")
plt.legend()
plt.show()
