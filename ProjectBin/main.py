#!/usr/bin/env python3
# coding: utf-8

import math, random, os, json
import numpy as np
from collections import defaultdict
from collections import OrderedDict

edgeWeights = defaultdict(int) # Can be used for finding dense subgraphs perhaps? sort it and remove lowest numbers?
nodeDegrees = defaultdict(int)
graph = {}

def main():
  edgeWeights, nodeDegrees = buildGraph()
  print(edgeWeights)
  print("###fdas###")
  print(nodeDegrees)
  # edgeWeights, nodeDegrees = findDensestsSubgraph(edgeWeights, nodeDegrees)

# def findDensestsSubgraph(edgeWeights, nodeDegrees, epsilon=0.1):
#   print(edgeWeights)
#   print(nodeDegrees)
#   # newEdgeWeights = sorted(edgeWeights.iteritems(), key=lambda (k,v): (v,k))
#   newEdgeWeights = edgeWeights
#   newNodeDegrees = OrderedDict(sorted(nodeDegrees.iteritems(), key=lambda (k,v): (v,k)))
#   print(newEdgeWeights)
#   print(newNodeDegrees)
#   print(newNodeDegrees.popitem(False)) # Pop first item

#   # TODO: define pG as edged/nodes (does an edge with weight 2 count as 2 edges?)
#   H = G
#   while edgeWeights:
#     for node in nodeDegrees:
#       if nodeDegrees[node] <= 2*(1+epsilon)*pG:
#         # TODO: remove node
#         # TODO: remove all edges
#       if pG > pH:
#         H = G
#   return H; # return edgeWeights, nodeDegrees

def buildGraph():
  filteredDataPath = '../FilteredData/ParisSearchJanFiltered'
  filename = 'Paris-2015-1-1'
  # TODO: loop through multiple files
  f = open(os.path.dirname(__file__) + os.path.join(filteredDataPath, filename), 'r')
  
  for line in f:
    # tweet_id = tweet['id']
    # text = tweet['text']
    tweet = json.loads(line)
    hashtags = tweet['hashtags']

    # Create a list of neighbours (hashtags occuring in the same tweet)
    neighbours = []

    # Only care for tweets with more than 1 hashtag
    if len(hashtags) > 1: # This should be implicit after filtering is done
      for hashtag in hashtags:
        print(hashtag)
        neighbours.append(hashtag)

    # Sort the list of hashtags to avoid duplicate keys, e.g. "a-b" and "b-a"
    neighbours.sort()

    for i in range(0, len(neighbours)):
      # Only need to look through the rest of the list
      for j in range(i+1, len(neighbours)):
        key = "{}-{}".format(neighbours[i].encode('utf-8'), neighbours[j].encode('utf-8'))
        
        # Increase the weight of the edge if it exists, otherwise set it to 1
        if key in edgeWeights:
          edgeWeights[key] += 1
        else:
          edgeWeights[key] = 1

        # Also, keep track of degree
        nodeDegrees[neighbours[i]] += 1 # TODO: make sure this gives a degree that is the sum of the weights of the node's neighbours
        nodeDegrees[neighbours[j]] += 1
  
  f.close()

  return edgeWeights, nodeDegrees

if __name__ == '__main__':
  main()
