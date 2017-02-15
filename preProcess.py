# -*- encoding: utf-8 -*-
"""
=========================================================
Preprocess.py. The Data Preprocessing Workflow Before Word2Vec Model Training
=========================================================

"""
print(__doc__)
# import pandas
from pymongo import MongoClient
import codecs  
import jieba
import os
import datetime
from configure import configure as conf
import shutil
import utility as ut

class PreProcess(object):
    """This script preprocess the data brefore word2vec model training"""
    def __init__(self):
        self.contentList = []
        self.preContent = ""
        self.loadUserDict()
        self.connectMongo()
        self.firstSave = True

    def initTxtData(self): 
        self.outputName = "txtBookContent"           
        self.data = ut.DocReader(conf["txtDataDir"]) # a memory-friendly iterator
        print "finish init data"

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

    def writeToFile(self, outputName = None):
        if outputName == None:
            outputName = self.outputName
        if conf['ifRawData']: 
            outputName = "rawEduWeiboContent"
        # if self.firstSave:
        #     if os.path.isfile(conf["outputDir"] + outputName + ".txt"):
        #         now = datetime.datetime.now().isoformat()
        #         shutil.move(conf["outputDir"] + outputName + ".txt", conf["preOutputDir"] + outputName + now + ".txt" )
        #     self.firstSave = False

        if self.firstSave:
            self.now = datetime.datetime.now().isoformat()
            self.firstSave = False

        with codecs.open(conf["outputDir"] + outputName + self.now + ".txt", "a", encoding="utf-8") as f:  
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


        # remove @ fron line
        if "@" in line:
            counter = 0
            while "@" in line:
                if counter > 10:
                    break
                # print "@ OUTSIDE ", line
                header = line.index("@")
                ender = 0
                while ender < header:
                    if counter > 10:
                        break
                    # print "@ inside ", line
                    try:
                        ender = line[ender:].index(":")
                    except Exception as e:
                        try:
                            ender = line[ender:].index(" ")
                        except Exception as e:
                            ender = header
                            break
                    counter += 1

                line = line[:header] + "$" + line[ender + 1:]
                counter += 1
        # remove http url fron line
        if "http." or "www." in line:
            counter = 0
            slashFlag = False
            while "http." in line or "www." in line:
                if counter > 10:
                    break
                print "outside ", counter
                if "http." in line:
                    header = line.index("http")
                    if "html" in line:
                        ender = line.index("html") + 4
                    elif ".com" in line:
                        ender = line.index(".com") + 4
                    else:
                        ender = header
                    first = line[:header]
                    left = line[ender:]
                    searchArea = left[:ender + 20]
                    print searchArea
                    while "/" in searchArea:
                        if counter > 10:
                            break
                        ender = searchArea.index("/")
                        searchArea = searchArea[ender + 1:]
                        print "searchArea: ", searchArea
                        counter += 1
                    ender = left.index(searchArea)
                    line = first + left[ender:]

                elif "www." in line:
                    header = line.index("www")
                    if "html" in line:
                        ender = line.index("html") + 4
                    elif ".com" in line:
                        ender = line.index(".com") + 4
                    else:
                        ender = header
                    first = line[:header]
                    left = line[ender:]
                    searchArea = left[:ender + 20]

                    if "/" in line:
                        slashFlag = True            
                    while "/" in searchArea:
                        if counter > 10:
                            break
                        print searchArea
                        ender = searchArea.index("/")
                        searchArea = searchArea[ender + 1:]
                        print "searchArea: ", searchArea
                        counter += 1

                    print "searchArea: ", searchArea   
                    if slashFlag:         
                        ender = left.index(searchArea)
                    line = first + left[ender:]
                counter += 1

        for i in range(len(line)):
            word = line[i]
            # add han zi
            if self.ishan(word):
                content += word
            # add letter
            elif word.strip().isalpha():
                content += word
            # elif word.strip() == "@":
            #     wordCount = 0
            #     spaceCount = 0
            #     j = i + 1
            #     if j < len(line) - 1:
            #         while line[j] == " " :
            #             spaceCount += 1
            #             j += 1
            #             if j > len(line) - 1:
            #                 break
            #         if j < len(line) - 1:
            #             while line[j] != " " :
            #                 wordCount += 1
            #                 j += 1
            #                 if j > len(line) - 1:
            #                     break
            #             j += 1
            #             if wordCount > 0 and spaceCount > 0 and j < len(line) - 1:
            #                 if line[j] != " " :
            #                     content += "$"
            #     else:
            #         content += " "
            
            # keep numbers
            elif word.strip().isdigit():
                content += word.strip()
            # keep keywords
            elif word.strip() in conf['keywords']:
                content += word.strip()
            else:
                content += " "

        seg_list = jieba.cut(content, cut_all=False)
        content = " ".join(seg_list)
        return content

    def collectDataMongo(self):
        print "collect data from mongoDB"
        counter = 0
        self.contentList = []
        for record in self.cursor:
            if "content" in record:
                content = record["content"]
                if not conf['ifRawData']:
                    content = self.filter(content)
                comments = []
                if "comments" in record:
                    preComment = None
                    for comment in record['comments']:
                        if preComment != comment:
                            preComment = comment
                            if conf['ifRawData']:
                                comment = comment['content']
                            else:
                                comment = self.filter(comment['content'])
                            comments.append(comment)
                        
                if content != self.preContent:
                    self.contentList.append(content)
                    if len(comments) != 0:
                        self.contentList.extend(comments)
                        counter += len(comments)
                    self.preContent = content
                    counter += 1


            if counter%100 == 0:
                print "counter: ", counter
                self.writeToFile()
                self.contentList = []

        if len(self.contentList) != 0:
            self.writeToFile()
            self.contentList = []
            print "final counter: ", counter
        print "finish writing data from MongoDB to file"
        self.firstSave = True

    def collectDataTxt(self):
        print "collect data from txt books"
        counter = 0
        failCounter = 0

        self.contentList = []
        self.initTxtData()
        for line in self.data:
            if line != []:
                try:
                    line = line[0].decode('utf-8')
                    content = self.filter(line)
                    self.contentList.append(content)
                    counter += 1
                except Exception as e:
                    failCounter +=1 
                    # print "fail to decode: ", line
                    print "fail line counter: ", failCounter
            if counter%100 == 0:
                print "counter: ", counter
                self.writeToFile()
                self.contentList = []
        if len(self.contentList) != 0:
            # self.writeToFile()
            self.contentList = []
            print "final counter: ", counter
        print "finish writing data from txt book resource to file"
        self.firstSave = True

    def run(self):
        # self.collectDataMongo()
        self.collectDataTxt()


if __name__ == '__main__':
    print "start running preProcessing.run()"
    PreProcess().run()





        
