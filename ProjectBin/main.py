#!/usr/bin/env python3
# coding: utf-8

from __future__ import division
import math, random, os, json
import numpy as np
from collections import defaultdict
from collections import OrderedDict

edgeWeights = defaultdict(int) # Can be used for finding dense subgraphs perhaps? sort it and remove lowest numbers?
nodeDegrees = defaultdict(int)
graph = {}

def main():
  print("################################################################################################")
  print("################################################################################################")
  print("################################################################################################")
    

  dataSet = "ParisSearchFebFiltered/" 
  fileName = "Paris-2015-2-"
  fileRange = (1,28)
  
  epsilon = 0.067
  numGraphs = 2  
  
  edgeWeights, nodeDegrees = buildGraph(dataSet,fileName,fileRange)

#  edgeWeights, nodeDegrees = findSeveralDenseSubgrafs(edgeWeights, nodeDegrees, epsilon, numGraphs)  
#  for i in range(0,len(edgeWeights)):
#      print(edgeWeights[i])
#      print(nodeDegrees[i])  
  
  denseEdgeWeights, denseNodeDegrees = findDensestsSubgraphParallell(edgeWeights, nodeDegrees, epsilon)
  print " nodeWeights = "
  print denseEdgeWeights
  print "nodeDegrees = "
  print denseNodeDegrees

#
  
def findSeveralDenseSubgrafs(edgeWeights, nodeDegrees, epsilon, numGraphs):
    
    denseEdgeWeightList =  []
    denseNodeDegreeList = []
    for i in range(numGraphs+1):
        denseEdgeWeights, denseNodeDegrees = findDensestsSubgraphParallell(edgeWeights, nodeDegrees, epsilon)
        print " nodeWeights = "
        print denseEdgeWeights
        print "nodeDegrees = "
        print denseNodeDegrees
        
#        if denseEdgeWeights and denseNodeDegrees:        
        for node in denseNodeDegrees:
            # print('node "{}" deleted'.format(node))
            del nodeDegrees[node]
            # Delete all edges connected to this node
            for edge in edgeWeights.keys():
                node1, node2 = edge.split('-')
                if node1 != node2:
                    if node == node1:
                        nodeDegrees[node2] -= edgeWeights[edge]
                        del edgeWeights[edge] 
                        #print('{}-{}'.format(node1, node2))
                    elif node == node2:
                        nodeDegrees[node1] -= edgeWeights[edge]
                        del edgeWeights[edge] 
                        #print('{}-{}'.format(node1, node2))
                else:
                    del edgeWeights[edge]
                    
        denseEdgeWeightList.append(denseEdgeWeights)
        denseNodeDegreeList.append(denseNodeDegrees)
    return denseEdgeWeightList, denseNodeDegreeList            


def computeAverageDensity(edgeWeights, nodeDegrees):
  e = 0
  v = len(nodeDegrees)
  for edge in edgeWeights:
    e += edgeWeights[edge]
  return e/v

# TODO: make sure it is OK.
def findDensestsSubgraphParallell(edgeWeights, nodeDegrees, epsilon):
  print("---------------------------findDensestsSubgraphParallell---------------------------")
  # print('avgGraphDensity: {}'.format(avgGraphDensity))
  # print('2*(1+epsilon)*avgGraphDensity = {}'.format(2*(1+epsilon)*avgGraphDensity))
  newEdgeWeights = 0
  newNodeDegrees = 0

  # Create a sorted dictionary with ascending node degrees !! does not sort itself later
  nodeDegrees = OrderedDict(sorted(nodeDegrees.iteritems(), key=lambda (k,v): (v,k)))
  avgGraphDensity = computeAverageDensity(edgeWeights, nodeDegrees)
  avgGraphDensityBest = avgGraphDensity

  count = 0
  while count <50:
    print('iteration #{}'.format(count))
    nodeDegreesUnchanged = nodeDegrees.copy()

    for node in nodeDegrees.keys():

      degree = nodeDegreesUnchanged[node]
#      print(2*(1+epsilon)*avgGraphDensity)
#      print(degree)
#      
      if degree <= 2*(1+epsilon)*avgGraphDensity:
        # print('node "{}" deleted'.format(node))
        del nodeDegrees[node]
        # Delete all edges connected to this node
        for edge in edgeWeights.keys():
            node1, node2 = edge.split('-')
            if node1 != node2:
                if node == node1:
                    nodeDegrees[node2] -= edgeWeights[edge]
                    del edgeWeights[edge] 
                    #print('{}-{}'.format(node1, node2))
                elif node == node2:
                    nodeDegrees[node1] -= edgeWeights[edge]
                    del edgeWeights[edge] 
                    #print('{}-{}'.format(node1, node2))
            else:
                del edgeWeights[edge]
            
    
    if len(edgeWeights) == 0:
      break

    avgGraphDensity = computeAverageDensity(edgeWeights, nodeDegrees)
#    print('nodeDegrees went from {} to {}'.format(oldNNodes, len(nodeDegrees)))
#    print('edgeWeights went from {} to {}'.format(oldNEdges, len(edgeWeights)))
#    print('avgGraphDensity went from {} to {}'.format(avgGraphDensity, newAvgGraphDensity))
    
    if avgGraphDensity > avgGraphDensityBest:
      newEdgeWeights = edgeWeights.copy()
      newNodeDegrees = nodeDegrees.copy()
      avgGraphDensityBest = avgGraphDensity
    
    count += 1
#    print " nodeWeights = "
#    print edgeWeights
#    print "nodeDegrees = "
#    print nodeDegrees

  print("while finished")
  print "count = " + str(count)
  return newEdgeWeights, newNodeDegrees



def buildGraph(dataSet, fileName, fileRange):

  filteredDataPath = "../FilteredData/" + dataSet

  for file_n in fileRange:
      fileName_n = fileName + str(file_n)
      f = open(os.path.dirname(__file__) + "/" + os.path.join(filteredDataPath, fileName_n), 'r')
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
            # print(hashtag)
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
            nodeDegrees[neighbours[i].encode('utf-8')] += 1 # TODO: make sure this gives a degree that is the sum of the weights of the node's neighbours
            nodeDegrees[neighbours[j].encode('utf-8')] += 1
      
      f.close()

  return edgeWeights, nodeDegrees

if __name__ == '__main__':
  main()



#def findDensestsSubgraph(edgeWeights, nodeDegrees, epsilon=0.1):
#  print("---------------------------findDensestsSubgraph---------------------------")
#
#  # Create a sorted dictionary with ascending node degrees
#  nodeDegrees = OrderedDict(sorted(nodeDegrees.iteritems(), key=lambda (k,v): (v,k)))
#  avgGraphDensity = computeAverageDensity(edgeWeights, nodeDegrees)  
#  # Create a copy of the edge dictionary so we can delete items from it while iterating through it
#  # newEdgeWeights = edgeWeights.copy()
#
#  count = 0
#  while True:
#    # print('iteration #{}'.format(count))
#    oldNNodes = len(nodeDegrees)
#    oldNEdges = len(edgeWeights)
#
#    
#    
#    node, degree = nodeDegrees.popitem(last=False)
#    # del nodeDegrees[node]
#    # Delete all edges connected to this node
#    for edge in edgeWeights.keys():
#      node1, node2 = edge.split('-')
#      # print('{}-{}'.format(node1, node2))
#      if (node == node1):
#        # print('edge "{}" deleted'.format(edge))
#        del edgeWeights[edge]
#        # If statement to handle special case where edge is a self-edge, e.g. "follow-follow". Should it be filtered?
#        if node1 != node2:
#          nodeDegrees[node2] -= 1
#      elif (node == node2):
#        # print('edge "{}" deleted'.format(edge))
#        del edgeWeights[edge]
#        # If statement to handle special case where edge is a self-edge, e.g. "follow-follow". Should it be filtered?
#        if node1 != node2:
#          nodeDegrees[node1] -= 1
#    
#    # Break while loop if we deleted last edge
#    if len(edgeWeights) == 0:
#      break
#
#    avgGraphDensity = computeAverageDensity(edgeWeights, nodeDegrees)
#    count += 1
#    # print('nodeDegrees went from {} to {}'.format(oldNNodes, len(nodeDegrees)))
#    # print('edgeWeights went from {} to {}'.format(oldNEdges, len(edgeWeights)))
#    # print('avgGraphDensity went from {} to {}'.format(avgGraphDensity, newAvgGraphDensity))
#    
#    if avgGraphDensityBest < avgGraphDensity:
#      avgGraphDensityBest = avgGraphDensity
#      newEdgeWeights = edgeWeights.copy()
#      newNodeDegrees = nodeDegrees.copy()
#    
#  # print("while finished")
#  return newEdgeWeights, newNodeDegrees
