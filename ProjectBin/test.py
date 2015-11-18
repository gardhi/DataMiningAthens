#!/usr/bin/python

# Open a file
fo = open("/cal/exterieurs/ext6641/test.txt","r")
print "Name of the file: ", fo.name
print "Closed or not : ", fo.closed
print "Opening mode : ", fo.mode
print "Softspace flag : ", fo.softspace

print 
fo.read()



