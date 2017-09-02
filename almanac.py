import pandas as pd
import numpy as np
import html5lib, time, os.path
from datetime import timedelta

startFrom = 0 #srishti
#startFrom = 100000 #swati
#startFrom = 200000 #sonaali

def getWeather(date):
       zipDate = str(int(date['zip'])) + "/" + str(date['date'])
       site = "http://www.almanac.com/weather/history/zipcode/" + zipDate
       try:
              weather = pd.read_html(io=site, encoding='utf-8')
              weather = weather[1].T
       except:
              print "Error encountered :/"
       if weather is None:
              return "None"
       weather.insert(0, 'Date', zipDate)
       weather.columns = range(weather.shape[1])
       return weather.iloc[1]

#initialisations
df = pd.read_csv('retailData.csv')
dates = df.drop_duplicates(subset=['zip', 'date']).filter(['zip', 'date'])

if os.path.exists('output_almanac.csv'):
       weatherTable = pd.read_csv('output_almanac.csv', encoding="utf-8", header=None)
       print 'Imported old data'
else:
       print 'No output data to import. Creating empty dataframe.'
       weatherTable = pd.DataFrame()
start = time.time()

for counter, x in dates.loc[startFrom + len(weatherTable.index):].iterrows():
       print "Getting weather for tuple " + str(counter) + "/235959 : " 
       weather = getWeather(x)
       weatherTable = weatherTable.append(weather)
       if counter % 10 == 0 :
               weatherTable.to_csv('output_almanac.csv', encoding="utf-8", header=None, index=False)
               print "Time elapsed: " + str(timedelta(seconds=(time.time() - start)))

#weatherTable.columns = ['Temp','MinTemp','MeanTemp','MaxTemp','Pressure and Dew Point','Mean Sea Level Pressure','Mean Dew Point','Precipitation','Total PrecipitationRain and/or melted snow rep','Visibility','Snow DepthLast report for the day if reported','Wind Speed and Gusts','Mean Wind Speed','Max Sustained Wind Speed','Max Wind Gust', 'Date', 'Zip']

