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
weektotallist = []
longeststreaklist = []
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
		i=1
		while end <= datetime.datetime(1990, 11, 21, 16, 30) or start <=datetime.datetime(1990, 11, 21, 16, 30):
			print endtime
			print starttime
			endtime = lista[i]
			starttime = lista[len(lista)-(i+1)]
			endtime = endtime['date']
			starttime = starttime['date']
			endtime = endtime.encode('ascii')
			starttime = starttime.encode('ascii')

			starttime = starttime[:-1]
			endtime = endtime[:-1]
			start =	dateutil.parser.parse(starttime)
			end = dateutil.parser.parse(endtime)
			i += 1

		numweeks = relativedelta(end,start).years*52 + \
		relativedelta(end,start).months*4 + \
		relativedelta(end,start).weeks + 1

		lista = lista[::-1]

		currentweek = start + relativedelta(weeks=+1)

		commitsPerWeek = []
		commitsThisWeek = 0
		longeststreak = 0
		currrentstreak = 0
		for commit in lista:
			if dateutil.parser.parse(commit['date'].encode('ascii')[:-1]) < currentweek:
				commitsThisWeek += 1
				currrentstreak = 0
			else:
				commitsPerWeek.append(commitsThisWeek)
				longeststreak = longeststreak if currrentstreak < longeststreak else currrentstreak
				if commitsThisWeek == 0:
					currrentstreak += 1
				#if currrentstreak > 600:
					#print start
					#print end
					#print repo['full_name']

				commitsThisWeek = 0
				currentweek = currentweek + relativedelta(weeks=+1)

		#print longeststreak
		commitsPerWeek.append(commitsThisWeek)

		weektotallist.append(commitsPerWeek)

		#popularity = repo['forks_count']
		#popularity = repo['stargazers_count']
		popularity = repo['forks_count'] + repo['stargazers_count'] + repo['subscribers_count']
		popularitylist.append(popularity)
		longeststreak += 1
		longeststreaklist.append(longeststreak)
		#popularitylist.append([popularity]*len(commitsPerWeek))

print len(lista)
y = popularitylist
x = longeststreaklist

slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)
x = numpy.array(x)
predict_y = intercept + slope * x
plt.scatter(x, y)
plt.plot(x, predict_y, 'k-', color="g", label="r = " + "{0:.4f}".format(r_value) +"\n" + "p = " + "{0:.4f}".format(p_value))

print(str(r_value) +", " + str(p_value))
lims = plt.xlim()
plt.xlim([lims[0], lims[1]])
plt.ylabel("Stars + forks + subscribers")
plt.xlabel("Longest inactive streak (weeks)")
plt.title("Weekly inactivity streak (SFS)")
plt.legend()
plt.show()
