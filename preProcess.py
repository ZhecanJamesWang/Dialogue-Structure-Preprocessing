# -*- encoding: utf-8 -*-
"""
=========================================================
Preprocess.py. The Data Preprocessing Workflow Before Word2Vec Model Training
=========================================================

"""
print(__doc__)
import pandas
from pymongo import MongoClient
import codecs  
import jieba
import os
import datetime
from configure import configure as conf
import shutil


class PreProcess(object):
    """This script preprocess the data brefore word2vec model training"""
    def __init__(self):
        self.contentList = []
        self.counter = 0
        self.preContent = ""
        self.loadUserDict()
        self.connectMongo()
        self.firstSave = True

    def connectMongo(self):
        self.client = MongoClient()
        print "database names: ", self.client.database_names()
 
        if conf["databaseName"] == "edu":
            self.db = self.client.sinaweiboEdu
            self.outputName = "eduWeiboContent"
        elif conf["databaseName"] == "tech":
            self.db = self.client.sinaweibo
            self.outputName = "techWeiboContent"
        else:
            raise Exception("Given database name does not exist")

        print "collection names: ", self.db.collection_names()
        self.Tweets = self.db.micro_blog
        self.cursor = self.Tweets.find()


    def loadUserDict(self):
        files = os.listdir(conf["userDictDir"])  
        for file in files:
            if ".txt" in file:
                jieba.load_userdict(conf["userDictDir"] + file)

    def ishan(self, text):
        # for python 2.x, 3.3+
        # sample: ishan(u'一') == True, ishan(u'我&&你') == False
        return all(u'\u4e00' <= char <= u'\u9fff' for char in text)

    def writeToFile(self):
        if self.firstSave:
            if os.path.isfile(conf["outputDir"] + self.outputName + ".txt"):
                now = str(datetime.datetime.now())
                shutil.move(conf["outputDir"] + self.outputName + ".txt", conf["preOutputDir"] + self.outputName + now + ".txt" )
            self.firstSave = False

        with codecs.open(conf["outputDir"] + self.outputName + ".txt", "a", encoding="utf-8") as f:  
            for sentence in self.contentList:
                f.write(sentence + "\n")

    def filter(self, line):
        content = ""
        # for word in line:
        #     if self.ishan(word):
        #         content += word
        #     elif word.strip().isalpha():
        #         content += word
        #     elif word.strip() == "@":
        #         content += word.strip() 
        #     elif word.strip().isdigit():
        #         content += word.strip()
        #     else:
        #         content += " "

        for i in range(len(line)):
            word = line[i]
            if self.ishan(word):
                content += word
            elif word.strip().isalpha():
                content += word
            elif word.strip() == "@":
                wordCount = 0
                spaceCount = 0
                j = i + 1
                if j < len(line) - 1:
                    while line[j] == " " :
                        spaceCount += 1
                        j += 1
                        if j > len(line) - 1:
                            break
                    if j < len(line) - 1:
                        while line[j] != " " :
                            wordCount += 1
                            j += 1
                            if j > len(line) - 1:
                                break
                        j += 1
                        if wordCount > 0 and spaceCount > 0 and j < len(line) - 1:
                            if line[j] != " " :
                                content += "$"
                else:
                    content += " "
            elif word.strip().isdigit():
                content += word.strip()
            else:
                content += " "

        seg_list = jieba.cut(content, cut_all=False)
        content = " ".join(seg_list)
        return content


    def run(self):
        for record in self.cursor:
            if "content" in record:
                content = record["content"]
                content = self.filter(content)

                comments = []
                if "comments" in record:
                    preComment = None
                    for comment in record['comments']:
                        if preComment != comment:
                            preComment = comment
                            comment = self.filter(comment['content'])
                            comments.append(comment)
                        
                if content != self.preContent:
                    self.contentList.append(content)
                    if len(comments) != 0:
                        self.contentList.extend(comments)
                        self.counter += len(comments)
                    self.preContent = content
                    self.counter += 1


            if self.counter%100 == 0:
                print "counter: ", self.counter
                self.writeToFile()
                self.contentList = []

        if len(self.contentList) != 0:
            self.writeToFile()
            print "final counter: ", self.counter
        print "finish writing to file"



if __name__ == '__main__':
    print "start running preProcessing.run()"
    PreProcess().run()





        
