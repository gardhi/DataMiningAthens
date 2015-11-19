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
  edgeWeights, nodeDegrees = buildGraph()
  # print(edgeWeights)
  # print("###fdas###")
  # print(nodeDegrees)
  edgeWeights, nodeDegrees = findDensestsSubgraphParallell(edgeWeights, nodeDegrees)
  print(edgeWeights)
  print(nodeDegrees)

def computeAverageDensity(edgeWeights, nodeDegrees):
  e = 0
  v = len(nodeDegrees)
  for edge in edgeWeights:
    e += edgeWeights[edge]
  return e/v

# TODO: make sure it is OK.
def findDensestsSubgraphParallell(edgeWeights, nodeDegrees, epsilon=0.5):
  print("---------------------------findDensestsSubgraphParallell---------------------------")
  # print('avgGraphDensity: {}'.format(avgGraphDensity))
  # print('2*(1+epsilon)*avgGraphDensity = {}'.format(2*(1+epsilon)*avgGraphDensity))

  # Create a sorted dictionary with ascending node degrees
  nodeDegrees = OrderedDict(sorted(nodeDegrees.iteritems(), key=lambda (k,v): (v,k)))
  # Create a copy of the edge dictionary so we can delete items from it while iterating through it
  # newEdgeWeights = edgeWeights.copy()


  count = 0
  while True:
    print('iteration #{}'.format(count))
    oldNNodes = len(nodeDegrees)
    oldNEdges = len(edgeWeights)

    avgGraphDensity = computeAverageDensity(edgeWeights, nodeDegrees)

    for node in nodeDegrees.keys():
      degree = nodeDegrees[node]
      # print(2*(1+epsilon)*avgGraphDensity)
      # print(degree)
      if degree <= 2*(1+epsilon)*avgGraphDensity:
        # print('node "{}" deleted'.format(node))
        del nodeDegrees[node]
        # Delete all edges connected to this node
        for edge in edgeWeights.keys():
          node1, node2 = edge.split('-')
          # print('{}-{}'.format(node1, node2))
          if (node == node1):
            # print('edge "{}" deleted'.format(edge))
            del edgeWeights[edge]
            # If statement to handle special case where edge is a self-edge, e.g. "follow-follow". Should it be filtered?
            if node1 != node2:
              nodeDegrees[node2] -= 1
          elif (node == node2):
            # print('edge "{}" deleted'.format(edge))
            del edgeWeights[edge]
            # If statement to handle special case where edge is a self-edge, e.g. "follow-follow". Should it be filtered?
            if node1 != node2:
              nodeDegrees[node1] -= 1
      else:
        # All remaining nodes have higher degree, no need to continue
        print('breaking for loop when node degree is: {}'.format(degree))
        break
    
    # print(len(edgeWeights))
    if len(edgeWeights) == 0: # TODO: is this correct, or should it be 0?
      break

    newAvgGraphDensity = computeAverageDensity(edgeWeights, nodeDegrees)
    print('nodeDegrees went from {} to {}'.format(oldNNodes, len(nodeDegrees)))
    print('edgeWeights went from {} to {}'.format(oldNEdges, len(edgeWeights)))
    print('avgGraphDensity went from {} to {}'.format(avgGraphDensity, newAvgGraphDensity))
    
    if newAvgGraphDensity > avgGraphDensity:
      newEdgeWeights = edgeWeights.copy()
      newNodeDegrees = nodeDegrees.copy()
    
    count += 1
  print("while finished")
  return newEdgeWeights, newNodeDegrees

def findDensestsSubgraph(edgeWeights, nodeDegrees, epsilon=0.1):
  print("---------------------------findDensestsSubgraph---------------------------")

  # Create a sorted dictionary with ascending node degrees
  nodeDegrees = OrderedDict(sorted(nodeDegrees.iteritems(), key=lambda (k,v): (v,k)))
  # Create a copy of the edge dictionary so we can delete items from it while iterating through it
  # newEdgeWeights = edgeWeights.copy()

  count = 0
  while True:
    # print('iteration #{}'.format(count))
    oldNNodes = len(nodeDegrees)
    oldNEdges = len(edgeWeights)

    avgGraphDensity = computeAverageDensity(edgeWeights, nodeDegrees)
    
    node, degree = nodeDegrees.popitem(last=False)
    # del nodeDegrees[node]
    # Delete all edges connected to this node
    for edge in edgeWeights.keys():
      node1, node2 = edge.split('-')
      # print('{}-{}'.format(node1, node2))
      if (node == node1):
        # print('edge "{}" deleted'.format(edge))
        del edgeWeights[edge]
        # If statement to handle special case where edge is a self-edge, e.g. "follow-follow". Should it be filtered?
        if node1 != node2:
          nodeDegrees[node2] -= 1
      elif (node == node2):
        # print('edge "{}" deleted'.format(edge))
        del edgeWeights[edge]
        # If statement to handle special case where edge is a self-edge, e.g. "follow-follow". Should it be filtered?
        if node1 != node2:
          nodeDegrees[node1] -= 1

    # Break while loop if we deleted last edge
    if len(edgeWeights) == 0:
      break

    newAvgGraphDensity = computeAverageDensity(edgeWeights, nodeDegrees)
    count += 1
    # print('nodeDegrees went from {} to {}'.format(oldNNodes, len(nodeDegrees)))
    # print('edgeWeights went from {} to {}'.format(oldNEdges, len(edgeWeights)))
    # print('avgGraphDensity went from {} to {}'.format(avgGraphDensity, newAvgGraphDensity))
    
    if newAvgGraphDensity > avgGraphDensity:
      newEdgeWeights = edgeWeights.copy()
      newNodeDegrees = nodeDegrees.copy()
    
  # print("while finished")
  return newEdgeWeights, newNodeDegrees


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
