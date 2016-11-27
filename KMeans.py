import numpy as np
import csv

from sklearn.cluster import KMeans

def main():
    data = []
    originalData = []
    ifp = open("Player Shooting Style Analysis-PG.csv","rb")
    reader = csv.reader(ifp)
    reader.next()
    for row in reader:
        data.append(row[2:5])
        originalData.append(row)
    classifier = KMeans(n_clusters = 3,n_jobs = 1)
    print data
    classifier.fit(data)
    clusterArray = classifier.predict(data)
    
    
if __name__ == "__main__":
    main()