import os

import librosa

import utilities

DATA_DRIVE = 'E:\\' # usb that the data is on

def run(trialSize = 100, generateNewSubset=False):
    '''
    Main task runner for this script.
    Select a trial size to randomly assemble a list of files to perform analysis on.
    Set trialSize to 'all' to run on entire dataset.
    Set generateNewSubset to 'True' if you've ran the same trial size before and want new samples.
    '''

    utilities.generateSubsetOfDataList(
        DATA_DRIVE,
        numSamples=100,
        generateNewSubset=generateNewSubset
        )