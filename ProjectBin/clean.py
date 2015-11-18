# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 14:32:14 2015

@author: ext6641
"""

import json
import time

start_time = time.time()
unique_tagset = set()


#filtering data
for date in range(1,32):
    filename = "Paris-2015-1-" + str(date)
    json_data = open("/cal/exterieurs/ext6641/ParisSearchJan/" + filename)
    
    ut = open("/cal/exterieurs/ext6641/DataMiningAthens/ParisSearchJanFiltered/" + filename, "wb")
    
    for line in json_data:        
        data = json.loads(line)
        
        if(data["entities"]["hashtags"]):
            utdata = {"id" : data["id"], "hashtags": [], "text" : data["text"], "user_id" : data["user"]["id"]}
            for tags in data["entities"]["hashtags"]:                
                utdata['hashtags'].append(tags["text"].lower())
            
            if frozenset(utdata["hashtags"]) not in unique_tagset:

                unique_tagset.add(frozenset(utdata["hashtags"]))
                ut.write(json.dumps((utdata), indent=4, separators=(',',': '), sort_keys=True).replace("\n",''))
                ut.write('\n')
            
    ut.close()
    json_data.close()

print "Finished Filtering"
print("it took: %s seconds" % (time.time() - start_time))
