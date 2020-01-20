# Creates and saves model of data as fit by the OC SVM
# args: data file, label file, name for model

import numpy as np 
from sklearn.svm import OneClassSVM
from sklearn.metrics import f1_score, precision_score, recall_score
import sys
from joblib import dump, load 
import csv

train = np.loadtxt(sys.argv[1], delimiter=",")
data = np.loadtxt(sys.argv[2], delimiter=",")
labels = np.loadtxt(sys.argv[3], delimiter=",")

clf = OneClassSVM(kernel='rbf', gamma='scale')
clf.fit(train)

dump(clf, sys.argv[3] + '.joblib')
predicted = clf.predict(data)

#Results of self test
selfResults = open(sys.argv[3] + 'selfResults.csv', "w+")
writer = csv.writer(selfResults)
writer.writerow([predicted])
selfResults.close()

#Results of self test recall
selfRecall = open(sys.argv[3] + 'selfRecall.csv', "w+")
writer = csv.writer(selfRecall)
writer.writerow([recall_score(labels, predicted)])
selfRecall.close()

#Results of self test precision
selfPrecision = open(sys.argv[3] + 'selfPrecision.csv', "w+")
writer = csv.writer(selfPrecision)
writer.writerow([precision_score(labels, predicted)])
selfPrecision.close()

#Results of self test f1 score
selfF1 = open(sys.argv[3] + 'selfF1.csv', "w+")
writer = csv.writer(selfF1)
writer.writerow([f1_score(labels, predicted)])
selfF1.close()