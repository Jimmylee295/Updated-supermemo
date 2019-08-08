#coding:UTF-8
import urllib.request
from lxml import etree
from functools import reduce

#获得释义（必应）
def get_trans(word):
	url_bing="http://cn.bing.com/dict/search?q="+word
	response_bing=urllib.request.urlopen(url_bing)
	html_bing=response_bing.read()
	tree_bing=etree.HTML(html_bing.decode('utf-8'))
	trans=[]
	trans1=tree_bing.xpath("/html/body/div[1]/div/div/div[1]/div[1]/ul/li")
	for item in trans1:
		it=item.xpath('span')
		trans.append('%s%s'%(it[0].text,it[1].xpath('span')[0].text))
	if len(trans)>0:
		return reduce(lambda x, y:"%s %s"%(x,y),trans)
	else:
		return "此单词拼写错误 此单词拼写错误"


#获得有道页面数据
def get_html(words):
	url="http://dict.youdao.com/w/"+word+"/#keyfrom=dict2.top"
	response=urllib.request.urlopen(url)
	html=response.read()
	tree=etree.HTML(html.decode('utf-8'))
	return tree

#获得词组
def get_phrase(tree):
	phrase1=tree.xpath("//*[@id='wordGroup']/p/span/a//text()")
	phrase2=tree.xpath("//*[@id='wordGroup']/p/text()")
	phrase3=[]
	for x in phrase2:
		x1=x.replace("\n","").replace(" ","").replace("\t","") #去掉空格，换行符等
		phrase3.append(x1)
		phrase3=[x for x in phrase3 if x!=""]  #去掉空的字符串
	phrase=[]
	for m in range(len(phrase1)):
		phrase.append(phrase1[m]+":"+phrase3[m])
	return phrase

#获得例句
def get_sentence(tree):
	sentence1=tree.xpath("//*[@id='authority']/ul/li/p[1]/text()[1]")
	sentence2=tree.xpath("//*[@id='authority']/ul/li/p[1]/b/text()")
	sentence3=tree.xpath("//*[@id='authority']/ul/li/p[1]/text()[2]")
	sentence5=tree.xpath("//*[@id='authority']/ul/li/p[2]/a/text()")
	sentence6=tree.xpath("//*[@id='authority']/ul/li/p[2]/a/i/text()")
	sentence4=[]
	for x in sentence3:
		x1=x.replace("\n","").strip() #去掉前后的空格，换行符等
		sentence4.append(x1)
	sentence=[]
	for n in range(len(sentence1)):
		sentence.append(sentence1[n]+sentence2[n]+sentence4[n]+"——"+sentence5[n]+sentence6[n])
	return sentence

#获得同根词
def con_dict(tree):
	con_dict={}
	try:
		w1=tree.xpath("//div[@id='relWordTab']//text()")  #利用xpath提取同根词部分文本
	except IndentationError:
		w1=[]
	#处理文件形成字典，格式为{单词:[词性1 同根词1 释义1,……],……}
	w2=[]
	for x in w1:
		x1=str(x).strip()   #去掉列表元素前后的空格和换行符
		w2.append(x1)
		w2=[x for x in w2 if x!=""]   #去除列表空元素

	#将列表元素分类
	try:
		for x in w2[w2.index("词根：")+1:w2.index("adj.")]:
			s1="词根："+x
	except ValueError:
		s1=""
		
	try:
		s2="adj. "
		for x in w2[w2.index("adj.")+1:w2.index("adv.")]:
			s2=s2+" "+x
	except ValueError:
		s2=""	

	try:
		s3="adv. "
		for x in w2[w2.index("adv.")+1:w2.index("n.")]:
			s3=s3+" "+x
	except ValueError:
		s3=""	
	
	try:
		s4="n. "
		for x in w2[w2.index("n.")+1:w2.index("vt.")]:
			s4=s4+" "+x
	except ValueError:
		s4=""

	try:
		s5="vi. "
		for x in w2[w2.index("vi.")+1:w2.index("vt.")]:
			s5=s5+" "+x
	except ValueError:
		s5=""
	
	try:
		s6="vt. "
		for x in w2[w2.index("vt.")+1:]:
			s6=s6+" "+x
	except ValueError:
		s6=""
			
	con_list=[s1,s2,s3,s4,s5,s6]
	con_list=[x for x in con_list if x!=""]   #去除列表空元素	
	con_dict[word]=con_list   #导入字典
	return con_dict

words=["name","financial","technology","university","game","dictionary",
	"error","effective","reservoir","essential","bright"]
for word in words:
	print(get_trans(word))
	#print(get_html(word))
	#print(get_phrase(get_html(word)))
	#print(get_sentence(get_html(word)))
	#print(con_dict(get_html(word)))
	
