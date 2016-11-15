import numpy as np
import random
import matplotlib.pyplot as plt
import sys

def getRandomCentroids(data_set, n):

	data_set_copy = data_set.copy()
	np.random.shuffle(data_set_copy)
	return data_set_copy[:n]

def findClosestCentroids(data_set,data_to_cluster_mapping, centroids):

	sum = 0;
	distance = []

	for k, data_point in enumerate(data_set):
		for i, centroid in enumerate(centroids):
			for j, cluster_point in enumerate(centroid):
				sum += (data_point[j] - cluster_point)**2
			distance.append(sum)
			sum = 0
		data_to_cluster_mapping[k] = distance.index(min(distance))
		distance[:] = []

	return data_to_cluster_mapping

def findSeperateDataPerCluster(data_to_cluster_mapping, centroids):

	seperate_data_per_cluster = []

	for i, centroid in enumerate(centroids):
		seperate_data_per_cluster.append(np.where(data_to_cluster_mapping == i)[0])

	return seperate_data_per_cluster

def recenterCentroids(data_set, seperate_data_per_cluster, centroids):

	dictionary = {'f0':0, 'f1':0, 'f2':0, 'f3':0, 'f4':0, 'f5':0, 'f6':0}

	for j, x in enumerate(seperate_data_per_cluster):
		for index in x:
			for i, val in enumerate(data_set[index]):
				dictionary['f'+str(i)] = val + dictionary.get('f'+str(i))
		for key in dictionary:
			dictionary[key] = dictionary.get(key) / x.size	
		centroids[j] = dictionary.values()
		dictionary = dictionary.fromkeys(dictionary, 0)
	return centroids

def getObjectiveFunction(data_set, number_of_clusters):

	old_centroids = getRandomCentroids(data_set,number_of_clusters)

	count = 0

	while(1):

		data_to_cluster_mapping = np.random.randint(0,old_centroids.shape[0], size=(data_set.shape[0]))

		data_to_cluster_mapping = findClosestCentroids(data_set, data_to_cluster_mapping, old_centroids)

		seperate_data_per_cluster = findSeperateDataPerCluster(data_to_cluster_mapping, old_centroids)

		new_centroids = recenterCentroids(data_set, seperate_data_per_cluster, old_centroids.copy())

		if np.allclose(old_centroids,new_centroids):
			print 'No of iterations => ',count
			break
		else:
			old_centroids = new_centroids
		count += 1

	sum = 0;
	distance = []

	for i, data_point in enumerate(data_set):
		for j, cluster_point in enumerate(new_centroids[data_to_cluster_mapping[i]]):
			sum += (data_point[j] - cluster_point)**2

	return sum			 

def main():

	data = np.loadtxt("seeds_dataset.txt", delimiter="\t")

	# omit last column f data
	data_set = np.delete(data,7, axis=1)

	i = 1
	NC =  int(sys.argv[1])
	ObjFunc = []
	NoOfClusters = range(i,NC + 1)
	
	while i <= NC:
		ObjFunc.append(getObjectiveFunction(data_set,i))
		i += 1

	print ObjFunc
	print NoOfClusters	
		
	plt.plot(NoOfClusters, ObjFunc)
	plt.legend(['Number of Clusters','Objective Function'])
	plt.grid(True)
	plt.savefig("NKVsOFPlot.png")
	plt.show()

	
main()