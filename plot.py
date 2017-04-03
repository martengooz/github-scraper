import matplotlib.pyplot as plt
import json



with open('saved') as data_file:    
    data = json.load(data_file)

max = 0
for repo in data: 
	if len(repo['commit']) > max:
		max = len(repo['commit'])


numberBars = len(data)
y = [0] * numberBars

sizes = []
for repo in data: 
	if len(repo['commit']) == 30:
		print repo['full_name']
	sizes.append(len(repo['commit']))

#sizes.sort()




plt.scatter(range(numberBars), sizes)
plt.show()

"""
#sizes.sort()

print sizes[len(sizes) -10]

n = 1
print max
for size in sizes:
	#print n*max/(numberBars)
	if (size <= n*max/(numberBars)):
		y[n-1] += 1
	else:
		n += 1
print y

plt.hist(sizes, bins=np.arange(data.min(), data.max()+1))
print y
N = len(y)
width = 1/1.5
plt.bar(x, y, width, color="blue")

fig = plt.gcf()
plt.show()
"""
