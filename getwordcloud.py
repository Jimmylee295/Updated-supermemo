#coding=GBK
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json

def getwordcloud():
	#打开每次背诵单词情况文件，提取其中单词
	with open('fbdict.json', 'r', encoding='utf-8') as json_file:
		fbdict = json.loads(json_file.read())
		fbdict = json.loads(fbdict)
		word=list(fbdict.keys())

	with open("status.json","r", encoding='utf-8') as json_file:
		status2 = json.loads(json_file.read())
		status = json.loads(status2)

	#将每次背诵单词写入新文件，用于统计词频
	with open("1.txt","w") as f:
		for word in list(status.keys()):
			if status[word][1] > 0:
				for num in range(status[word][1]):
					f.write(word+"\n")

	#根据新文件中单词词频生成词云
	with open("1.txt","r") as f:
		text=f.read()
	wordcloud = WordCloud(background_color='white',scale=1.5).generate(text)
	#image_colors = ImageColorGenerator(bg_pic)
	#显示词云图片
	plt.imshow(wordcloud)
	plt.axis('off')
	plt.show()


