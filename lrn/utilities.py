# for any repeatedly used utility files

import os
import csv

import pathlib
import psutil
import random

def checkDataDrive(driveName):
    # validates that the drive is present, returns the drive name if it is. Not that cool.  
    if driveName in [i.device for i in psutil.disk_partitions()]:
        return driveName
    else:
        return False

def generateSubsetOfDataList(
    dataDrivePath, 
    numSamples=10,
    outputPath='samples',
    generateNewSubset=False):

    if(
        os.path.isfile(
            os.path.join(outputPath, '{}-selected-samples.txt'.format(numSamples))
        )
    ):
        if not generateNewSubset:
            return

    samplePool = []
    collectedSamples = []

    # make the sample pool of all available audio files
    for fold in os.listdir(dataDrivePath):
        d1 = os.path.join(dataDrivePath, fold)
        try:
            if os.path.isdir(d1):
                for f in os.listdir(d1):
                    d2 = os.path.join(d1, f)
                    if os.path.isdir(d2):
                        samplePool += os.listdir(d2)
        except:
            pass

    while len(collectedSamples) < numSamples:
        idx = random.randint(0, len(samplePool)-1)
        collectedSamples.append(samplePool[idx])

    with open(
        os.path.join(
                outputPath,
                '{}-selected-samples.txt'.format(numSamples)), 'w') as f:
                    for i in collectedSamples:
                        f.write(i + '\n')

if __name__ == "__main__":
    generateSubsetOfDataList('E:\\', 100)