"""Naive method
Number of rows : 247919 --- 247000
Training data : 1 - 222300 
Testing data : 222301 - 247000


Unique rows in MaxByNormalizedQty:823
Naming of HMMs in file: hmmno_part.pkl"""

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

def unique_rows(a):
    a = np.ascontiguousarray(a)
    unique_a = np.unique(a.view([('', a.dtype)]*a.shape[1]))
    return unique_a.view(a.dtype).reshape((unique_a.shape[0], a.shape[1]))

startTime = time.time()
weatherFilePath = 'CompiledWeather.csv'
trendingFilePath = 'top5trending.csv'
HMMfile = 'hmmRecords.csv'
predictedData = 'predictedData.csv'

dfWeather = pd.DataFrame.from_csv(weatherFilePath, index_col=None)
HMMs = []

def processValue(str):
	try:
		x = float(str.split(' ')[0])
		return x
	except ValueError:
		return 0
	except AttributeError:
		return 0

def ReadDataAndMakeHMM():
    # Get data from csv
    HMMno = 0
    df = pd.DataFrame.from_csv(trendingFilePath, index_col=None)

    removeValues=[]
    for i in range(222301,247000):
    	removeValues.append(i)
    df = df.drop(df.index[removeValues])
    df = df[df.duplicated(subset=['MaxByNormalizedQty']) | df.duplicated(subset=['MaxByNormalizedQty'], keep='last')] #remove unique entries
    df2 = df.groupby('MaxByNormalizedQty')['key'].apply(list).to_frame().reset_index() #create df with list of dates having same trending products
    columns = ["hmmno", "key", "MaxByNormalizedQty"]
    dfHmm = pd.DataFrame(index=None, columns=columns)


    print("Total number of rows:", df2.count())
    
    for oindex,row in islice(df2.iterrows(), 0, None):

        keys = row['key']
        trendingItem = row['MaxByNormalizedQty']
        


        m = len(keys)/100
        if len(keys)%100 != 0:
        	m = m+1

        start = 0
        for ind in range(0,m):
        	if (len(keys) < start+100):
        	    end = len(keys)
        	else:
        		end = start+100 
        	key = keys[start:end]
        	start = end+1
	        
	        if(len(key) <= 1):
	        	break

	        df3 = dfWeather.loc[dfWeather['key']==key[0]]
	        for k in range(1,len(key)):
	        	df3 = pd.concat([df3, dfWeather.loc[dfWeather['key']==key[k]]])
	        print('Row number : ', oindex, 'Keys:', len(key))
	    	c1 = []
	        c2 = []
	        c3 = []
	        c4 = []
	        c5 = []
	        c7 = []
	        c8 = []
	        c9 = []
	        c10 = []
	        c11 = []




        	for index,d in df3.iterrows():
		        c1.append(processValue(d['c1']))
		        c2.append(processValue(d['c2']))
		        c3.append(processValue(d['c3']))
		        c4.append(processValue(d['c4']))
		        c5.append(processValue(d['c5']))
		        c7.append(processValue(d['c7']))
		        c8.append(processValue(d['c8']))
		        c9.append(processValue(d['c9']))
		        c10.append(processValue(d['c10']))
		        c11.append(processValue(d['c11']))
		        

	        #print(len(c1), len(key), len(df3), key)
	        
	        # Pack diff and volume for training.
	        X = np.column_stack([c1,c2,c3,c4,c5,c7,c8,c9,c10,c11 ])
	        ###############################################################################
	        # Make an HMM instance and execute fit
	        if len(unique_rows(X)) <= 1:
	        	continue
	        X = unique_rows(X)
	        #print(X)

	        model = GaussianHMM(n_components=len(X), covariance_type="diag", n_iter=1000).fit(X)
	        joblib.dump(model, "saveHMM/hmm" + str(HMMno)+ ".pkl")


	        newItem = {"hmmno": HMMno, "hmm": model, "key":key, "MaxByNormalizedQty":trendingItem}
	        HMMs.append(newItem)
	        #print("SCORE")
	        x = [ 26.1  , 37.9,   44.1,   29.9,   36.1,  3.4 ,   0.4 ,  11.74 , 16.11,0  ]
	        # print(model.transmat_)
	        # print(model.startprob_)

	        
	        for i in  range(0, len(model.transmat_)):
	        	if model.transmat_[i].sum() == 0.0:
	        		model.transmat_[i][0]=1.0

	        # print(sm)
	        # print(model.score(x))

	        HMMno = HMMno + 1
        if HMMno%10 == 0:
        	print("Time elapsed: " + str(timedelta(seconds=(time.time() - startTime))))
        #print(newItem)

        #if(HMMno == 222300):


    hmmno,key,mx = [],[],[]

    for i in HMMs:
    	hmmno.append(i["hmmno"])
    	key.append(i["key"])
    	mx.append(i["MaxByNormalizedQty"])
    dfHmm["hmmno"] = hmmno
    dfHmm["key"] = key
    dfHmm["MaxByNormalizedQty"] = mx

    dfHmm.to_csv(HMMfile, encoding="utf-8", header=True, index=False)


    #for hmm in HMMs:
        #print('HMM ' + str(HMMno))
        #print(hmm.transmat_)

# def rename():
# 	path = "saveHMM/"
# 	files = os.listdir(path)
# 	for filename in files:
# 		x = filename.split('_')[0]
# 		os.rename(os.path.join(path, filename), os.path.join(path, x+".pkl"))


def loadHMMs():
	df = pd.DataFrame.from_csv(HMMfile, index_col=None)
	for index,row in islice(df.iterrows(), 0, None):
		model = joblib.load("saveHMM/hmm" + str(row["hmmno"]) + ".pkl")
		newItem = {"hmmno": row["hmmno"], "hmm": model, "key":row["key"], "MaxByNormalizedQty":row["MaxByNormalizedQty"]}
		HMMs.append(newItem)

####################### MAIN STUFF #######################

ReadDataAndMakeHMM()
columns = ['key', 'MaxByNormalizedQty', 'score', 'trendKey']
key=[]
MaxByNormalizedQty=[]
trendKey = []
score = []

df_ = pd.DataFrame(index=None, columns=columns)
for index, d in islice(dfWeather.iterrows(), 222301, None):
    
    c1 = []
    c2 = []
    c3 = []
    c4 = []
    c5 = []
    c7 = []
    c8 = []
    c9 = []
    c10 = []
    c11 = []
    c1.append(processValue(d['c1']))
    c2.append(processValue(d['c2']))
    c3.append(processValue(d['c3']))
    c4.append(processValue(d['c4']))
    c5.append(processValue(d['c5']))
    c7.append(processValue(d['c7']))
    c8.append(processValue(d['c8']))
    c9.append(processValue(d['c9']))
    c10.append(processValue(d['c10']))
    c11.append(processValue(d['c11']))
    
    
    # Pack diff and volume for training.
    X = np.column_stack([c1,c2,c3,c4,c5,c7,c8,c9,c10,c11 ])
    
    maxPredictionScore = HMMs[0]["hmm"].score(X)
    hmmNo = 0
    for i in range(1,len(HMMs)):
    	predictionScore = HMMs[i]["hmm"].score(X)
        print(str(predictionScore), end=',')
        if predictionScore > maxPredictionScore:
            maxPredictionScore = predictionScore
            hmmNo = i
    print("Maximum score is" + str(maxPredictionScore))
    print("HMM number " + str(hmmNo))
    key.append(d['key'])
    trendKey.append(HMMs[hmmNo]['key'])
    MaxByNormalizedQty.append(HMMs[hmmNo]['MaxByNormalizedQty'])
    score.append(maxPredictionScore)



df_['key'] = key
df_['MaxByNormalizedQty'] = MaxByNormalizedQty
df_['score'] = score
df_['trendKey'] = trendKey

df_.to_csv(predictedData, encoding="utf-8", header=True, index=False)










def FindMostProbableHMM(input):
    maxPredictionScore = HMMs[0].score(input)
    hmmNo = 0
    for i in range(len(HMMs)):
        predictionScore = i["hmm"].score(input)
        print(str(predictionScore), end=',')
        if predictionScore > maxPredictionScore:
            maxPredictionScore = predictionScore
            hmmNo = i
    print("Maximum score is" + str(maxPredictionScore))
    print("HMM number " + str(hmmNo))

def TestMostProbableSequence():
    for d in csv.DictReader(open(filePath), delimiter=','):
        maxTemp = []
        minTemp = []
        uvIndex = []
        windspeedMiles = []
        weatherCode = []
        weatherDesc = []
        precipitation = []
        humidity = []
        visibility = []
        pressure = []
        cloudCover = []
        HeatIndex = []
        DewPoint = []
        WindChill = []
        WindGust = []
        FeelsLike = []
        for i in range(8):
            maxTemp.append(int(d['maxtempC']))
            minTemp.append(int(d['mintempC']))
            uvIndex.append(int(d['uvIndex']))
            weatherCode.append(int(d['weatherCode']))
            pre = 'hourly/' + str(i) + '/'
            weatherDesc.append(str(d[pre+'weatherDesc/0/value']))
            windspeedMiles.append(int(d[pre+'windspeedMiles']))
            precipitation.append(float(d[pre+'precipMM']))
            humidity.append(int(d[pre+'humidity']))
            visibility.append(int(d[pre+'visibility']))
            pressure.append(int(d[pre+'pressure']))
            cloudCover.append(int(d[pre+'cloudcover']))
            HeatIndex.append(int(d[pre+'HeatIndexC']))
            DewPoint.append(int(d[pre+'DewPointC']))
            WindChill.append(int(d[pre+'WindChillC']))
            WindGust.append(int(d[pre+'WindGustMiles']))
            FeelsLike.append(int(d[pre+'FeelsLikeC']))
        X = np.column_stack([maxTemp, minTemp, uvIndex,windspeedMiles, weatherCode])
        FindMostProbableHMM(X)


print("ALL Done!!")
