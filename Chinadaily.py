import json
import random



def getlinks():
    with open('fbdict.json', 'r', encoding='utf-8') as json_file:
        fbdict2 = json.loads(json_file.read())
        fbdict = json.loads(fbdict2)

    wordlist = list(fbdict.keys())
    print(len(wordlist))

    with open('link.json', 'r', encoding='utf-8') as json_file:
        link2 = json.loads(json_file.read())
        link_ori = json.loads(link2)

    links = {}
    for word in list(link_ori.keys()): #生成了一个所有单词对应的文章列表构成的dictionary 得到链接中含有的单词
        for alink in link_ori[word]:
            if alink not in list(links.keys()):
                links[alink] = [word]
            else:
                links[alink].append(word)

    article = []
    for link in [a for a in list(links.keys()) if len(links[a]) > 1]: #超过一个单词的链接
        if set(links[link]).issubset(set(wordlist)): #如果这个link里面的单词都在今天的wordlist里
            article.append(link)
            print("a")
            for word in links[link]:
                wordlist.remove(word)

    for link in [a for a in list(links.keys()) if len(links[a]) > 1]:
        if len(set(links[link]) & set(wordlist)) >1:
            article.append(link)
            for word in list(set(links[link]) & set(wordlist)):
                wordlist.remove(word)

    for word in wordlist: #这些匹配剩下的单词只能用单篇文章填补
        try:
            random.shuffle(link_ori[word])
            article.append(link_ori[word][0])
        except:
            print("这个单词没有更新文章列表",word)

    articledic = {}
    for word in wordlist:
        if word in list(link_ori.keys()) and len(list(set(link_ori[word]) & set(article)))>0:
            articledic[word] = list(set(link_ori[word]) & set(article))[0] #今日链接列表和单词对应的链接列表，只有可能有一个元素
        else:
            articledic[word] = ""

    return article, articledic


