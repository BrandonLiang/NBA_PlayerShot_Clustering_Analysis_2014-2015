# # -*- coding: utf-8 -*-
import csv
import os
from sets import Set
import math
#import numpy as np
import random
import math

iteration = 100 # number of iterations to apply K-means Algorithm for clustering

# Use sci-kit's K-Means Clustering

directory = "/Users/brandonliang/Desktop/*5. NBA Stats Data/2014-2015 Player Shots Data/Data"
newDirectory = "/Users/brandonliang/Desktop/*5. NBA Stats Data/2014-2015 Player Shots Data"

style = newDirectory + "/Shooting Style/Player Shooting Style Analysis.csv"
stylePG = newDirectory + "/Shooting Style/Player Shooting Style Analysis-PG.csv"
styleSG = newDirectory + "/Shooting Style/Player Shooting Style Analysis-SG.csv"
styleSF = newDirectory + "/Shooting Style/Player Shooting Style Analysis-SF.csv"
stylePF = newDirectory + "/Shooting Style/Player Shooting Style Analysis-PF.csv"
styleC = newDirectory + "/Shooting Style/Player Shooting Style Analysis-C.csv"
stylePerformance = newDirectory + "/Shooting Style + Shot Performance/Player Shooting Style + Shot Performance Analysis.csv"
stylePerformancePG = newDirectory + "/Shooting Style + Shot Performance/Player Shooting Style + Shot Performance Analysis-PG.csv"
stylePerformanceSG = newDirectory + "/Shooting Style + Shot Performance/Player Shooting Style + Shot Performance Analysis-SG.csv"
stylePerformanceSF = newDirectory + "/Shooting Style + Shot Performance/Player Shooting Style + Shot Performance Analysis-SF.csv"
stylePerformancePF = newDirectory + "/Shooting Style + Shot Performance/Player Shooting Style + Shot Performance Analysis-PF.csv"
stylePerformanceC = newDirectory + "/Shooting Style + Shot Performance/Player Shooting Style + Shot Performance Analysis-C.csv"

def cluster(filepath,k):
	ifile  = open(filepath, "rb")
	reader = csv.reader(ifile)
	reader.next()
	playerList = []
	teamList = []
	featureMatrix = []
	#featureToPlayer = {}
	playerToFeature = {}
	playerToTeam = {}
	for row in reader:
		playerList.append(row[0])
		teamList.append(row[1])
		featureMatrix.append(row[2:])
		#featureToPlayer[row[2:]] = row[0]
		playerToFeature[row[0]] = row[2:]
		playerToTeam[row[0]] = row[1]
	totalPlayer = len(featureMatrix)
	centroids = []
	cluster = {}
	
	# First choose 3 x's as starting centroids
	for i in range(k):
		m = random.randint(0,totalPlayer-1)
		f = featureMatrix[m]
		#f[0] = '0.01'
		#f[1] = '0.01'
		#f[2] = '0.01'
		#f[i] = '0.98'
		centroids.append(f)
		print f
	
	for times in range(iteration):
		for i in range(k):
			cluster[i] = []
		for eachPlayerFeature in featureMatrix: 
			thisDistanceComparison = []
			for i in range(k):
				center = centroids[i]
				distance1, distance2 = distanceMetrics(center, eachPlayerFeature)
				dist = distance1 
				#dist = distance(center,eachPlayerFeature)
				thisDistanceComparison.append(dist)
			index = thisDistanceComparison.index(min(thisDistanceComparison))
			tempCluster = cluster[index]
			tempCluster.append(eachPlayerFeature)
			cluster[index] = tempCluster
		newCentroids = []
		for each in cluster.keys():
			y = computeMean(cluster[each])
			newCentroids.append(y)

		distanceFactor = []
		for i in range(k):
			distance1, distance2 = distanceMetrics(centroids[i],newCentroids[i])
			distance = distance1 * distance2
			distanceFactor.append(distance)
		centroids = newCentroids

	resultingPlayerCluster = []
	for i in range(k):
		clusterFeatures = cluster[i]
		currentPlayerCluster = []
		for clusterFeature in clusterFeatures:
			player = playerList[featureMatrix.index(clusterFeature)]
			currentPlayerCluster.append(player)
		resultingPlayerCluster.append(currentPlayerCluster)

	for i in range(k):
		resultingPlayerCluster.append(cluster[i])

	styleOrNot = filepath.split("/")[6]
	filename = filepath.split("/")[7]
	outputFilename = newDirectory + "/" + styleOrNot + "/Cluster/" + filename + "--" + str(k) + " Cluster.csv"
	return resultingPlayerCluster,outputFilename

def distanceMetrics(x,y): # Chebychev for shot attempt tendency and Euclidean for the shot performance
	chebyChevDist = 1.0
	EuclideanDistance = 0
	if (len(x) == 0 or len(y) == 0):
		return 0,0
	if (len(x) > 0):
		for i in range(3):
			#if (math.fabs(float(x[i])-float(y[i])) <= chebyChevDist):
			chebyChevDist = chebyChevDist + math.fabs(float(x[i])-float(y[i]))
		for i in range(len(x)-3):
			EuclideanDistance = EuclideanDistance + math.fabs(float(x[i+3])-float(y[i+3]))
		return chebyChevDist, 1 #EuclideanDistance

def computeMean(x):
	y = []
	count = len(x)
	if (len(x)==0):
		return []
	for i in range(len(x[0])):
		sum = 0
		for j in range(len(x)):
			sum = sum + float(x[j][i])
		y.append(sum*1.0/count)
	return y

def putTogether(resultingPlayerCluster,outputFilename):

	result = csv.writer(open(outputFilename,"wb"))
	for entry in resultingPlayerCluster:
		result.writerow(entry)

def main():
	resultingPlayerCluster,outputFilename = cluster(style,3)
	putTogether(resultingPlayerCluster,outputFilename)
	resultingPlayerCluster,outputFilename = cluster(stylePG,3)
	putTogether(resultingPlayerCluster,outputFilename)
	resultingPlayerCluster,outputFilename = cluster(styleSG,3)
	putTogether(resultingPlayerCluster,outputFilename)
	resultingPlayerCluster,outputFilename = cluster(styleSF,3)
	putTogether(resultingPlayerCluster,outputFilename)
	resultingPlayerCluster,outputFilename = cluster(stylePF,3)
	putTogether(resultingPlayerCluster,outputFilename)
	resultingPlayerCluster,outputFilename = cluster(styleC,3)
	putTogether(resultingPlayerCluster,outputFilename)
	"""
	resultingPlayerCluster,outputFilename = cluster(stylePerformance,3)
	putTogether(resultingPlayerCluster,outputFilename)
	resultingPlayerCluster,outputFilename = cluster(stylePerformancePG,3)
	putTogether(resultingPlayerCluster,outputFilename)
	resultingPlayerCluster,outputFilename = cluster(stylePerformanceSG,3)
	putTogether(resultingPlayerCluster,outputFilename)
	resultingPlayerCluster,outputFilename = cluster(stylePerformanceSF,3)
	putTogether(resultingPlayerCluster,outputFilename)
	resultingPlayerCluster,outputFilename = cluster(stylePerformancePF,3)
	putTogether(resultingPlayerCluster,outputFilename)
	resultingPlayerCluster,outputFilename = cluster(stylePerformanceC,3)
	putTogether(resultingPlayerCluster,outputFilename)
	"""

if __name__ == "__main__":
	main()