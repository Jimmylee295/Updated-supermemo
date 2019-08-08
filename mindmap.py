#coding=GBK
import xmind
import time
import json
from nltk.corpus import wordnet
import urllib.request
from lxml import etree
from functools import reduce
from openpyxl import load_workbook

class mindmap():
	def __init__(self):
		with open('messstatus.json', 'r', encoding='utf-8') as json_file:
			messstatus = json.loads(json_file.read())
			self.messstatus = json.loads(messstatus)

		try:
			with open('vocabulary.json', 'r', encoding='utf-8') as json_file:
				vocabulary = json.loads(json_file.read())
				self.vocabulary = json.loads(vocabulary)
		except:
			print("单词本中空空如也")

		with open('fbdict.json', 'r', encoding='utf-8') as json_file:
			fbdict = json.loads(json_file.read())
			self.fbdict = json.loads(fbdict)

		self.synonym = {}
		self.antonym = {}
		self.conjugate = {}
		self.phrase = {}
		self.sentence = {}
		

	def syn(self,fbxmind):    # 近义词
		if 2 in fbxmind:   # 根据用户需求判断是否需要寻找近义词
			for x in list(self.fbdict.keys()):
				syn_list = []
				for syn in wordnet.synsets(x):  # 获得词集
					for lm in syn.lemmas():  # 获得词条
						syn_list.append(lm.name())  # 将同义词添加到列表
				syn_list1 = []
				[syn_list1.append(i) for i in syn_list if not i in syn_list1]  # 去除列表重复项
				for y in syn_list1:
					if y in list(self.fbdict.keys()):
						syn_list1.remove(y)  # 去除列表中和原词相同的单词
				syn_list1 = syn_list1[:3]  # 截取列表中的前三个单词
				self.synonym[x] = syn_list1

		# 反义词
	def ant(self,fbxmind):
		if 3 in fbxmind:
			for x in list(self.fbdict.keys()):
				ant_list = []
				for syn in wordnet.synsets(x):  # 获得词集
					for lm in syn.lemmas():  # 获得词条
						if lm.antonyms():
							ant_list.append(lm.antonyms()[0].name())  # 将反义词添加到列表
				ant_list1 = list(set(ant_list))  # 去除列表重复项
				self.antonym[x] = ant_list1
            
	#从有道词典爬取同根词
	def con(self,fbxmind):
		if 4 in fbxmind:
			for x in list(self.fbdict.keys()):
				#获得页面
				url="http://dict.youdao.com/w/eng/"+x+"/#keyfrom=dict2.index"
				res=urllib.request.urlopen(url)
				page=res.read()
	
				#获得同根词
				tree=etree.HTML(page) #使用etree对html解析
				dir(tree)
				try:
					w1=tree.xpath("//div[@id='relWordTab']//text()")  #利用xpath提取同根词部分文本
				except IndentationError:
					w1=[]
			
				#处理文件形成字典，格式为{单词:[词性1 同根词1 释义1,……],……}
				w2=[]
				for i in w1:
					i1=str(i).strip()   #去掉列表元素前后的空格和换行符
					w2.append(i1)
					w2=[i for i in w2 if i!=""]   #去除列表空元素
	
				#将列表元素分类
				try:
					for i in w2[w2.index("词根：")+1:w2.index("adj.")]:
						s1="词根："+i
				except ValueError:
					s1=""
		
				try:
					s2="adj. "
					for i in w2[w2.index("adj.")+1:w2.index("adv.")]:
						s2=s2+" "+i
				except ValueError:
					s2=""	

				try:
					s3="adv. "
					for i in w2[w2.index("adv.")+1:w2.index("n.")]:
						s3=s3+" "+i
				except ValueError:
					s3=""	
	
				try:
					s4="n. "
					for i in w2[w2.index("n.")+1:w2.index("vi.")]:
						s4=s4+" "+i
				except ValueError:
					s4=""

				try:
					s5="vi. "
					for i in w2[w2.index("vi.")+1:w2.index("vt.")]:
						s5=s5+" "+i
				except ValueError:
					s5=""
	
				try:
					s6="vt. "
					for i in w2[w2.index("vt.")+1:]:
						s6=s6+" "+i
				except ValueError:
					s6=""
			
				con_list=[s1,s2,s3,s4,s5,s6]
				con_list=[i for i in con_list if i!=""]   #去除列表空元素	
				self.conjugate[x]=con_list   #导入字典
			

	#从有道词典爬取词组
	def phr(self,fbxmind):
		if 6 in fbxmind:
			for x in list(self.fbdict.keys()):
				#获得页面
				url="http://dict.youdao.com/w/"+x+"/#keyfrom=dict2.top"
				response=urllib.request.urlopen(url)
				html=response.read()
				tree=etree.HTML(html.decode('utf-8'))
			
				#获取词组
				phrase1=tree.xpath("//*[@id='wordGroup']/p/span/a//text()")
				phrase2=tree.xpath("//*[@id='wordGroup']/p/text()")
			
				#处理文件形成字典，格式为{单词:[词组1 释义1,……],……}
				phrase3=[]
				for i in phrase2:
					i1=i.replace("\n","").replace(" ","").replace("\t","") #去掉空格，换行符等
					phrase3.append(i1)
					phrase3=[i for i in phrase3 if i!=""]  #去掉空的字符串
				phrase0=[]
				for m in range(len(phrase1)):
					phrase0.append(phrase1[m]+" "+phrase3[m])  #组合词组和词组释义
				phrase=phrase0[:3]
				self.phrase[x]=phrase   #导入字典
		
	#从有道词典爬取例句
	def sen(self,fbxmind):
		if 7 in fbxmind: 
			for x in list(self.fbdict.keys()):
				#获得页面
				url="http://dict.youdao.com/w/"+x+"/#keyfrom=dict2.top"
				response=urllib.request.urlopen(url)
				html=response.read()
				tree=etree.HTML(html.decode('utf-8'))
			
				#获得例句
				sentence1=tree.xpath("//*[@id='authority']/ul/li/p[1]/text()[1]")
				sentence3=tree.xpath("//*[@id='authority']/ul/li/p[1]/text()[2]")
				sentence5=tree.xpath("//*[@id='authority']/ul/li/p[2]/a/text()")
				sentence4=[]
				for m in sentence3:
					m1=m.replace("\n","").strip() #去掉前后的空格，换行符等
					sentence4.append(m1)
				sentence2=[]
				for y in sentence1:
					y1=y.replace("\n","").strip() #去掉前后的空格，换行符等
					sentence2.append(y1)
				sentence=[]
				for n in range(len(sentence1)):
					if sentence4[n]!="":
						sentence.append(sentence2[n]+" "+x+" "+sentence4[n]+"——"+sentence5[n])
					else:
						sentence.append(sentence2[n]+"——"+sentence5[n])
				self.sentence[x]=sentence   #导入字典
				
	#构建每日单词思维导图			
	def get_xmind(self,fbxmind):
		self.ant(fbxmind)
		self.syn(fbxmind)
		self.con(fbxmind)
		self.phr(fbxmind)
		self.sen(fbxmind)
		
		w=xmind.load("vocabulary.xmind")   #创建或打开已有XMind文件
		s=w.createSheet()   #创建画布
		s.setTitle(time.strftime("%Y.%m.%d") )  #设置画布名称

		r=s.getRootTopic()   #创建中心主题
		r.setTitle(time.strftime("%Y.%m.%d"))    #设置主题名称为当前日期

		for x in list(self.fbdict.keys()):
			sub=r.addSubTopic()  #创建单词分支
			sub.setTitle(x)
			
			if 1 in fbxmind:
				s1=sub.addSubTopic()   #创建第一个副主题
				s1.setTitle("单词释义")   #设置副主题名称为单词释义
				for i in range(len(self.vocabulary[x])):
					ss1=s1.addSubTopic()
					ss1.setTitle(self.vocabulary[x][i])   #将释义加到第一个副主题

			if self.synonym !={}:
				if len(self.synonym[x]) !=0:
					s2=sub.addSubTopic()
					s2.setTitle("同义词")   #创建第二个副主题“同义词”
					for i in range(len(self.synonym[x])):
						ss2 = s2.addSubTopic()
						ss2.setTitle(self.synonym[x][i])  # 将同义词加到第二个副主题

			if self.antonym !={}:
				if len(self.antonym[x]) !=0:
					s3=sub.addSubTopic()
					s3.setTitle("反义词")   #创建第三个副主题“反义词”
					for i in range(len(self.antonym[x])):
						ss3=s3.addSubTopic()
						ss3.setTitle(self.antonym[x][i])   #将反义词加到第三个副主题
            
			if self.conjugate !={}:
				if len(self.conjugate[x]) !=0:
					s4=sub.addSubTopic()
					s4.setTitle("同根词")   #创建第四个副主题“同根词”
					for i in range(len(self.conjugate[x])):
						ss4=s4.addSubTopic()
						ss4.setTitle(self.conjugate[x][i])    #将同根词加到第四个副主题
			
			if 5 in fbxmind:
				if x in self.messstatus.keys():
					if len(list(self.messstatus[x].keys())) !=0:
						s5=sub.addSubTopic()
						s5.setTitle("易混淆词")   #创建第五个副主题“易混淆词”
						for i in range(len(list(self.messstatus[x].keys()))):
							ss5 = s5.addSubTopic()
							ss5.setTitle(list(self.messstatus[x].keys())[i])

			if self.phrase !={}:
				if len(self.phrase[x]) !=0:
					s6=sub.addSubTopic()
					s6.setTitle("词组")   #创建第六个副主题“词组”
					for i in range(len(self.phrase[x])):
						ss6=s6.addSubTopic()
						ss6.setTitle(self.phrase[x][i])    #将词组加到第六个副主题
			
			if self.sentence !={}:
				if len(self.sentence[x]) !=0:
					s7=sub.addSubTopic()
					s7.setTitle("例句")   #创建第七个副主题“例句”
					for i in range(len(self.sentence[x])):
						ss7=s7.addSubTopic()
						ss7.setTitle(self.sentence[x][i])    #将例句加到第七个副主题
					
			
		xmind.save(w, "vocabulary.xmind")

	#构建每日单词excel			
	def get_excel(self,fbxmind):
		self.ant(fbxmind)
		self.syn(fbxmind)
		self.con(fbxmind)
		self.phr(fbxmind)
		self.sen(fbxmind)
		
		#打开工作簿
		wb=load_workbook("vocabulary.xlsx")
		ws=wb.active 
		ws.title=time.strftime("%Y.%m.%d") #命名工作表
		rows=[["单词"]]
		if 1 in fbxmind:  #根据用户需求内容生成excel第一行
			rows[0].append("释义")  
		if 2 in fbxmind:
			rows[0].append("同义词")
		if 3 in fbxmind:
			rows[0].append("反义词")
		if 4 in fbxmind:
			rows[0].append("同根词")
		if 6 in fbxmind:
			rows[0].append("词组")
		if 7 in fbxmind:
			rows[0].append("例句")
			 
		for x in list(self.fbdict.keys()):
			listx=[]
			listx.append(x)
			
			if 1 in fbxmind:
				if len(self.vocabulary[x]) !=0:
					tra="｜".join(self.vocabulary[x]) #得到各单词释义
				else:
					tra="None"
				listx.append(tra)
			
			if self.synonym !={}:
				if len(self.synonym[x]) !=0:
					syn="｜".join(self.synonym[x]) #得到各单词近义词
				else:
					syn="None"
				listx.append(syn)
			
			if self.antonym !={}:
				if len(self.antonym[x]) !=0:
					ant="｜".join(self.antonym[x]) #得到各单词反义词
				else:
					ant="None"
				listx.append(ant)
			
			if self.conjugate !={}:
				if len(self.conjugate[x]) !=0:
					con="｜".join(self.conjugate[x]) #得到各单词同根词
				else:
					con="None"
				listx.append(con)
			
			if self.phrase !={}:	
				if len(self.phrase[x]) !=0:
					phr="｜".join(self.phrase[x]) #得到各单词词组
				else:
					phr="None"
				listx.append(phr)
			
			if self.sentence !={}:	
				if len(self.sentence[x]) !=0:
					sen="｜".join(self.sentence[x]) #得到各单词例句
				else:
					sen="None"
				listx.append(sen)	
				
			rows.append(listx)
				
		for row in rows:
			ws.append(row)  #将各行放入工作表

		#保存Excel
		wb.save("vocabulary.xlsx")
