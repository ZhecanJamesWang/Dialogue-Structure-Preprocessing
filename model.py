# -*- encoding: utf-8 -*-
"""
=========================================================
word2Vec.py.  The Word2Vec Training And Testing
=========================================================

"""
print(__doc__)

# import modules & set up logging
import gensim, logging
import os
import datetime
import codecs
import itertools
import matplotlib.pyplot as plt
import os
from configure import configure as conf
import utility as ut
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
 
class Model(object):
    """ class of word2vec model"""
    def __init__(self):        
        # hyper-parameters
        self.sizes = conf["sizes"]
        self.min_counts = conf["min_counts"]
        self.workers = conf["workers"]
        self.window = conf["window"]

        self.preload = conf["preload"]
        self.debug = conf["debug"]
        self.plot = conf["plot"]
        self.testType = conf["testType"]
        self.testDataDir = conf["testDataDir"]

        self.model = None
        self.maxScore = -100
        self.similarityArr = []
        self.currComb = None
        
    def generateComb(self):
        self.comb = list(itertools.product(self.sizes, self.min_counts, self.workers))

    def initData(self):
        self.data = ut.DocReader('./data/trainData/') # a memory-friendly iterator
        print "finish init data"


    def train(self):
        print "train model with "
        print self.currComb
        self.model = gensim.models.Word2Vec(self.data, size = self.sizes[0], min_count = self.min_counts[0], workers = self.workers[0], window = self.window[0])


    def saveModel(self):
        now = datetime.datetime.now()
        self.model.save('./model/model' + now.isoformat())
        print "successfully save model at " + now.isoformat()

    def preLoadModel(self):
        # If preLoad flag is True, this function will automatically load the most recent saved model
        # from model folder
        modelPath = "./model/"
        files = os.listdir(modelPath)
        count = -1
        file = files[count].strip()
        while ".npy" in file:
            count -=1 
            file = files[count].strip()

        print "########  loading model name ####### "
        print file
        self.model = gensim.models.Word2Vec.load(modelPath + file)
  
    def gridSearch(self):
        self.preload = False
        self.generateComb()
        for comb in self.comb:
            print "comb: ", comb
            self.currComb = list(comb)
            score = self.test()

            if self.maxScore < score:
                self.maxScore = score
                self.bestComb = self.currComb

            print "the best comb so far is: "
            print self.bestComb

    def test(self):

        if self.preload:
            self.preLoadModel()
        else:
            self.train()

        correct = 0
        counter = 0
        grossCounter = 0

        open = codecs.open
        if self.testType == "pos":
            f = open( self.testDataDir + "synonymDict.txt", 'r', 'utf-8')
        elif self.testType == "nega":
            f = open( self.testDataDir + "antonymDict.txt", 'r', 'utf-8')
        else:
            f = open( self.testDataDir + "randomDict.txt", 'r', 'utf-8')

        for line in f:
            grossCounter += 1
            line = line.split(",")
            if len(line) < 2:
                continue
            word1, word2 = line[0].strip().encode('UTF-8'), line[1].strip().encode('UTF-8')    
            try:
                similarity = self.model.similarity(word1, word2)
                if self.testType == "pos":
                    if similarity > .7:
                        correct += 1
                    elif similarity < 0.7 and self.debug:
                        print word1, " ", word2

                elif self.testType == "nega":
                    if similarity < .3:
                        correct += 1   
                    elif similarity > 0.3 and self.debug:
                        print word1, " ", word2
                        
                counter += 1 
                self.similarityArr.append(similarity)
            except Exception as e:
                if self.debug:
                    print "cannot compare: ", word1, " ", word2
                pass

        if counter == 0:
            counter = 1
        score = float(correct)/counter
        print "total comparison counter: ", grossCounter
        print "total successful comparison counter: ", counter
        print "the correct classify pencentage is: ", score

        if self.plot:
            self.plotFreq()

        return score
    
    def plotFreq(self):
        self.similarityArr = self.similarityArr * 100
        plt.hist(self.similarityArr, bins = 
            20)
        plt.xlabel("Value")
        plt.ylabel("Frequency")
        plt.show()


    def run(self):
        # self.initData()
        # self.train()
        # self.saveModel()
        # self.gridSearch()
        # self.test()
        pass

if __name__ == '__main__':
    Model().run()