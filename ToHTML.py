# -*- coding: utf-8 -*-
import mistune

def AddWrongWord(htmlpage, WrongWordList):
	InsertPosition = []
	# flag 变量的目的是标明前一个需要高亮的单词的末尾位置
    # 防止出现多次高亮，重复高亮的情况
	flag = -1
	for item in WrongWordList:
		WrongWords = ""
		WrongWords += item[0]
		WrongWords += item[1]
		
		Ins_start = htmlpage.find(WrongWords)
		# 如果找不到
		if Ins_start == -1:
			print("Cannot find the Wrong Word" + WrongWords)
			continue
		else:
		# 如果两个需要高亮的单词没有重复
			if Ins_start > flag :
				Ins_end = Ins_start + len(WrongWords)
				flag = Ins_end
			 # 如果有重复
			else:
				Ins_end = Ins_start + len(WrongWords)
				Ins_start = flag
				flag = Ins_end

		InsertPosition.append((Ins_start,Ins_end))

	
	 # 根据插入位置进行<mark> 高亮
	NewPage = ""
	PreviousStart = 0
	for item in InsertPosition:
		NewPage += htmlpage[PreviousStart:item[0]]
		NewPage += "<mark>"
		NewPage += htmlpage[item[0]:item[1]]
		NewPage += "</mark>"
		PreviousStart = item[1]

	return NewPage

# file 是我们的 MarkDown 文件
# OutputName 是我们最终生成的HTML文件的名称
# WrongWordList 是我们之前求出的错误单词列表
def ToHTML(file, OutputName, WrongWordList):
	 # 生成一个 Markdown 对象
	markdown = mistune.Markdown()

	# 进行 MarkDown 解析
	htmlpage = markdown(file)
	# AddWrongWord 是高亮错误单词的函数
	htmlpage = AddWrongWord(htmlpage,WrongWordList)

	try:
		OutputFile = open(OutputName,'r+')
	except FileNotFoundError:
		OutputFile = open(OutputName,'w')
	# 向HTML文件中写入必要的信息以正确显示中文
	OutputFile.write("<head>\n")
	OutputFile.write("<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/>")
	OutputFile.write("</head>\n")
	 # 写入 HTML 文本
	OutputFile.write(htmlpage)

