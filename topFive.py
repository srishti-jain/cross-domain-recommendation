import pandas as pd
import numpy as np

n = 5
df = pd.read_csv('retailData.csv')
df1 = df[['date', 'zip']] #initialise dataframe with top5 data

df.drop(df.columns[0], axis=1, inplace=True) #drop index column
df.set_index(['date', 'zip']) #sort by date and zip
#df = df.iloc[:10] #trial
df.drop(['mmid', 'store', 'city', 'zip', 'lat', 'long', 'date', 'week', 'custcoun'], axis=1, inplace=True) #drop unnecessary/text columns
#df = df.replace(0.0, np.nan) #if we want to ignore zero values

def topN(row):
       val = row.sort_values(ascending=False)[:n] #sort and choose first n values
       val = val.index.values #choose only index values
       return str(val) 

df1['MaxByQty'] = df.apply(topN, axis=1) #retrieving top n values for every row
df1['MaxByNormalizedQty'] = df.div(df.sum(axis=1), axis=0).apply(topN, axis=1) #divide each value by sum
df1['ByMaxIncrease'] = df.diff().reset_index(drop=True).apply(topN, axis=1) #find increase from last day's data
df1['ByMaxPercentIncrease'] = df.pct_change().apply(topN, axis=1) #find % increase from last day's data
