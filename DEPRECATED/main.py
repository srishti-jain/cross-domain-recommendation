"""
Gaussian HMM of weather data
--------------------------
link : http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key=42299afedf80448c8b2150645171703&q=London&format=json&date=2016-01-01&enddate=2016-02-01

The JSON data from above link is converted to a cvs file. Data is loaded from that csv file.
Rightnow, one HMM for 1 day. It contains 7 observations per day, for 32 days ( K+LOndon Jan-Feb 2016 )

"""

from __future__ import print_function
import datetime
import numpy as np
import csv
from hmmlearn.hmm import GaussianHMM

import warnings
warnings.simplefilter("ignore", DeprecationWarning)

##print(__doc__)
###############################################################################

HMMno = 1
HMMs = []
filePath = 'london_jan_2016.csv'

def ReadDataAndMakeHMM():
    # Get data from csv
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

        # Pack diff and volume for training.
        X = np.column_stack([maxTemp, minTemp, uvIndex,windspeedMiles, weatherCode])
        ###############################################################################
        # Make an HMM instance and execute fit
        model = GaussianHMM(n_components=8, covariance_type="diag", n_iter=1000).fit(X)
        HMMs.append(model)

    ######## Print generated HMMs
    HMMno = 1
    for hmm in HMMs:
    	#print('HMM ' + str(HMMno))
    	#print(hmm.transmat_) 
    	HMMno = HMMno + 1


def FindMostProbableHMM(input):
    maxPredictionScore = HMMs[0].score(input)
    hmmNo = 0
    for i in range(len(HMMs)):
        predictionScore = HMMs[i].score(input)
        print(str(predictionScore), end=',')
        if predictionScore > maxPredictionScore:
            maxPredictionScore = predictionScore
            hmmNo = i
    print("Maximum score is" + str(maxPredictionScore))
    print("HMM number " + str(hmmNo))


####################### MAIN STUFF #######################

ReadDataAndMakeHMM()


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
