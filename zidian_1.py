#coding:UTF-8
import urllib.request
from lxml import etree
import time
from functools import reduce
from tkinter.filedialog import askopenfilename
import json
#获得页面：构造一个函数，输入单词，通过urllib获得对应页面
def get_page(myword):
    basurl='http://cn.bing.com/dict/search?q='
    searchurl=basurl+myword
    response=urllib.request.urlopen(searchurl)  
    html=response.read()
    return html

#获得单词释义
def get_citiao(html_selector):
    citiao=[]
    hanyi_xpath='/html/body/div[1]/div/div/div[1]/div[1]/ul/li'
    get_hanyi=html_selector.xpath(hanyi_xpath)
    for item in get_hanyi:
        it=item.xpath('span')
        citiao.append('%s%s'%(it[0].text,it[1].xpath('span')[0].text))
    if len(citiao)>1: #排除只有网络释义的单词
        return reduce(lambda x, y:"%s %s"%(x,y),citiao)
    else:
        return "此单词拼写错误 此单词拼写错误"

#合并单词和释义
def get_word(word):
    #获得页面
    pagehtml=get_page(word)
    #单词释义
    selector=etree.HTML(pagehtml.decode('utf-8'))
    citiao=get_citiao(selector)
    citiao=citiao.split(" ")
    citiao=citiao[0:-1]  #去除网络释义
    return citiao

def openfile():
    filename = askopenfilename()
    if len(filename) != 0:
        f=open(filename,"rb")
        words=f.read().decode("utf-8")
        words=list(filter(None,words.split(" ")))
        dic={}
        for word in words:
            time.sleep(0.2) #生成速度
            shiyi=get_word(word.rstrip())
            if shiyi != ["此单词拼写错误"]:
                if len(shiyi) != 0:
                    zidian = {word:shiyi}
                    dic.update(zidian)

        print(dic)
        try:
            with open('vocabulary.json', 'r', encoding='utf-8') as json_file:
                vocabulary2 = json.loads(json_file.read())
                vocabulary = json.loads(vocabulary2)

            with open('status.json', 'r', encoding='utf-8') as json_file:
                status2 = json.loads(json_file.read())
                status = json.loads(status2)

            status_new = {}
            for word in list(dic.keys()):
                status_new[word] = ["2000-1-1",0,1,2.5]

            vocabulary.update(dic)
            status.update(status_new)
            json_vocabulary = json.dumps(vocabulary, sort_keys=False, ensure_ascii=False)
            with open('vocabulary.json', 'w', encoding='utf-8') as json_file:
                json.dump(json_vocabulary, json_file, ensure_ascii=False)
                
            json_status = json.dumps(status, sort_keys=False, ensure_ascii=False)
            with open('status.json', 'w', encoding='utf-8') as json_file:
                json.dump(json_status, json_file, ensure_ascii=False)
        except:
            print("单词本中空空如也")

            json_status = json.dumps(status, sort_keys=False, ensure_ascii=False)
            with open('status.json', 'w', encoding='utf-8') as json_file:
                json.dump(json_status, json_file, ensure_ascii=False)

        f.close()
    else:
        print("没有找到文件")

def add_word(words):
    dic = {}
    zidian = {}
    for word in words:
        time.sleep(0.2)  # 生成速度
        shiyi = get_word(word.rstrip())
        if len(shiyi) > 1:
            zidian = {word: shiyi}
        else:
            print("您输入的单词"+str(word)+"拼写错误")
        dic.update(zidian)

    return dic

