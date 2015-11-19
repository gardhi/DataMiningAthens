# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 14:32:14 2015

@author: ext6641
"""

import json
import time

start_time = time.time()
unique_tagset = set()

num_tweets = 0

#Date spesifications:
#    ParisJanuary has 31 files from 1 to 31
#    ParisFebruary has 28 files from 1 to 28
#    Oscars has 4 files from 23 to 26
#    NewYork has 4 files from 23 to 26
#

#filtering data

#for date in range(1,32):
#    filename = "Paris-2015-1-" + str(date)
#    ut = open("/cal/exterieurs/ext6641/DataMiningAthens/FilteredData/ParisSearchJanFiltered/" + filename, "wb") # test/" +filename,"wb") ##    
#    json_data = open("/cal/exterieurs/ext6641/ParisSearchJan/" + filename)
#
#for date in range(1,29):    
#    filename = "Paris-2015-2-" + str(date)
#    json_data = open("/cal/exterieurs/ext6641/ParisSearchFeb/" + filename)
#    ut = open("/cal/exterieurs/ext6641/DataMiningAthens/FilteredData/ParisSearchFebFiltered/" + filename, "wb") # test/" +filename,"wb") ##  

#for date in range(23,27):
#    filename = "Oscars-2015-2-" + str(date)
#    json_data = open("/cal/exterieurs/ext6641/Oscars/" + filename)
#    ut = open("/cal/exterieurs/ext6641/DataMiningAthens/FilteredData/OscarsFiltered/" + filename, "wb") # test/" +filename,"wb") ##  

for date in range(23,27):
    filename = "NewYork-2015-2-" + str(date)
    json_data = open("/cal/exterieurs/ext6641/NewYorkOneWeek/" + filename)
    ut = open("/cal/exterieurs/ext6641/DataMiningAthens/FilteredData/NewYorkOneWeekFiltered/" + filename, "wb") # test/" +filename,"wb") ##  



    
    
    for line in json_data: 
        num_tweets += 1        
        
        data = json.loads(line)
        
        if(data["entities"]["hashtags"]):
            utdata = {"id" : data["id"], "hashtags": [], "text" : data["text"], "user_id" : data["user"]["id"]}
            for tags in data["entities"]["hashtags"]:                
                utdata['hashtags'].append(tags["text"].lower())
            
            if (len(utdata["hashtags"]) > 1):
                
                if frozenset(utdata["hashtags"]) not in unique_tagset:
                    unique_tagset.add(frozenset(utdata["hashtags"]))
                    ut.write(json.dumps((utdata), indent=4, separators=(',',': '), sort_keys=True).replace("\n",''))
                    ut.write('\n')

    ut.close()
    json_data.close()

print "Finished Filtering " + str(num_tweets) + " tweets."
print("it took: %s seconds" % (time.time() - start_time))
