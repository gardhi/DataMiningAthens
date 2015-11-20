#!/usr/bin/env python3
# coding: utf-8

from __future__ import division
import math, random, os, json
import numpy as np
from collections import defaultdict
from collections import OrderedDict

edgeWeights = defaultdict(int)
nodeDegrees = defaultdict(int)

def main():
    dataSet = "ParisSearchFebFiltered/"
    fileName = "Paris-2015-2-"
    fileRange = (1,28)

    epsilon = 0.067
    numGraphs = 3

    # Build the graph
    edgeWeights, nodeDegrees = buildGraph(dataSet,fileName,fileRange)

    # Find densest subgraph, non-parallell implementation
    # denseEdgeWeights, denseNodeDegrees = findDensestsSubgraph(edgeWeights, nodeDegrees)
    # print(denseEdgeWeights)
    # print(denseNodeDegrees)

    # Find dense subgraphs
    denseEdgeWeightList, denseNodeDegreeList = findSeveralDenseSubgrafs(edgeWeights, nodeDegrees, epsilon, numGraphs)

    for i in range(0,len(denseEdgeWeightList)):
        print('subgraph #{}'.format(i+1))
        print(denseEdgeWeightList[i])
        print(denseNodeDegreeList[i])

def computeAverageDensity(edgeWeights, nodeDegrees):
    e = 0
    v = len(nodeDegrees)
    for edge in edgeWeights:
        e += edgeWeights[edge]
    return e/v

def findSeveralDenseSubgrafs(edgeWeights, nodeDegrees, epsilon, numGraphs):
    denseEdgeWeightList = []
    denseNodeDegreeList = []

    for i in range(numGraphs):
        print("Finding dense subgraph #{}".format(i+1))
        denseEdgeWeights, denseNodeDegrees = findDensestsSubgraphParallell(edgeWeights.copy(), nodeDegrees.copy(), epsilon)

        subgraphIntegrities = {}
        for node in denseNodeDegrees:
            degreeInSubgraph = 0
            for edge in denseEdgeWeights.keys():
                node1, node2 = edge.split('-')
                if (node == node1 or node == node2):
                    degreeInSubgraph += denseEdgeWeights[edge]
            subgraphIntegrity = degreeInSubgraph/denseNodeDegrees[node]
            subgraphIntegrities[node] = subgraphIntegrity
        avgSubgraphIntegrity = sum(subgraphIntegrities.values())/len(subgraphIntegrities)
        
        for node in denseNodeDegrees:
            # We want to keep nodes that doesn't have a high integrity.
            isDenseInSubgraph = subgraphIntegrities[node] > avgSubgraphIntegrity
            if isDenseInSubgraph:
                del nodeDegrees[node]

                # Delete all edges connected to this node
                for edge in edgeWeights.keys():
                    node1, node2 = edge.split('-')
                    """If edge is a self edge, delete it and don't reduce the degree
                    of "the other" node, since it is yourself"""
                    if node1 == node2:
                        del edgeWeights[edge]
                    else:
                        if node == node1:
                            nodeDegrees[node2] -= edgeWeights[edge]
                            del edgeWeights[edge]
                        elif node == node2:
                            nodeDegrees[node1] -= edgeWeights[edge]
                            del edgeWeights[edge]

        denseEdgeWeightList.append(denseEdgeWeights)
        denseNodeDegreeList.append(denseNodeDegrees)
    return denseEdgeWeightList, denseNodeDegreeList

"""
Parallell implementation of densest subgraph algorithm
"""
def findDensestsSubgraphParallell(edgeWeights, nodeDegrees, epsilon):
    # Create a sorted dictionary with ascending node degrees. NB! Does not sort itself later!
    nodeDegrees = OrderedDict(sorted(nodeDegrees.iteritems(), key=lambda (k,v): (v,k)))

    avgGraphDensity = computeAverageDensity(edgeWeights, nodeDegrees)
    avgGraphDensityBest = avgGraphDensity

    count = 0
    while count < 50:
        print('Iteration #{}'.format(count))
        nodeDegreesUnchanged = nodeDegrees.copy()

        for node in nodeDegrees.keys():
            degree = nodeDegreesUnchanged[node]

            if degree <= 2*(1+epsilon)*avgGraphDensity:
                del nodeDegrees[node]
                
                # Delete all edges connected to this node
                for edge in edgeWeights.keys():
                    node1, node2 = edge.split('-')
                    """If edge is a self edge, delete it and don't reduce the degree
                    of "the other" node, since it is yourself"""
                    if node1 == node2:
                        del edgeWeights[edge]
                    else:
                        if node == node1:
                            nodeDegrees[node2] -= edgeWeights[edge]
                            del edgeWeights[edge]
                        elif node == node2:
                            nodeDegrees[node1] -= edgeWeights[edge]
                            del edgeWeights[edge]

        # If no more edges left, we are finished
        if len(edgeWeights) == 0:
            break

        avgGraphDensity = computeAverageDensity(edgeWeights, nodeDegrees)
        
        if avgGraphDensity > avgGraphDensityBest:
            newEdgeWeights = edgeWeights.copy()
            newNodeDegrees = nodeDegrees.copy()
            avgGraphDensityBest = avgGraphDensity
        
        count += 1

    return newEdgeWeights, newNodeDegrees

"""
Non-parallell implementation of densest subgraph
"""
def findDensestsSubgraph(edgeWeights, nodeDegrees, epsilon=0.1):
    # Create a sorted dictionary with ascending node degrees
    nodeDegrees = OrderedDict(sorted(nodeDegrees.iteritems(), key=lambda (k,v): (v,k)))
    avgGraphDensity = computeAverageDensity(edgeWeights, nodeDegrees)
    avgGraphDensityBest = avgGraphDensity

    count = 0
    while True:
        node, degree = nodeDegrees.popitem(last=False)
        
        # Delete all edges connected to this node
        for edge in edgeWeights.keys():
            node1, node2 = edge.split('-')
            if (node == node1):
                del edgeWeights[edge]
                
                # If statement to handle special case where edge is a self-edge, e.g. "follow-follow". Should it be filtered?
                if node1 != node2:
                    nodeDegrees[node2] -= 1
            elif (node == node2):
                del edgeWeights[edge]
                
                # If statement to handle special case where edge is a self-edge, e.g. "follow-follow". Should it be filtered?
                if node1 != node2:
                    nodeDegrees[node1] -= 1

        # Break while loop if we deleted last edge
        if len(edgeWeights) == 0:
            break

        avgGraphDensity = computeAverageDensity(edgeWeights, nodeDegrees)
        count += 1

        if avgGraphDensityBest < avgGraphDensity:
            avgGraphDensityBest = avgGraphDensity
            newEdgeWeights = edgeWeights.copy()
            newNodeDegrees = nodeDegrees.copy()

    return newEdgeWeights, newNodeDegrees

def buildGraph(dataSet, fileName, fileRange):
    filteredDataPath = "../FilteredData/" + dataSet

    for file_n in fileRange:
        fileName_n = fileName + str(file_n)
        f = open(os.path.dirname(__file__) + os.path.join(filteredDataPath, fileName_n), 'r')
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
                  nodeDegrees[neighbours[i].encode('utf-8')] += 1
                  nodeDegrees[neighbours[j].encode('utf-8')] += 1
        f.close()

    return edgeWeights, nodeDegrees

if __name__ == '__main__':
    main()