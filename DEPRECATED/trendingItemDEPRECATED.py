import pandas as pd

retailData = pd.read_csv('retailData.csv')
mean = {}
keys = retailData.keys()
l = len(retailData)
for j in range(3,33):
	total = 0
	num = 0
	for i in range(l):
		if retailData[keys[j]][i] == 0:
			continue
		else:
			num += retailData[keys[j]][i]
			total += 1
	mean[keys[j]] = num/total
	print "mean of " + keys[j] + ' is ' + str(mean[keys[j]])
	
print mean

trends = []
for i in range(l):
	max = 0
	item = None
	for j in range(3,33):
		n = retailData[keys[j]][i]/mean[keys[j]]
		if n > max : 
			max = n
			item = keys[j]
	trends += [(retailData['date'][i],retailData['zip'][i],retailData['city'][i],item)]
	print('Trending Item on ' + str(retailData['date'][i]) + ' in city ' + str(retailData['city'][i]) + ' was ' + str(item) )

df = pd.DataFrame(data = trends, columns=['Date', 'Zip Code', 'City', 'Item'])
df.to_csv('trendingItem.csv')
