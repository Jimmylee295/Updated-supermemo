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
			print("���ʱ��пտ���Ҳ")

		with open('fbdict.json', 'r', encoding='utf-8') as json_file:
			fbdict = json.loads(json_file.read())
			self.fbdict = json.loads(fbdict)

		self.synonym = {}
		self.antonym = {}
		self.conjugate = {}
		self.phrase = {}
		self.sentence = {}
		

	def syn(self,fbxmind):    # �����
		if 2 in fbxmind:   # �����û������ж��Ƿ���ҪѰ�ҽ����
			for x in list(self.fbdict.keys()):
				syn_list = []
				for syn in wordnet.synsets(x):  # ��ôʼ�
					for lm in syn.lemmas():  # ��ô���
						syn_list.append(lm.name())  # ��ͬ�����ӵ��б�
				syn_list1 = []
				[syn_list1.append(i) for i in syn_list if not i in syn_list1]  # ȥ���б��ظ���
				for y in syn_list1:
					if y in list(self.fbdict.keys()):
						syn_list1.remove(y)  # ȥ���б��к�ԭ����ͬ�ĵ���
				syn_list1 = syn_list1[:3]  # ��ȡ�б��е�ǰ��������
				self.synonym[x] = syn_list1

		# �����
	def ant(self,fbxmind):
		if 3 in fbxmind:
			for x in list(self.fbdict.keys()):
				ant_list = []
				for syn in wordnet.synsets(x):  # ��ôʼ�
					for lm in syn.lemmas():  # ��ô���
						if lm.antonyms():
							ant_list.append(lm.antonyms()[0].name())  # ���������ӵ��б�
				ant_list1 = list(set(ant_list))  # ȥ���б��ظ���
				self.antonym[x] = ant_list1
            
	#���е��ʵ���ȡͬ����
	def con(self,fbxmind):
		if 4 in fbxmind:
			for x in list(self.fbdict.keys()):
				#���ҳ��
				url="http://dict.youdao.com/w/eng/"+x+"/#keyfrom=dict2.index"
				res=urllib.request.urlopen(url)
				page=res.read()
	
				#���ͬ����
				tree=etree.HTML(page) #ʹ��etree��html����
				dir(tree)
				try:
					w1=tree.xpath("//div[@id='relWordTab']//text()")  #����xpath��ȡͬ���ʲ����ı�
				except IndentationError:
					w1=[]
			
				#�����ļ��γ��ֵ䣬��ʽΪ{����:[����1 ͬ����1 ����1,����],����}
				w2=[]
				for i in w1:
					i1=str(i).strip()   #ȥ���б�Ԫ��ǰ��Ŀո�ͻ��з�
					w2.append(i1)
					w2=[i for i in w2 if i!=""]   #ȥ���б��Ԫ��
	
				#���б�Ԫ�ط���
				try:
					for i in w2[w2.index("�ʸ���")+1:w2.index("adj.")]:
						s1="�ʸ���"+i
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
				con_list=[i for i in con_list if i!=""]   #ȥ���б��Ԫ��	
				self.conjugate[x]=con_list   #�����ֵ�
			

	#���е��ʵ���ȡ����
	def phr(self,fbxmind):
		if 6 in fbxmind:
			for x in list(self.fbdict.keys()):
				#���ҳ��
				url="http://dict.youdao.com/w/"+x+"/#keyfrom=dict2.top"
				response=urllib.request.urlopen(url)
				html=response.read()
				tree=etree.HTML(html.decode('utf-8'))
			
				#��ȡ����
				phrase1=tree.xpath("//*[@id='wordGroup']/p/span/a//text()")
				phrase2=tree.xpath("//*[@id='wordGroup']/p/text()")
			
				#�����ļ��γ��ֵ䣬��ʽΪ{����:[����1 ����1,����],����}
				phrase3=[]
				for i in phrase2:
					i1=i.replace("\n","").replace(" ","").replace("\t","") #ȥ���ո񣬻��з���
					phrase3.append(i1)
					phrase3=[i for i in phrase3 if i!=""]  #ȥ���յ��ַ���
				phrase0=[]
				for m in range(len(phrase1)):
					phrase0.append(phrase1[m]+" "+phrase3[m])  #��ϴ���ʹ�������
				phrase=phrase0[:3]
				self.phrase[x]=phrase   #�����ֵ�
		
	#���е��ʵ���ȡ����
	def sen(self,fbxmind):
		if 7 in fbxmind: 
			for x in list(self.fbdict.keys()):
				#���ҳ��
				url="http://dict.youdao.com/w/"+x+"/#keyfrom=dict2.top"
				response=urllib.request.urlopen(url)
				html=response.read()
				tree=etree.HTML(html.decode('utf-8'))
			
				#�������
				sentence1=tree.xpath("//*[@id='authority']/ul/li/p[1]/text()[1]")
				sentence3=tree.xpath("//*[@id='authority']/ul/li/p[1]/text()[2]")
				sentence5=tree.xpath("//*[@id='authority']/ul/li/p[2]/a/text()")
				sentence4=[]
				for m in sentence3:
					m1=m.replace("\n","").strip() #ȥ��ǰ��Ŀո񣬻��з���
					sentence4.append(m1)
				sentence2=[]
				for y in sentence1:
					y1=y.replace("\n","").strip() #ȥ��ǰ��Ŀո񣬻��з���
					sentence2.append(y1)
				sentence=[]
				for n in range(len(sentence1)):
					if sentence4[n]!="":
						sentence.append(sentence2[n]+" "+x+" "+sentence4[n]+"����"+sentence5[n])
					else:
						sentence.append(sentence2[n]+"����"+sentence5[n])
				self.sentence[x]=sentence   #�����ֵ�
				
	#����ÿ�յ���˼ά��ͼ			
	def get_xmind(self,fbxmind):
		self.ant(fbxmind)
		self.syn(fbxmind)
		self.con(fbxmind)
		self.phr(fbxmind)
		self.sen(fbxmind)
		
		w=xmind.load("vocabulary.xmind")   #�����������XMind�ļ�
		s=w.createSheet()   #��������
		s.setTitle(time.strftime("%Y.%m.%d") )  #���û�������

		r=s.getRootTopic()   #������������
		r.setTitle(time.strftime("%Y.%m.%d"))    #������������Ϊ��ǰ����

		for x in list(self.fbdict.keys()):
			sub=r.addSubTopic()  #�������ʷ�֧
			sub.setTitle(x)
			
			if 1 in fbxmind:
				s1=sub.addSubTopic()   #������һ��������
				s1.setTitle("��������")   #���ø���������Ϊ��������
				for i in range(len(self.vocabulary[x])):
					ss1=s1.addSubTopic()
					ss1.setTitle(self.vocabulary[x][i])   #������ӵ���һ��������

			if self.synonym !={}:
				if len(self.synonym[x]) !=0:
					s2=sub.addSubTopic()
					s2.setTitle("ͬ���")   #�����ڶ��������⡰ͬ��ʡ�
					for i in range(len(self.synonym[x])):
						ss2 = s2.addSubTopic()
						ss2.setTitle(self.synonym[x][i])  # ��ͬ��ʼӵ��ڶ���������

			if self.antonym !={}:
				if len(self.antonym[x]) !=0:
					s3=sub.addSubTopic()
					s3.setTitle("�����")   #���������������⡰����ʡ�
					for i in range(len(self.antonym[x])):
						ss3=s3.addSubTopic()
						ss3.setTitle(self.antonym[x][i])   #������ʼӵ�������������
            
			if self.conjugate !={}:
				if len(self.conjugate[x]) !=0:
					s4=sub.addSubTopic()
					s4.setTitle("ͬ����")   #�������ĸ������⡰ͬ���ʡ�
					for i in range(len(self.conjugate[x])):
						ss4=s4.addSubTopic()
						ss4.setTitle(self.conjugate[x][i])    #��ͬ���ʼӵ����ĸ�������
			
			if 5 in fbxmind:
				if x in self.messstatus.keys():
					if len(list(self.messstatus[x].keys())) !=0:
						s5=sub.addSubTopic()
						s5.setTitle("�׻�����")   #��������������⡰�׻����ʡ�
						for i in range(len(list(self.messstatus[x].keys()))):
							ss5 = s5.addSubTopic()
							ss5.setTitle(list(self.messstatus[x].keys())[i])

			if self.phrase !={}:
				if len(self.phrase[x]) !=0:
					s6=sub.addSubTopic()
					s6.setTitle("����")   #���������������⡰���顱
					for i in range(len(self.phrase[x])):
						ss6=s6.addSubTopic()
						ss6.setTitle(self.phrase[x][i])    #������ӵ�������������
			
			if self.sentence !={}:
				if len(self.sentence[x]) !=0:
					s7=sub.addSubTopic()
					s7.setTitle("����")   #�������߸������⡰���䡱
					for i in range(len(self.sentence[x])):
						ss7=s7.addSubTopic()
						ss7.setTitle(self.sentence[x][i])    #������ӵ����߸�������
					
			
		xmind.save(w, "vocabulary.xmind")

	#����ÿ�յ���excel			
	def get_excel(self,fbxmind):
		self.ant(fbxmind)
		self.syn(fbxmind)
		self.con(fbxmind)
		self.phr(fbxmind)
		self.sen(fbxmind)
		
		#�򿪹�����
		wb=load_workbook("vocabulary.xlsx")
		ws=wb.active 
		ws.title=time.strftime("%Y.%m.%d") #����������
		rows=[["����"]]
		if 1 in fbxmind:  #�����û�������������excel��һ��
			rows[0].append("����")  
		if 2 in fbxmind:
			rows[0].append("ͬ���")
		if 3 in fbxmind:
			rows[0].append("�����")
		if 4 in fbxmind:
			rows[0].append("ͬ����")
		if 6 in fbxmind:
			rows[0].append("����")
		if 7 in fbxmind:
			rows[0].append("����")
			 
		for x in list(self.fbdict.keys()):
			listx=[]
			listx.append(x)
			
			if 1 in fbxmind:
				if len(self.vocabulary[x]) !=0:
					tra="��".join(self.vocabulary[x]) #�õ�����������
				else:
					tra="None"
				listx.append(tra)
			
			if self.synonym !={}:
				if len(self.synonym[x]) !=0:
					syn="��".join(self.synonym[x]) #�õ������ʽ����
				else:
					syn="None"
				listx.append(syn)
			
			if self.antonym !={}:
				if len(self.antonym[x]) !=0:
					ant="��".join(self.antonym[x]) #�õ������ʷ����
				else:
					ant="None"
				listx.append(ant)
			
			if self.conjugate !={}:
				if len(self.conjugate[x]) !=0:
					con="��".join(self.conjugate[x]) #�õ�������ͬ����
				else:
					con="None"
				listx.append(con)
			
			if self.phrase !={}:	
				if len(self.phrase[x]) !=0:
					phr="��".join(self.phrase[x]) #�õ������ʴ���
				else:
					phr="None"
				listx.append(phr)
			
			if self.sentence !={}:	
				if len(self.sentence[x]) !=0:
					sen="��".join(self.sentence[x]) #�õ�����������
				else:
					sen="None"
				listx.append(sen)	
				
			rows.append(listx)
				
		for row in rows:
			ws.append(row)  #�����з��빤����

		#����Excel
		wb.save("vocabulary.xlsx")
