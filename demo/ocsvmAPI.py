# API to train and test SVM Models for Nuclear Export Sequences
# Requires all sequence sets entered to have equivalent lengths
# Supports data entry by csv, sequences separated by new lines

#Author: Erin Conneilly
#Last Modified: 12/2/19

import sys
import csv
import numpy as np 
import pandas as pd 
from sklearn.svm import OneClassSVM
from sklearn.metrics import f1_score, precision_score, recall_score
import json

# Define values associated with each amino acid
def getHydropathy(aa):
    if aa == 'a':
        return '1.8'
    elif aa == 'r':
        return '-4.5'
    elif aa == 'n':
        return '-3.5'
    elif aa == 'd':
        return '-3.5'
    elif aa == 'c':
        return '2.5'
    elif aa == 'e':
        return '-3.5'
    elif aa == 'q':
        return '-3.5'
    elif aa == 'g':
        return '-0.4'
    elif aa == 'h':
        return '-3.2'
    elif aa == 'i':
        return '4.5'
    elif aa == 'l':
        return '3.8'
    elif aa == 'k':
        return '-3.9'
    elif aa == 'm':
        return '1.9'
    elif aa == 'f':
        return '2.8'
    elif aa == 'p':
        return '-1.6'
    elif aa == 's':
        return '-0.8'
    elif aa == 't':
        return '-0.7'
    elif aa == 'w':
        return '-0.9'
    elif aa == 'y':
        return '-1.3'
    elif aa == 'v':
        return '4.2'
    else:
        return ''

def getIP(aa):
    if aa == 'a':
        return '1.0'
    elif aa == 'r':
        return '-7.5'
    elif aa == 'n':
        return '-2.7'
    elif aa == 'd':
        return '-3.0'
    elif aa == 'c':
        return '0.2'
    elif aa == 'e':
        return '-2.6'
    elif aa == 'q':
        return '-2.9'
    elif aa == 'g':
        return '0.7'
    elif aa == 'h':
        return '-1.7'
    elif aa == 'i':
        return '3.1'
    elif aa == 'l':
        return '2.2'
    elif aa == 'k':
        return '-4.6'
    elif aa == 'm':
        return '1.1'
    elif aa == 'f':
        return '2.5'
    elif aa == 'p':
        return '-0.3'
    elif aa == 's':
        return '-1.1'
    elif aa == 't':
        return '-0.8'
    elif aa == 'w':
        return '1.5'
    elif aa == 'y':
        return '0.1'
    elif aa == 'v':
        return '2.3'
    else:
        return ''

def getMW(aa):
    if aa == 'a':
        return '89.1'
    elif aa == 'r':
        return '174.2'
    elif aa == 'n':
        return '132.1'
    elif aa == 'd':
        return '133.1'
    elif aa == 'c':
        return '121.2'
    elif aa == 'e':
        return '147.1'
    elif aa == 'q':
        return '147.1'
    elif aa == 'g':
        return '75.1'
    elif aa == 'h':
        return '155.2'
    elif aa == 'i':
        return '131.2'
    elif aa == 'l':
        return '131.2'
    elif aa == 'k':
        return '146.2'
    elif aa == 'm':
        return '149.2'
    elif aa == 'f':
        return '165.2'
    elif aa == 'p':
        return '115.1'
    elif aa == 's':
        return '105.1'
    elif aa == 't':
        return '119.1'
    elif aa == 'w':
        return '204.2'
    elif aa == 'y':
        return '181.2'
    elif aa == 'v':
        return '117.1'
    else:
        return ''

def getNumPKA(aa):
    if aa == 'a':
        return '2'
    elif aa == 'r':
        return '3'
    elif aa == 'n':
        return '2'
    elif aa == 'd':
        return '3'
    elif aa == 'c':
        return '3'
    elif aa == 'e':
        return '3'
    elif aa == 'q':
        return '2'
    elif aa == 'g':
        return '2'
    elif aa == 'h':
        return '3'
    elif aa == 'i':
        return '2'
    elif aa == 'l':
        return '2'
    elif aa == 'k':
        return '3'
    elif aa == 'm':
        return '2'
    elif aa == 'f':
        return '2'
    elif aa == 'p':
        return '2'
    elif aa == 's':
        return '2'
    elif aa == 't':
        return '2'
    elif aa == 'w':
        return '2'
    elif aa == 'y':
        return '3'
    elif aa == 'v':
        return '2'
    else:
        return ''

def getLowPKA(aa):
    if aa == 'a':
        return '2.35'
    elif aa == 'r':
        return '2.18'
    elif aa == 'n':
        return '2.02'
    elif aa == 'd':
        return '1.88'
    elif aa == 'c':
        return '1.71'
    elif aa == 'e':
        return '2.19'
    elif aa == 'q':
        return '2.17'
    elif aa == 'g':
        return '2.34'
    elif aa == 'h':
        return '1.78'
    elif aa == 'i':
        return '2.32'
    elif aa == 'l':
        return '2.36'
    elif aa == 'k':
        return '2.2'
    elif aa == 'm':
        return '2.28'
    elif aa == 'f':
        return '2.58'
    elif aa == 'p':
        return '1.99'
    elif aa == 's':
        return '2.21'
    elif aa == 't':
        return '2.15'
    elif aa == 'w':
        return '2.38'
    elif aa == 'y':
        return '2.2'
    elif aa == 'v':
        return '2.29'
    else:
        return ''

def getHighPKA(aa):
    if aa == 'a':
        return '9.87'
    elif aa == 'r':
        return '13.2'
    elif aa == 'n':
        return '8.8'
    elif aa == 'd':
        return '9.6'
    elif aa == 'c':
        return '10.78'
    elif aa == 'e':
        return '9.67'
    elif aa == 'q':
        return '9.13'
    elif aa == 'g':
        return '9.6'
    elif aa == 'h':
        return '8.97'
    elif aa == 'i':
        return '9.76'
    elif aa == 'l':
        return '9.6'
    elif aa == 'k':
        return '10.28'
    elif aa == 'm':
        return '9.21'
    elif aa == 'f':
        return '9.24'
    elif aa == 'p':
        return '10.6'
    elif aa == 's':
        return '9.15'
    elif aa == 't':
        return '9.12'
    elif aa == 'w':
        return '9.39'
    elif aa == 'y':
        return '10.1'
    elif aa == 'v':
        return '9.72'
    else:
        return ''

def getPropA(aa):
    if aa == 'a':
        return '1.42'
    elif aa == 'r':
        return '0.98'
    elif aa == 'n':
        return '0.67'
    elif aa == 'd':
        return '1.01'
    elif aa == 'c':
        return '0.70'
    elif aa == 'e':
        return '1.11'
    elif aa == 'q':
        return '1.51'
    elif aa == 'g':
        return '0.57'
    elif aa == 'h':
        return '1.00'
    elif aa == 'i':
        return '1.08'
    elif aa == 'l':
        return '1.21'
    elif aa == 'k':
        return '1.16'
    elif aa == 'm':
        return '1.45'
    elif aa == 'f':
        return '1.13'
    elif aa == 'p':
        return '0.57'
    elif aa == 's':
        return '0.77'
    elif aa == 't':
        return '0.83'
    elif aa == 'w':
        return '1.08'
    elif aa == 'y':
        return '0.69'
    elif aa == 'v':
        return '1.06'
    else:
        return ''

def getPropB(aa):
    if aa == 'a':
        return '0.83'
    elif aa == 'r':
        return '0.93'
    elif aa == 'n':
        return '0.89'
    elif aa == 'd':
        return '0.54'
    elif aa == 'c':
        return '1.19'
    elif aa == 'e':
        return '1.10'
    elif aa == 'q':
        return '0.37'
    elif aa == 'g':
        return '0.75'
    elif aa == 'h':
        return '0.87'
    elif aa == 'i':
        return '1.60'
    elif aa == 'l':
        return '1.30'
    elif aa == 'k':
        return '0.74'
    elif aa == 'm':
        return '1.05'
    elif aa == 'f':
        return '1.38'
    elif aa == 'p':
        return '0.55'
    elif aa == 's':
        return '0.75'
    elif aa == 't':
        return '1.19'
    elif aa == 'w':
        return '1.37'
    elif aa == 'y':
        return '1.47'
    elif aa == 'v':
        return '1.70'
    else:
        return ''

# Takes in the filename of the dataset, filename of the labels, and training parameters
# Returns a dataframe of the dataset features and the model
def prepFile(dataFile):
    sequences = open(dataFile, 'r')
    reader = csv.reader(sequences, delimiter=',')
    data = []
    numSequences = 0
    for row in reader:
        sequence = row[0].lower()
        aa = 0
        while aa<10:
            data.append([numSequences, 0, aa, getHydropathy(sequence[aa])])
            data.append([numSequences, 1, aa, getIP(sequence[aa])])
            data.append([numSequences, 2, aa, getMW(sequence[aa])])
            data.append([numSequences, 3, aa, getNumPKA(sequence[aa])])
            data.append([numSequences, 4, aa, getLowPKA(sequence[aa])])
            data.append([numSequences, 5, aa, getHighPKA(sequence[aa])])
            aa+= 1
        numSequences+= 1

    sequences.close()

    df = pd.DataFrame(data, columns= ['seqID', 'dimension', 'aaNum', 'value'])
    currSeq = []
    allSeq = []
    for row in df.index:
        currSeq.append(float(df['value'][row]))
        if df['aaNum'][row] == 9 and df['dimension'][row] == 5:
            allSeq.append(np.asarray(currSeq))
            currSeq = []

    np.asarray(allSeq)
    return allSeq

#removing high+low pka
def prepFileDel(dataFile):
    sequences = open(dataFile, 'r')
    reader = csv.reader(sequences, delimiter=',')
    data = []
    numSequences = 0
    for row in reader:
        sequence = row[0].lower()
        aa = 0
        while aa<10:
            data.append([numSequences, 0, aa, getHydropathy(sequence[aa])])
            data.append([numSequences, 1, aa, getIP(sequence[aa])])
            data.append([numSequences, 2, aa, getMW(sequence[aa])])
            data.append([numSequences, 3, aa, getNumPKA(sequence[aa])])
            aa+= 1
        numSequences+= 1

    sequences.close()

    df = pd.DataFrame(data, columns= ['seqID', 'dimension', 'aaNum', 'value'])
    currSeq = []
    allSeq = []
    for row in df.index:
        currSeq.append(float(df['value'][row]))
        if df['aaNum'][row] == 9 and df['dimension'][row] == 3:
            allSeq.append(np.asarray(currSeq))
            currSeq = []

    np.asarray(allSeq)
    return allSeq

#adding prop A+B
def prepFileAdd(dataFile):
    sequences = open(dataFile, 'r')
    reader = csv.reader(sequences, delimiter=',')
    data = []
    numSequences = 0
    for row in reader:
        sequence = row[0].lower()
        aa = 0
        while aa<10:
            data.append([numSequences, 0, aa, getHydropathy(sequence[aa])])
            data.append([numSequences, 1, aa, getIP(sequence[aa])])
            data.append([numSequences, 2, aa, getMW(sequence[aa])])
            data.append([numSequences, 3, aa, getNumPKA(sequence[aa])])
            data.append([numSequences, 4, aa, getLowPKA(sequence[aa])])
            data.append([numSequences, 5, aa, getHighPKA(sequence[aa])])
            data.append([numSequences, 6, aa, getPropA(sequence[aa])])
            data.append([numSequences, 7, aa, getPropB(sequence[aa])])
            aa+= 1
        numSequences+= 1

    sequences.close()

    df = pd.DataFrame(data, columns= ['seqID', 'dimension', 'aaNum', 'value'])
    currSeq = []
    allSeq = []
    for row in df.index:
        currSeq.append(float(df['value'][row]))
        if df['aaNum'][row] == 9 and df['dimension'][row] == 7:
            allSeq.append(np.asarray(currSeq))
            currSeq = []

    np.asarray(allSeq)
    return allSeq

#replacing high+low pka with prop A+B
def prepFileReplace(dataFile):
    sequences = open(dataFile, 'r')
    reader = csv.reader(sequences, delimiter=',')
    data = []
    numSequences = 0
    for row in reader:
        sequence = row[0].lower()
        aa = 0
        while aa<10:
            data.append([numSequences, 0, aa, getHydropathy(sequence[aa])])
            data.append([numSequences, 1, aa, getIP(sequence[aa])])
            data.append([numSequences, 2, aa, getMW(sequence[aa])])
            data.append([numSequences, 3, aa, getNumPKA(sequence[aa])])
            data.append([numSequences, 4, aa, getPropA(sequence[aa])])
            data.append([numSequences, 5, aa, getPropB(sequence[aa])])
            aa+= 1
        numSequences+= 1

    sequences.close()

    df = pd.DataFrame(data, columns= ['seqID', 'dimension', 'aaNum', 'value'])
    currSeq = []
    allSeq = []
    for row in df.index:
        currSeq.append(float(df['value'][row]))
        if df['aaNum'][row] == 9 and df['dimension'][row] == 5:
            allSeq.append(np.asarray(currSeq))
            currSeq = []

    np.asarray(allSeq)
    return allSeq

#Takes in a set of true and predicted labels and returns:
#the true positives, true negatives, false positives, and false negatives
def confusionMatrix(trueLabels, predLabels):
    falsePos = 0
    falseNeg = 0
    truePos = 0
    trueNeg = 0
    for i in range(len(trueLabels)):
        if trueLabels[i] == predLabels[i]:
            if trueLabels[i] == 1:
                trueNeg+= 1
            else:
                truePos+= 1
        else:
            if trueLabels[i] == 1:
                falseNeg+= 1
            else:
                falsePos+= 1
    return truePos, trueNeg, falsePos, falseNeg

# Takes in prepped data, filename of labelFile, and optional training parameters
# parameters default to the best performing all NES model
# Creates a results summary file returns the trained model
# **want recall to be higher**
def train(preppedData, configName):
    settings = parseConfig(configName)
    model = OneClassSVM(kernel=settings[0], gamma=settings[1], nu=float(settings[2]))
    model.fit(preppedData)
 
    return model

#Takes in model, prepped test data, filename of the labels for the test data
#Prints a results summary for the performance of the model on the test data
def testData(model, preppedData, labelFile):
    labels = np.loadtxt(labelFile, delimiter= ',')
    prediction = model.predict(preppedData)
    
    print('Test Results:')
    print('True Labels: ' + str(labels))
    print('Predicted Labels: ' + str(prediction))
    truePos, trueNeg, falsePos, falseNeg = confusionMatrix(labels, prediction)
    print('True Positives: ' + str(truePos))
    print('True Negatives: ' + str(trueNeg))
    print('False Positives: ' + str(falsePos))
    print('False Negatives: ' + str(falseNeg))
    print('Recall: ' + str(recall_score(labels, prediction)))
    print('Precision: ' + str(precision_score(labels, prediction)))
    print('Accuracy: ' + str((truePos+trueNeg)/(truePos+trueNeg+falsePos+falseNeg)))
    
#TestData, but saves to a file
def testDataSave(model, preppedData, labelFile, fname, testName):
    save = open(fname+'.txt', 'a')
    labels = np.loadtxt(labelFile, delimiter= ',')
    prediction = model.predict(preppedData)
    
    save.write(testName+' Test Results:\n')
    save.write('True Labels: ' + str(labels)+'\n')
    save.write('Predicted Labels: ' + str(prediction)+'\n')
    truePos, trueNeg, falsePos, falseNeg = confusionMatrix(labels, prediction)
    save.write('True Positives: ' + str(truePos)+'\n')
    save.write('True Negatives: ' + str(trueNeg)+'\n')
    save.write('False Positives: ' + str(falsePos)+'\n')
    save.write('False Negatives: ' + str(falseNeg)+'\n')
    save.write('Recall: ' + str(recall_score(labels, prediction))+'\n')
    save.write('Precision: ' + str(precision_score(labels, prediction))+'\n')
    save.write('Accuracy: ' + str((truePos+trueNeg)/(truePos+trueNeg+falsePos+falseNeg))+'\n\n')

    save.close()

#Creates a config file
def createConfig(kernel='', gamma='', nu='', configName='config'):
    data = {'DEFAULT': {'kernel':'rbf', 'gamma':'scale', 'nu':'0.2'}}
    data['USER INPUT'] = {'kernel':kernel, 'gamma':gamma, 'nu':nu}
    with open(configName+'.json', 'w+') as outfile:
        json.dump(data, outfile)
    return configName+'.json'

#Parses a config file
def parseConfig(filename='config'):
    with open(filename, 'r') as config:
        data = json.load(config)
        if data['USER INPUT']['kernel'] != '':
            kernel = data['USER INPUT']['kernel']
        else:
            kernel = data['DEFAULT']['kernel']
        if data['USER INPUT']['gamma'] != '':
            gamma = float(data['USER INPUT']['gamma'])
        else:
            gamma = data['DEFAULT']['gamma']
        if data['USER INPUT']['nu'] != '':
            nu = data['USER INPUT']['nu']
        else:
            nu = data['DEFAULT']['nu']
        
        return (kernel, gamma, float(nu))