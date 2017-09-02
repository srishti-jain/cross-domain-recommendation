from __future__ import print_function
from sklearn.externals import joblib
import datetime
from datetime import timedelta
import numpy as np
from itertools import *
import csv
import html5lib, time, os.path
from hmmlearn.hmm import GaussianHMM
import pandas as pd
import os

import warnings
warnings.simplefilter("ignore", DeprecationWarning)


#df1 contains actual output, df2 expected output. Columns in both-Zip/Date, MaxByNormalizedQty
#Add this column to both

trendingFilePath = 'top5trending.csv'
predictedData = 'predictedData.csv'

df1 = pd.DataFrame.from_csv(trendingFilePath, index_col=None)
df2 = pd.DataFrame.from_csv(predictedData, index_col=None)

print(df1.count())


df1['key'] = df1['zip'].apply(int).apply(str) + "/" + df1['date'].apply(str) #make Zip/Date column to match RetailData file

print(df1.count())

df3 = df1.merge(df2, on='key')
def match(x):
       list1 = str(x['MaxByNormalizedQty_x']).split(' ')
       list2 = str(x['MaxByNormalizedQty_y']).split(' ')
       return len(set(list1) & set(list2))

df3['match'] = df3.apply(match, axis=1)
print(df3[['match']].mean()) 
df3.to_csv("sample.csv", header=True, index=False)
#'match' column contains everything now. aggregate functions can be applie on it now
