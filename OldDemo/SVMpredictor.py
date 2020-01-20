# Uses a trained SVM to predict the validation set chosen
# args: model file, validation set file, name of results

import numpy as np 
from sklearn.svm import SVC
import sys
from joblib import dump, load 
import csv

clf = load(sys.argv[1])
data = np.loadtxt(sys.argv[2], delimiter=",")

results = open(sys.argv[3] +'.csv', "w+")
writer = csv.writer(results)

writer.writerow(clf.predict(data))

results.close()