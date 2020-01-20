# Creates and saves model of data as fit by the SVM
# args: data file, label file, name for model

import numpy as np 
from sklearn.svm import SVC
import sys
from joblib import dump, load 

data = np.loadtxt(sys.argv[1], delimiter=",")
labels = np.loadtxt(sys.argv[2], delimiter=",")

clf = SVC(kernel='rbf', gamma='auto')
clf.fit(data, labels)

dump(clf, sys.argv[3] + '.joblib')
