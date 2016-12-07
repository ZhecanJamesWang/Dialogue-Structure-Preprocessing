## Dependency

1. The most simple way is to download anaconda since it includes most commonlibraries
       
     anaconda (python and basic libraries) 
     https://www.continuum.io/downloads

2. The following are some common libraries, they may be included in the anaconda already. If not, you could use pip install to get them(pip in included in anaconda):

    matplotlib https://github.com/rueckstiess/mtools/wiki/matplotlib-Installation-Guide-for-Mac-OS-X
    pandas  http://pandas.pydata.org/pandas-docs/version/0.17.1/install.htmlgc

3. These libraries are for sure not included in anaconda and you need to install them separately. 
    
    jieba (preprocessing中的中文断句) https://github.com/fxsjy/jieba
    gensim(for word2vec) https://radimrehurek.com/gensim/install.html
    cola (for crawling info) https://github.com/chineking/cola/wiki
    mongo db (database platform associated with crawling)  https://docs.mongodb.com/v3.0/tutorial/install-mongodb-on-os-x/
    pymongo (library to interface between mongo database and python)http://api.mongodb.com/python/current/installation.html
    sublime text (General IDE) https://www.sublimetext.com/3

## Directory
-data
    -testData  include 3 word dictionaries (synonym, antonym and random shuffle)
    -trainData  train data from weibo and wiki
    -previousTrainData 
    every time when preProcess generate new data, it will automatically move the old data into this folder for backup 
    -userDict sougou dictionaries for tokenization
-model directories for saving past models

## Main Files

configure.py   file for storing all the configuration parameters
main.py      main file for running 
preProcess.py file for preprocessing data before word2Vec training
word2Vec.py  file for training word2vec model

## Use

1. preProcess Data
uncomment following line in main.py
  
  PreProcess().run()

2. Train and Save Model
uncomment following line in main.py

    model = Model()
    model.initData()
    model.train()
    model.saveModel()


3. Test Model and Plot Histogram

uncomment following line in main.py

    model = Model()
    model.test()

change following line in configure.py

    "preload": True,            # flag for preloading model
    "plot": True,               # plot flag for showing the histogram 
    "testType": "random", 
                                # testing type name 
                                # "random" for random words test 
                                # "pos" for synonym words test
                                # "nega" for antonym words test 

4. Grid Search

uncomment following line in main.py

    model = Model()
    model.initData()
    model.gridSearch()

change following line in configure.py

    "testType": "random", 
                                # testing type name 
                                # "random" for random words test 
                                # "pos" for synonym words test
                                # "nega" for antonym words test 
