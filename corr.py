import numpy
import json
import time
import datetime
import dateutil
import dateutil.parser

with open('saved') as data_file:    
    data = json.load(data_file)
stars = []
for repo in data:
	repostars = []
	repostars.append(repo['stargazers_count'])
	repostars.append(repo['stargazers_count'])
	repostars.append(repo['stargazers_count'])
	stars.append(repostars)

#print stars

frekv = []
for repo in data:
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
	third = start + diff/3
	twothird = start + diff/3*2
	
	third_date = datetime.datetime.fromtimestamp(third)
	twothird_date = datetime.datetime.fromtimestamp(twothird)
	
	"""print "start" + str(datetime.datetime.fromtimestamp(start))
	print third_date
	print twothird_date
	print "end" + str(datetime.datetime.fromtimestamp(end))"""
	
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
	
	repofrekv[0] = float(repofrekv[0]) / float(len(lista))
	repofrekv[1] = float(repofrekv[0]) / float(len(lista))
	repofrekv[2] = float(repofrekv[0]) / float(len(lista))
	frekv.append(repofrekv)

corr = numpy.corrcoef(stars,frekv)
#print numpy.corrcoef(stars,frekv)
			
