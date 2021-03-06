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
import re

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

## Checks if sequence file is properly formatted
def fileMalformed(dataFile):
    sequences = open(dataFile, 'r')
    reader = csv.reader(sequences, delimiter=',')
    numSequences = 0
    for row in reader:
        if (len(row[0]) != 10) or re.match(r"[^acdefghiklmnpqrstvwy]+", row[0].lower()) != None:
            return True
        numSequences+=1
    if numSequences<2:
        return True
    else:
        return False



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
    return allSeq, numSequences

def prepText(dataFile):
    reader = dataFile.split(', ')
    data = []
    numSequences = 0
    for row in reader:
        sequence = row.lower()
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

# Takes in a set of true labels and predicted labels and a sequence file and returns
# lists of false positives, false negatives, true positives, and true negatives
def confusionMatrixList(trueLabels, predLabels, sequenceFile):
    sequences = open(sequenceFile, 'r')
    reader = csv.reader(sequences, delimiter=',')
    falsePosList = ''
    falseNegList = ''
    truePosList = '' 
    trueNegList = ''
    i = 0
    for row in reader:
        if trueLabels[i] == predLabels[i]:
            if trueLabels[i] == 1:
                trueNegList+= '<br>'+row[0].upper()
            else:
                truePosList+=  '<br>'+row[0].upper()
        else:
            if trueLabels[i] == 1:
                falseNegList+=  '<br>'+row[0].upper()
            else:
                falsePosList+=  '<br>'+row[0].upper()
        i+=1

    return falsePosList[4:], falseNegList[4:], truePosList[4:], trueNegList[4:]

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
def testData(model, preppedData, labelFile, unpreppedData):
    labels = np.loadtxt(labelFile, delimiter= ',')
    prediction = model.predict(preppedData)
    truePos, trueNeg, falsePos, falseNeg = confusionMatrix(labels, prediction)
# display variables
    accuracy = str(((truePos+trueNeg)/(truePos+trueNeg+falsePos+falseNeg))*100)
    falsePosList, falseNegList, truePosList, trueNegList = confusionMatrixList(labels, prediction, unpreppedData)


    return accuracy, falsePosList, falseNegList, truePosList, trueNegList
    
def testSelfWeb(model, preppedData, numSequences, unpreppedData):
    labels = []
    for label in range(numSequences):
        labels.append(1)
    prediction = model.predict(preppedData)
    truePos, trueNeg, falsePos, falseNeg = confusionMatrix(labels, prediction)
# display variables
    accuracy = str("{:.2f}".format(((truePos+trueNeg)/(truePos+trueNeg+falsePos+falseNeg))*100))
    falsePosList, falseNegList, truePosList, trueNegList = confusionMatrixList(labels, prediction, unpreppedData)


    return accuracy, falsePosList, falseNegList, truePosList, trueNegList

# Uses prepped data and a model to make a prediction
def predict(model, preppedData, miniSequences):
    prediction = model.predict(preppedData)
    sequences = miniSequences.split(',')
    functional = ''
    for i in range(0, len(prediction)):
        if prediction[i] == 1:
            functional+='<br>'+str(i+1)+' '+sequences[i]+' '+str(i+10)
    return functional[4:]


# Turns a sequence string into an API recognizable csv
def getSequencesFromString(fullSequence):
    start = 0
    miniSequences = fullSequence[start:start+10]
    start+= 1
    while start+9 < len(fullSequence):
        miniSequences+= ', '+fullSequence[start:start+10]
        start+=1
    return miniSequences

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
            if data['USER INPUT']['gamma'] == 'scale':
                gamma = data['USER INPUT']['gamma']
            else:
                gamma = float(data['USER INPUT']['gamma'])
        else:
            gamma = data['DEFAULT']['gamma']
        if data['USER INPUT']['nu'] != '':
            nu = data['USER INPUT']['nu']
        else:
            data['DEFAULT']['nu']
        
        
        return (kernel, gamma, float(nu))