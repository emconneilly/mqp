# Erin Conneilly 
# Oct 29, 2019
# Dataset creation: Sequences to Features

import sys
import csv
import os

# arguments: this file, sequence file name

# Define values
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

#Pass in sequence file
rawSequences = sys.argv[1]
sFile = open(rawSequences, "r")
reader = csv.reader(sFile, delimiter=',')
#Set up feature file
name = rawSequences.split('.')
featureFile = open(name[0] + 'Features.csv', 'w+')
writer = csv.writer(featureFile)
writer.writerow(['sequence_id', 'dim_id', 'aa', 'value'])
#Fill rows with sequence data
#'Hydropathy'= 0
#'Isoelectric Point'= 1
#'Molecular Weight'= 2
#'# of pKa Values'= 3
#'Lowest pKa'= 4
# 'Highest pKa'= 5
numSequences = 0
for row in reader:
    sequence = row[0].lower()
    aa = 0
    while aa<10:
        writer.writerow([numSequences, 0, aa, getHydropathy(sequence[aa])])
        writer.writerow([numSequences, 1, aa, getIP(sequence[aa])])
        writer.writerow([numSequences, 2, aa, getMW(sequence[aa])])
        writer.writerow([numSequences, 3, aa, getNumPKA(sequence[aa])])
        writer.writerow([numSequences, 4, aa, getLowPKA(sequence[aa])])
        writer.writerow([numSequences, 5, aa, getHighPKA(sequence[aa])])
        aa+= 1
    numSequences+= 1


featureFile.close()
sFile.close()

