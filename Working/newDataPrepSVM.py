#take sktime style csv and return csv for SVM fitting

#args: this file, feature file

import sys
import csv
import numpy as np

featureFile = sys.argv[1]
features = open(featureFile, "r")
reader = csv.reader(features, delimiter=',')
name = featureFile.split('.')

currSeq = []
allSeq = []
rowCount = 0
for row in reader:
    if rowCount != 0:
        currSeq.append(float(row[3]))
        if row[2] == '9' and row[1] == '5':
            allSeq.append(np.asarray(currSeq))
            currSeq = []
    rowCount+= 1
    


np.asarray(allSeq)

np.savetxt(name[0]+'SVM.csv', allSeq, delimiter=',')

