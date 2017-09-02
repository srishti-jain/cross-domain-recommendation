#Database: https://research.chicagobooth.edu/kilts/marketing-databases/dominicks
#sales data(ccount.dta): http://kilts.chicagobooth.edu/dff/store-demos-customer-count/ccount_stata.zip
#store data(demo.dta): http://kilts.chicagobooth.edu/dff/store-demos-customer-count/demo_stata.zip

import pandas as pd

#pd.set_option('max_rows', 20) #set maximum rows to be displayed

#read datasets
df = pd.read_stata('ccount.dta')
df2 = pd.read_stata('demo.dta')

#clean up sales data
df = df.apply(pd.to_numeric, errors = 'coerce').dropna() #remove rows with non-numeric values
df = df[df.columns[~df.columns.str.contains('coup')]] # drop rows with sales by coupons
df.drop(['mvpclub', 'promo'], axis=1, inplace=True)
df = df[df['date'] > 500000] #ignore negligible rows of 21st century
df['date'] = pd.to_datetime(df['date'] + 19000000, format='%Y%m%d') #make date proper

df = df.merge(df2[['mmid', 'store', 'city', 'zip', 'lat', 'long']], on=['store']).dropna() #add geographical info from store data

df.to_csv('retailData.csv')#Name of output .csv file. Conversion not really required, unless you want to open with Excel/Libre
#print df
