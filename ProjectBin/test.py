#!/usr/bin/python

# Open a file

import json

filename = "Paris-2015-1-1"
ut = open("/cal/exterieurs/ext6641/test/" + filename, "r")

for line in ut:
    print line
    hallo = json.loads(line)

ut.close()