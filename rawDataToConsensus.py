# Takes csv of all NES
# Creates csv of all consensus sequences and csv of all nonconsensus

#arguments: this file, file to be sorted
import sys
import re
import csv

def byConsensus(sequence):
    rand22 = re.findall("L.{2}[LIVMF].{2}L.[LI]", sequence)
    rand23 = re.findall("L.{2}[LIVMF].{3}L.[LI]", sequence)
    rand32 = re.findall("L.{3}[LIVMF].{2}L.[LI]", sequence)
    rand33 = re.findall("L.{3}[LIVMF].{3}L.[LI]", sequence)

    if rand22 or rand23 or rand32 or rand33:
        return True
    else:
        return False

filename = sys.argv[1]
sequences = open(filename, "r")
reader = csv.reader(sequences, delimiter=',')
name = filename.split('.')

consensus = csv.writer(open(name[0]+'Consensus.csv', "w+"))
non = csv.writer(open(name[0]+'Non.csv', "w+"))

for row in reader:
    if byConsensus(row[0]):
        consensus.writerow([row[0]])
    else:
        non.writerow([row[0]])

