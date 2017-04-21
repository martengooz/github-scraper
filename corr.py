import numpy
import json
import time
import datetime
import dateutil
import dateutil.parser
from scipy.stats.stats import pearsonr
import matplotlib.pyplot as plt
import scipy
from operator import truediv

with open('repos') as data_file:    
    data = json.load(data_file)
popularity = []
for repo in data:
	if repo['stargazers_count'] > 10 and len(repo['commit']) >300:
		popularity.append(repo['stargazers_count'])

#print stars
difflist = []
frekv = []
for repo in data:
	if repo['stargazers_count'] > 10 and len(repo['commit']) >300:
		repofrekv = [0,0,0]
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
		start = int(time.mktime(start.timetuple()))
		end = int(time.mktime(end.timetuple()))
		

		diff = end - start
		difflist.append(diff/60/60)
		third = start + diff/3
		twothird = start + diff/3*2
		
		third_date = datetime.datetime.fromtimestamp(third)
		twothird_date = datetime.datetime.fromtimestamp(twothird)
		
		"""print "start" + str(datetime.datetime.fromtimestamp(start))
		print third_date
		print twothird_date
		print "end" + str(datetime.datetime.fromtimestamp(end))"""
		"""
		for date in lista:
			datum = dateutil.parser.parse(date['date'].encode('ascii')[:-1])
			#print datum
			#print third_date
			if datum <= third_date:
				repofrekv[0] = repofrekv[0] + 1
			elif datum <= twothird_date:
				repofrekv[1] = repofrekv[1] + 1
			else:
				repofrekv[2] = repofrekv[2] + 1
		
		repofrekv[0] = float(repofrekv[0])# / float(len(lista))
		repofrekv[1] = float(repofrekv[1])# / float(len(lista))
		repofrekv[2] = float(repofrekv[2])# / float(len(lista))

		frekv.append(repofrekv)"""
		#print frekv
		frekv.append(len(repo['commit']))

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

x = map(truediv, frekv, difflist)
print x

slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, popularity)
x = numpy.array(x)
predict_y = intercept + slope * x
plt.scatter(x, popularity)
plt.plot(x, predict_y, 'k-', color="g", label="r = " + "{0:.4f}".format(r_value) +"\n" + "p = " + "{0:.4f}".format(p_value))


print(str(r_value) +", " + str(p_value))
lims = plt.xlim()
plt.xlim([lims[0], lims[1]])
plt.xlabel("Commit/hour") 
plt.ylabel("Stars")
plt.title("Average frequency throughout the project lifetime")
plt.legend()
plt.show()
			
