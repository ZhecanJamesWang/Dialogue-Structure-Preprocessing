#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
=========================================================
Configure.py. Configure file that Contains All the Setting Options
=========================================================

"""

print(__doc__)
configure = {

##### Parameters for preProcess.py ####################################

    "databaseName":"tech", 
    # database names. choose either edu (education) or tech(technology)
    "userDictDir": "./data/userDict/userDictTxt/", # sougou dictionary directory for tokenization
    "outputDir": "./data/trainData/", # output directory for filtered data from preProcess.py
    "preOutputDir": "./data/previousTrainData/", # previous outputed data directory

##### Parameters for word2vec.py ####################################

    "sizes": [300],  #[100, 200, 300]   # could specify more values in the list when using grid search
    "min_counts": [3],  #range(1,6)  # could specify more values in the list when using grid search
    "workers": [1], #range(1, 5)   # could specify more values in the list when using grid search
    "preload": True, # flag for preloading model
    "debug": False, # debug flag for printing debug message
    "plot": True, # plot flag for showing the histogram 
    "testType": "random", 
    # testing type name 
    # "random" for random words test 
    # "pos" for synonym words test
    # "nega" for antonym words test
    "testDataDir": "./data/testdata/" # testing data directory
}
