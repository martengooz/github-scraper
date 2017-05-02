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
	if repo['stargazers_count'] > 4 and len(repo['commit']) >100:
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
			else:
				commitsPerWeek.append(commitsThisWeek)
				currrentstreak += 1
				longeststreak = longeststreak if currrentstreak < longeststreak else currrentstreak
				if commitsThisWeek == 0:
					currrentstreak = 0
				commitsThisWeek = 0
				currentweek = currentweek + relativedelta(weeks=+1)

		#print longeststreak
		commitsPerWeek.append(commitsThisWeek)

		weektotallist.append(commitsPerWeek)

		popularity = repo['stargazers_count']
		popularitylist.append(popularity)
		longeststreak += 1
		longeststreaklist.append(longeststreak)
		#popularitylist.append([popularity]*len(commitsPerWeek))

print popularitylist
print longeststreaklist

"""
list0 = []
for n in frekv:
	list0.append(n[0])
list1 = []
for n in frekv:
	list1.append(n[1])
list2 = []
for n in frekv:
	list2.append(n[2])

#print list1
#corr = numpy.corrcoef(stars,list1)[1,0]
slope0, intercept0, r_value0, p_value0, std_err0 = scipy.stats.linregress(list0, popularity)
slope1, intercept1, r_value1, p_value1, std_err1 = scipy.stats.linregress(list1, popularity)
slope2, intercept2, r_value2, p_value2, std_err2 = scipy.stats.linregress(list2, popularity)


x0 = numpy.array(list0)
x1 = numpy.array(list1)
x2 = numpy.array(list2)

predict_y0 = intercept0 + slope0 * x0
predict_y1 = intercept1 + slope1 * x1
predict_y2 = intercept2 + slope2 * x2


#print pearsonr(stars,list1)

plt.scatter(list0, popularity)
#plt.scatter(list1, popularity, color="g")
#plt.scatter(list2, popularity, color="m")

plt.plot(x0, predict_y0, 'k-', color="g", label="r = " + "{0:.4f}".format(r_value0) +"\n" + "p = " + "{0:.4f}".format(p_value0))
#plt.plot(x1, predict_y1, 'k-', color="b", linewidth=2.0, label="r = " + "{0:.4f}".format(r_value1) +"\n" + "p = " + "{0:.4f}".format(p_value1))
#plt.plot(x2, predict_y2, 'k-', linewidth=2.0, label="r = " + "{0:.4f}".format(r_value2) +"\n" + "p = " + "{0:.4f}".format(p_value2))

"""
x = popularitylist
y = longeststreaklist

slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)
x = numpy.array(x)
predict_y = intercept + slope * x
plt.scatter(x, y)
plt.plot(x, predict_y, 'k-', color="g", label="r = " + "{0:.4f}".format(r_value) +"\n" + "p = " + "{0:.4f}".format(p_value))

print(str(r_value) +", " + str(p_value))
lims = plt.xlim()
plt.xlim([lims[0], lims[1]])
plt.xlabel("Commit/hour")
plt.ylabel("Stars")
plt.title("Average frequency throughout the project lifetime")
plt.legend()
plt.show()
