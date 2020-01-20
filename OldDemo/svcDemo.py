from sklearn import preprocessing
from sklearn.svm import SVC
import numpy as np

# Import demo data
NES1 = np.loadtxt('trainingSets/NES/NES-0001.csv', delimiter=",")
NES2 = np.loadtxt('trainingSets/NES/NES-0002.csv', delimiter=",")
NES3 = np.loadtxt('trainingSets/NES/NES-0003.csv', delimiter=",")
NES4 = np.loadtxt('trainingSets/NES/NES-0004.csv', delimiter=",")
NES5 = np.loadtxt('trainingSets/NES/NES-0005.csv', delimiter=",")

ran1 = np.loadtxt('trainingSets/nonNES/ran-350-001.csv', delimiter=",")
ran2 = np.loadtxt('trainingSets/nonNES/ran-400-001.csv', delimiter=",")
ran3 = np.loadtxt('trainingSets/nonNES/ran-400-002.csv', delimiter=",")
ran4 = np.loadtxt('trainingSets/nonNES/ran-600-001.csv', delimiter=",")
ran5 = np.loadtxt('trainingSets/nonNES/ran-600-002.csv', delimiter=",")

# Flatten demo data
NES1 = NES1.flatten()
NES2 = NES2.flatten()
NES3 = NES3.flatten()
NES4 = NES4.flatten()
NES5 = NES5.flatten()

ran1 = ran1.flatten()
ran2 = ran2.flatten()
ran3 = ran3.flatten()
ran4 = ran4.flatten()
ran5 = ran5.flatten()

# Put demo data and labels into arrays
X = np.array([NES1, NES2, ran1, NES3, ran2, ran3, ran4, NES4, NES5, ran5])

maxLen =0
for sequence in X:
    if sequence.shape[0] > maxLen:
        maxLen = sequence.shape[0]
acc = 0
for sequence in X:
    sequence = np.pad(sequence, (0, maxLen-sequence.shape[0]), mode='constant', constant_values=0)
    X[acc] = sequence
    acc = acc + 1
X = np.stack(X)

Y = np.array([1, 1, 2, 1, 2, 2, 2, 1, 1, 2])

# Fit the data
clf = SVC(kernel='rbf', gamma='auto')
clf.fit(X, Y)

# Make a sample prediction (from training set)
predNES3 = np.pad(NES3, (0, maxLen-NES3.shape[0]), mode='constant', constant_values=0)
pred1 = np.array([predNES3])
pred1 = np.stack(pred1) 
print(clf.predict(pred1))

# Make some real predictions (all NES)
NES6 = np.loadtxt('validationSets/NES/NES-0006.csv', delimiter=",")
NES8 = np.loadtxt('validationSets/NES/NES-0008.csv', delimiter=",")
NES9 = np.loadtxt('validationSets/NES/NES-0009.csv', delimiter=",")
NES10 = np.loadtxt('validationSets/NES/NES-0010.csv', delimiter=",")

NES6 = NES6.flatten()
NES8 = NES8.flatten()
NES9 = NES9.flatten()
NES10 = NES10.flatten()

pred2 = np.array([NES6, NES8, NES9, NES10])
acc1 = 0
for sequence in pred2:
    sequence = np.pad(sequence, (0, maxLen-sequence.shape[0]), mode='constant', constant_values=0)
    pred2[acc1] = sequence
    acc1 = acc1 + 1
pred2 = np.stack(pred2)

print(clf.predict(pred2))