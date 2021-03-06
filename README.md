# Cross Domain Recommmendation System using Weather Data and Commercial Sales Data

*Database: https://research.chicagobooth.edu/kilts/marketing-databases/dominicks*

*Sales data(ccount.dta): http://kilts.chicagobooth.edu/dff/store-demos-customer-count/ccount_stata.zip*

*Store data(demo.dta): http://kilts.chicagobooth.edu/dff/store-demos-customer-count/demo_stata.zip*

How to run:
1. Download ccount.dta, demo.dta. Run dtaToCsv, and retailData.csv is generated
2. Run almanac.py to get output_almanac.csv.
3. All output_almanac.csv were compiled, and we had CompiledWeather.csv
4. Modify first row of Compiled weather to key,c1,c2....c11
5. Run topFive.py, and get top5trending.csv
6. Run trendprocessing.py. This adds a column 'key' to top5trending.csv, which is 'zip/date' 
7. Create a folder named 'saveHMM'. Run method1.py. It performs:
	(a) ReadDataAndMakeHMM : dumps HMMs to 'saveHMM' folder. Create a file named 'hmmRecords.csv' ( "hmmno","key", "MaxByNormalizedQty")
	(b) loadHMMs : loads HMMS from folder and data from 'hmmRecords.csv'
	(c) main stuff : save predictions to 'predictedData.csv'
8. Run compareTables.py, this gives mean value. 
