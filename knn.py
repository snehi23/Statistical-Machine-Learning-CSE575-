import scipy.io
import math
import operator
from scipy import spatial
import numpy as np
import matplotlib.pyplot as plt

# It will load data from .mat file as python dictionary
def loadDataFromFile(filename, trainingSet=[] , testSet=[]):
	mat = scipy.io.loadmat(filename)

	for x in range(len(mat['traindata'])):
		trainingSet.append((mat['traindata'][x], mat['trainlabels'][x]))

	for x in range(len(mat['testdata'])):
		testSet.append((mat['testdata'][x], mat['testlabels'][x]))	

# cosine distance between two points
def cosineDistance(point1, point2):
	
	return spatial.distance.cosine(point1, point2);

# It return list of k closest neighbors
def findNGB(trainingSet, testInstance, k):
	distances = []
	length = len(testInstance)-1
	for x in range(len(trainingSet)):
		dist = cosineDistance(testInstance, trainingSet[x][0])
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors

# It will return Max Voted class label of neighbor instances
def findVotedLabel(neighbors):
	Votes = {}
	for x in range(len(neighbors)):
		label = neighbors[x][1][0]
		if label in Votes:
			Votes[label] += 1
		else:
			Votes[label] = 1				
	maxToMinVotes = sorted(Votes.iteritems(), key=operator.itemgetter(1), reverse=True)
	return maxToMinVotes[0][0]

# It will find error between predicted VS actual 
def findError(testSet, predictedLabels):
	missedPredictions = 0
	for x in range(len(testSet)):
		if testSet[x][1][0] != predictedLabels[x]:
			missedPredictions += 1
	return (missedPredictions/float(len(testSet))) * 100.0
	
def main():

	trainingSet=[]
	testSet=[]
	TestError = []
	TrainingError = []
	
	loadDataFromFile('faces.mat', trainingSet, testSet)

	predictedLabels =[]
	
	k = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

	for itr in range(len(k)):
		print k[itr]
		for x in range(len(testSet)):
			neighbors = findNGB(trainingSet, testSet[x][0], k[itr])
			result = findVotedLabel(neighbors)
			predictedLabels.append(result)
		TestError.append(findError(testSet, predictedLabels))
		predictedLabels=[]
	
	print TestError

	for itr in range(len(k)):
		print k[itr]
		for x in range(len(trainingSet)):
			neighbors = findNGB(trainingSet, trainingSet[x][0], k[itr])
			result = findVotedLabel(neighbors)
			predictedLabels.append(result)
		TrainingError.append(findError(trainingSet, predictedLabels))
		predictedLabels=[]
	
	print TrainingError

	plt.plot(k, TestError, k, TrainingError)
	plt.legend(['TestError', 'TrainingError'])
	plt.grid(True)
	plt.savefig("ErrorVsKPlot.png")
	plt.show()
	
main()
