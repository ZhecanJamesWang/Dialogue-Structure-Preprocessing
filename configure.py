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
    "databaseName":"edu", 
    # database names. choose either edu (education) or tech(technology)
    "userDictDir": "./data/userDict/userDictTxt/", # sougou dictionary directory for tokenization
    "outputDir": "./data/trainData/", # output directory for filtered data from preProcess.py
    "preOutputDir": "./data/previousTrainData/", # previous outputed data directory
    "txtDataDir": "rawData/downloadData/book/txtFiles", # directory path for txt book data
    'ifRawData': False, # flag if saving data as its original directly from mongoDB
    'keywords': ["$"], # list of special keywords to reserve in filtering function

##### Parameters for model.py ####################################    
    # hyper-parameters, could specify more values in the list when using grid search
    "sizes": [100, 200, 300], #[300] or [100, 200, 300] 
    "min_counts": range(1,6), # [3] or range(1,6) 
    "workers": [5], # [5] or range(1, 5) 
    "window": [2, 3, 4, 5, 6], #[3] or [2, 3, 4, 5, 6] 
    
    "preload": True, # flag for preloading model
    "debug": False, # debug flag for printing debug message
    "plot": False, # plot flag for showing the histogram 
    "testType": "pos", 
    # testing type name 
    # "random" for random words test 
    # "pos" for synonym words test
    # "nega" for antonym words test
    "testDataDir": "./data/testdata/" # testing data directory
}
