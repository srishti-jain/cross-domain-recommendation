#contains a folder of CSVs with 5 most popular item ids per day for Jan 2016.
import pandas as pd
import datetime, os, operator

homePath = "/home/srishti/"
month = "January"
path = homePath + month + "/"
if not os.path.exists(path):
	os.mkdir(path)

Jan1 = 1388534400 #January 1, 2014
oneDay = 86400
filename = 'ratings_Sports_and_Outdoors.csv'
csv_input = pd.read_csv(filename, header=None)

csv_input = csv_input[(csv_input[3] > Jan1) & (csv_input[3] < (Jan1 + oneDay*31))] #take entries for jan 2014 only. UNIX timestamp

beg = Jan1
for i in range(1, 32):
       reviews = csv_input[(csv_input[3] >= beg) & (csv_input[3] < beg + oneDay)]
       reviews = reviews[[0]].groupby([0])[0].count().nlargest(5).reset_index(name='top5')
       reviews = reviews[0] #DISCARD COUNTS
       reviews.to_csv(path + str(i) + '.csv', index=False, header=None)
       beg += oneDay

#Convert UNIX timestamp to normal:
#csv_input[3] = csv_input[3].apply(lambda x:datetime.datetime.fromtimestamp(int(x)).strftime('%Y-%m-%d %H:%M:%S')) 

