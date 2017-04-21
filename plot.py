import matplotlib.pyplot as plt
import json



with open('reposextra') as data_file:    
    data = json.load(data_file)

max = 0
for repo in data: 
	if repo['stargazers_count']> max:
		max = repo['stargazers_count']


numberBars = 0
y = [0] * numberBars

sizes = []
for repo in data: 
	if repo['stargazers_count'] > -1: #and len(repo['commit']) > 100:	
		numberBars += 1
		sizes.append(len(repo['commit']))

sizes.sort()

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
