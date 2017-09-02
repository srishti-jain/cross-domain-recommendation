from bs4 import BeautifulSoup
from random import randint
import pandas as pd
import numpy as np
import urllib2, time
from fake_useragent import UserAgent

#initialisations
filename = 'ratings_Sports_and_Outdoors.csv' #NAME OF CSV WHICH HAS USERIDS
Jan1 = 1388534400 #January 1, 2014
oneDay = 86400
ua = UserAgent()
csv_input = pd.read_csv(filename, header=None)
csv_input = csv_input[(csv_input[3] > Jan1) & (csv_input[3] < (Jan1 + oneDay*31))] #take entries for jan 2014 only. UNIX timestamp
reviewerIDs = csv_input[0].unique()
csv_input[4] = csv_input[0]
start = time.time()

def getLocation(userid):
       #GETS THE LOCATION OF A USER BASED ON USERID. NONE IS LOCATION NOT SPECIFIED
       site = "https://www.amazon.com/gp/cdp/member-reviews/" + userid
       hdr = {'User-Agent': ua.random}
       try:
              html = BeautifulSoup(urllib2.urlopen(urllib2.Request(site, headers=hdr)), "lxml").body
              location = html.find('div', attrs={'class':'a-fixed-right-grid location-and-occupation-holder'})
       except:
              print "Error encountered :/"
              print "Retrying after 30 seconds"
              time.sleep(30)
              return getLocation(userid)
       if location is None:
              return "None"
       return location.text.strip('\n')

#print len(csv_input) will print the number of rows in this file
#print len(csv_input[0].unique()) will print the number of unique reviewers (since first column has reviewerIDs)
for counter, x in enumerate(reviewerIDs):
       print "Getting ID for reviewer" + str(counter) + "/122793"
       location = getLocation(x)
       location = location.encode('ascii', 'ignore') #take care of any ascii encoding errors
       print location
       csv_input[4] = csv_input[4].replace(x, location)
       if counter % 10 == 0 : # replcae with counter > N if you want to analyse N IDs only
              csv_input.to_csv('output_sports.csv', index=False, header=None)
              time.sleep(randint(1, 10))
              print "Time elapsed: " + str(timedelta(seconds=(time.time() - start))) #print total time elapsed after every 10 queries
       time.sleep(randint(1, 3))
csv_input = csv_input[csv_input[4] != "None"] #ELIMINATE USERS WITH NO LOCATION
