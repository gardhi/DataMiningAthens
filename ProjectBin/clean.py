# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 14:32:14 2015

@author: ext6641
"""

import json


for date in range(1,32):
    filename = "Paris-2015-1-" + str(date)
    json_data = open("/cal/exterieurs/ext6641/ParisSearchJan/" + filename)
    
    ut = open("/cal/exterieurs/ext6641/ProjectDump/" + filename, "wb")
    
    for line in json_data:
        data = json.loads(line)
        utdata = "{\"id\": "  + str(data["id"]) + ", \"hashtags\": ["
        if(data["entities"]["hashtags"]):
            for tags in data["entities"]["hashtags"]:
                utdata += tags["text"].lower() + ", "    
            utdata = utdata[:-2]
            utdata += "], \"text\":" + data["text"].replace("\n",' ') + "}\n"
            ut.write(utdata)
    ut.close()

print "finished"