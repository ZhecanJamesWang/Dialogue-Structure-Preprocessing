# -*- encoding: utf-8 -*-


import gensim, logging
import codecs

model = gensim.models.Word2Vec.load('./model/model2016-10-18T21:55:43.600754')


# print model.similarity('傻', '笨')
# print model.similarity('你们', '我们')
# print model.similarity('你们', '天空')
print model.similarity('他', '随便')
print model.similarity('天空', '学校')
print model.similarity('桌子', '吃饭')

# print model.similarity('笔记本', '屏幕')
# print model.similarity('皇后', '女人')
# print model.similarity('皇后', '皇上')
# print model.similarity('小孩', '男人')
# print model.similarity('小孩', '女孩')

# print model.similarity("保卫", "守卫")




# open = codecs.open
# f = open("./data/synonymDict.txt", 'r', 'utf-8')
# for line in f:
#     line = line.split(",")
#     break

# word1, word2 = line[0].strip().encode('UTF-8'), line[1].strip().encode('UTF-8')
# print word1 + " " + word2
# print model.similarity(word1, word2)
