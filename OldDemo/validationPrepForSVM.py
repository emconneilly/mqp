# Takes a folder of csv's of features for each NES and returns a csv ready to be fit by SVM
# args: source directory, name for files, maxLen of training set
import numpy as np
import os
import sys


def loadAndFlatten(filename):
    loaded = np.loadtxt(filename, delimiter=",")
    flat = loaded.flatten()
    return flat

sourceDir = sys.argv[1]
dirList = os.listdir(sourceDir)
allSequences = []
allLabels = []

for f in dirList:
    name = f.split(".")
    if name[1] == 'csv':
        sequence = loadAndFlatten(sourceDir + f)
        allSequences.append(sequence)
        if 'NES' in name[0]:
            allLabels.append(1)
        else:
            allLabels.append(2)

acc = 0
for sequence in allSequences:
    sequencePad = np.pad(sequence, (0, int(sys.argv[3])-len(sequence)), 'mean')
    allSequences[acc] = sequencePad
    acc += 1

np.asarray(allSequences)
np.asarray(allLabels)

np.savetxt(sys.argv[2] + 'Data.csv', allSequences, delimiter=',')
np.savetxt(sys.argv[2] + 'Labels.csv', allLabels, delimiter=',')