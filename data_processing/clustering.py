# encoding: utf-8
import numpy as np
import math
import matplotlib.pyplot as plt
import json
import csv
from sklearn import metrics
from sklearn.cluster import DBSCAN
from scipy.spatial.distance import pdist, squareform


# DBSCAN clustering algorithm


def creationCluster(data_path, save_path):
    
    """ creat clusters
    args : data_path, save_path : path to the file that will be use        
    """
    database = database_path
    save = save_path
   
    X = []
    
    with open(database, "r") as f:
        reader = csv.reader(f)
        
        for line in reader:
            var = [line[2], line[3]]
            X.append(var)
        
        X = np.array(X, np.float)

    def calcul_distance_miles(lat1, lon1, lat2, lon2):

        """ calculate distance in miles 
       
        args : lat1, lon1,lat2,lon2 : latitudes and longitudes of 2 points
        returns : distance s in miles      
        
        """
        x = lon1 - lon2
        
        distance = math.sin(math.radians(lat1)) * math.sin(math.radians(lat2)) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(x))
        
        if distance - 1 > 0:
            distance = 1
        
        elif distance + 1 < 0:
            distance = -1
       
        distance = math.acos(distance)
        distance = math.degrees(distance)
        miles = distance * 60 * 1.1515
        
        return miles

    def distance_points(p1, p2):

        """ calculate distance between 2 points
       
        args : p1,p2, 2 points 
        returns : distance between 2 points in miles      
        
        """


        lat1, lon1 = p1
        lat2, lon2 = p2
        
        distance = calcul_distance_miles(lat1, lon1, lat2, lon2) * 1.609344
        
        return distance

    distance_of_matrix = squareform(pdist(X, (lambda u, v: distance_points(u, v))))
    
    print(distance_of_matrix)
   
   # fitting

    db = DBSCAN(eps=0.05, min_samples=3, metric='precomputed')
    labels = db.fit_predict(distance_of_matrix)

    

    mask_sample = np.zeros_like(labels, dtype=bool)
    mask_sample[db.core_sample_indices_] = True

    number_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    labels_unique = set(labels)
    
    colors = plt.cm.Spectral(np.linspace(0, 1, len(labels_unique)))

    center_point = []
    heatmap_point = []

    f_cluster = open(save, 'w', newline='')

    for k, col in zip(labels_unique, colors):
        
        if k == -1:
            col = 'k'

        mask_class_member= (labels == k)
        xy = X[mask_class_member & mask_sample]
        num_point_contained = len(xy)
        
        f_cluster.write(
            str(k) + ',' + str(len(xy)) + ',' + str(np.mean(xy[:, 0])) + ',' +
            str(np.mean(xy[:, 1])) + ',' + str(num_point_contained) + '\r')
        
        center_point.append([np.mean(xy[:, 1]), np.mean(xy[:, 0])])
       
        heatmap_point.append({
            "lng": np.mean(xy[:, 1]),
            "lat": np.mean(xy[:, 0]),
            "count": len(xy[:, 1])
        })

