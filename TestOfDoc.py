import jieba
import numpy as np
from isIdealString import *
import sys
import CrawlTitle
import time
import ToHTML
import sys


WordsToIndex = np.load("/home/shichun/anaconda3/envs/ChineseSpellingCheck/WordsToIndex.npy",allow_pickle=True).item()
BigramCounter = np.load("/home/shichun/anaconda3/envs/ChineseSpellingCheck/BigramCounter.npy",allow_pickle=True).item()

f = open(sys.argv[1])

file = f.read()

seg_list = jieba.cut(file,cut_all=False)#调用jieba库进行中文分词

SuspiciousList = []


counter = False
#获得我们的数据，并对测试文件进行分词。把没有在前后关系文档中出现的搭配放到 SuspiciousList 当中去。
#在 WordsToIndex 这个字典中，一个中文单词的 Index 其实是由一个计数器 Counter 给出的，每遇到一个新单词，Counter 这个变量都会自加 1。

#获取测试文件中的分词数据
for word in seg_list:
	if counter == False:
		PreviousWord = word
		counter = True
	else:
		if isIdealString(word,PreviousWord):
			if BigramCounter[WordsToIndex[PreviousWord],WordsToIndex[word]] == 0:
				SuspiciousList.append((PreviousWord,word))
		PreviousWord = word

print(SuspiciousList)
print(len(SuspiciousList))
print("\n")

time.sleep(1)


# get the worong word according to the result of search


WrongWordList = []

for pairs in SuspiciousList:
	question_word = ""
	question_word += pairs[0]
	question_word += pairs[1]
	res, NeedAutoCorrection = CrawlTitle.GetTitle(question_word)
	# print(res)
	if not CrawlTitle.CheckCorrectness(res, question_word) or NeedAutoCorrection:
		WrongWordList.append(pairs)
	time.sleep(0.5)

print(WrongWordList)
print(len(WrongWordList))

ToHTML.ToHTML(file,sys.argv[2], WrongWordList)
