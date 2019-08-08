import math
import time
import numpy as np
import random
import json
from collections import defaultdict
from datetime import datetime,timedelta
import json
import zidian_1


class caculate():
    def __init__(self):
        #打开各种json文件
        with open('fbdict.json', 'r', encoding='utf-8') as json_file: #打开每次背单词之后记录单词记忆情况的feedbackdictionary
            fbdict = json.loads(json_file.read())
            self.fbdict = json.loads(fbdict)


        with open('messstatus.json', 'r', encoding='utf-8') as json_file:  #打开记录单词间混淆情况的messstatus.json
            messstatus = json.loads(json_file.read())
            self.messstatus = json.loads(messstatus)

        with open('status.json', 'r', encoding='utf-8') as json_file:   #打开记录各单词以往记忆情况，下次记忆时间的status.json
            status = json.loads(json_file.read())
            self.status = json.loads(status)

        try:    #打开单词本文件，避免为空
            with open('vocabulary.json', 'r', encoding='utf-8') as json_file:
                vocabulary = json.loads(json_file.read())
                self.vocabulary = json.loads(vocabulary)
        except:
            print("单词本中空空如也")

        #初始化变量
        self.times = 0
        self.lastinterval = 0
        self.EF = 0
        self.q_factor = 0
        self.nextdate = 0
        self.localtime = time.localtime(time.time())
        self.localdate = time.asctime(self.localtime)

    #定义函数获得某单词下一次背诵的时间
    def getnextdate(self, word, interval,status):
        nexttime = time.localtime(time.time() + interval * 86400)   #interval是天数
        nextdate = str(nexttime.tm_year) + "-" + str(nexttime.tm_mon) + "-" + str(nexttime.tm_mday)

        # 如果单词没有背错，就正常地记录下一次的时间。如果背错了，就强制今天再背一次
        if status ==0 :
            self.status[word][0] = nextdate
        elif status ==1:
            localtime = time.localtime(time.time())
            self.status[word][0] = str(localtime.tm_year) + "-" + str(localtime.tm_mon) + "-" + str(localtime.tm_mday)

        #无论是否背错，都要记录单词背过的总次数，和时间间隔。分析需要
        self.status[word][1] += 1
        self.status[word][2] = interval

    # 得到本次记忆与下次记忆的间隔时间
    def ginterval(self, times, EF, lastinterval):
        if times == 1:
            interval = 1
        elif times == 2:
            interval = 6
        else:
            interval = lastinterval * EF
            interval = int(round(interval))
        return interval

    # 更新参数 Easiness Factor （EF），此处尽可能还原原软件Super Memo原汁原味的算法
    def update(self, oldEF, q_factor):
        newEF = oldEF + (0.1 - (5 - q_factor) * (0.08 + (5 - q_factor) * 0.02))  # Easiness Factor 此处照搬原算法函数

        if newEF < 1.3:  # 避免报错
            EF = 1.3
        elif newEF > 2.5:
            EF = 2.5
        else:
            EF = newEF

        return EF

    # 计算分位数的函数
    def quantile_p(self, data, p):
        a = np.array(data)
        try:
            Q = np.percentile(a, p)
        except:
            Q = 0

        return Q

    #本函数对记忆过程中出错混淆的单词进行预处理
    def get_confusing_word(self):
        confusing = []
        # 对于选择的不是正确选项的单词，把这个fbdict里的meaning替换成单词
        for word in list(self.fbdict.keys()):
            if self.fbdict[word][0] != "True":
                self.fbdict[word] = list(self.fbdict[word])          #原本以tuple的形式记录，转为list，进行替换
                origin_word = [x for x, y in self.vocabulary.items() if self.fbdict[word][0] in list(y)]  #理论上同个释义可能有多个单词

                if len(origin_word) != 0:
                    del self.fbdict[word][0]     #将混淆单词的释义替换为单词
                    self.fbdict[word].insert(0,origin_word[0])
                else:
                    pass

                self.fbdict[word] = tuple(self.fbdict[word]) #转换回tuple

    #主要的计算函数，根据每个单词记忆情况更新下一次的时间，更新单词间的混淆关系
    def cnt(self):  # 计算各单词下次复习时间，更新单词状态
        timelist1 = []  # 正确单词的时间list
        timelist2 = []  # 错误单词的时间list
        for word in list(self.fbdict.keys()):  # 得到所有单词记忆的时间，用于后续分析
            if self.fbdict[word][0] == "True":
                timelist1.append(self.fbdict[word][1])
            else:
                timelist2.append(self.fbdict[word][1])

        # 计算正确单词记忆平均时间
        nsum = 0
        for i in range(len(timelist1)):
            nsum += timelist1[i]
        try:
            ave_time = nsum / len(timelist1)
        except:
            ave_time = 0

        #对记忆正确的单词，高于平均和低于平均进行分组，用于分析
        list_above_ave = []
        list_below_ave = []
        for time in timelist1:
            if time >= ave_time:
                list_above_ave.append(time)
            if time < ave_time:
                list_below_ave.append(time)

        Q1 = self.quantile_p(list_below_ave, 50)  # 小于平均记忆时间的 时间 的 中位数
        Q2 = self.quantile_p(timelist2, 50)
        Q3 = self.quantile_p(timelist2, 75)

        # requirement and descriptions in Super memo 2                                  #in our App
        # q_factor should be 0-5:
        # 5 - perfect response                                                          # 5 - 记忆正确，且时间短于低于平均数一组的中位数以下
        # 4 - correct response after a hesitationw                                      # 4 - 记忆正确，时间介于低于平均数一组中位数以上
        # 3 - correct response recalled with serious difficulty                         # 3 - 记忆正确，时间高于正确组平均数
        # 2 - incorrect response; where the correct one seemed easy to recall           # 2 - 回答错误，时间高于66分位数
        # 1 - incorrect response; the correct one remembered                            # 1 - 回答错误，时间在33.3-66.6分位之间
        # 0 - complete blackout.                                                        # 0 - 回答错误，时间低于33.3分位

        # q_factor 更新
        for word in list(self.fbdict.keys()):
            if word in self.status:
                pass
            else:
                self.status[word] = ["", 0, 1, 2.5]  # 初始化水平

            #读取文件记录的上一次的总背诵次数，旧的EF数据，旧的时间间隔，用于分析
            times = self.status[word][1]
            oldEF = self.status[word][3]
            lastinterval = self.status[word][2]

            # 打分 更新q_factor
            if self.fbdict[word][0] == "True":
                if self.fbdict[word][1] <= ave_time:  # 相当于SM算法中q_factor的4/5分，根据反应时间来分配这两个评分
                    if self.fbdict[word][1] <= Q1:
                        self.q_factor = 5
                    else:
                        self.q_factor = 4
                if self.fbdict[word][1] > ave_time:
                    self.q_factor = 3

                status = 0

            else:  # 更新易混词，并计算错误时的q_factor 0,1,2
                self.get_confusing_word()  # 替换成单词
                word_f = self.fbdict[word][0]

                # 统一小数位数
                word_t_str = str(self.fbdict[word][1])
                a, b, c = word_t_str.partition(".")
                word_t = float(".".join([a, c[:2]]))

                # 更新混淆单词，将用户在背单词的时候出现的错误记录下来，混淆“程度”是以时间倒数来评价。时间越短，越“不假思索”，混淆越严重
                if word in self.messstatus:
                    if word_f in self.messstatus[word]:
                        self.messstatus[word][word_f] += round(math.log(1 + 1 / word_t),2)
                    else:
                        self.messstatus[word][word_f] = round(math.log(1 + 1 / word_t),2)
                else:
                    self.messstatus[word] = {}
                    self.messstatus[word][word_f] = round(math.log(1 + 1 / word_t),2)

                sorted(self.messstatus[word],reverse=True) #把单词按照混乱程度划分 方便后面根据这个排序

                # 更新q_factor，如果记忆错误，分配0\1\2三个评分
                if self.fbdict[word][1] > Q2:
                    self.q_factor = 0
                elif self.fbdict[word][1] < Q2 and self.fbdict[word][1] > Q3:
                    self.q_factor = 2
                elif self.fbdict[word][1] < Q3:
                    self.q_factor = 1

                #如果单词出现错误，强行从头再来，今天重复记忆
                lastinterval = 1
                status = 1


            # 更新status dictionary，把该单词下次的记忆时间写入
            EF = self.update(oldEF, self.q_factor)
            self.status[word][3] = EF #更新EF
            if lastinterval != 1: #当单词记忆错误的时候，要重新开始记忆
                interval = self.ginterval(times, EF, lastinterval)
            else:
                interval = self.ginterval(times, 1, lastinterval)
            self.getnextdate(word, interval,status)

        #调用函数将所有更改储存下来
        self.store()

    #将背单词途中手动输入的，联想到的单词记录下来。如果没有手动添加易混单词的话，这个函数不会被使用
    def add_new_word(self,fbdict2):

        for word, word_list in list(fbdict2.items()):
            try:     #将单词对应的 手动输入混淆单词列表导入函数 得到一个对应的dictionary
                meaningdict = zidian_1.add_word(word_list) #得到新添加的单词及其对应的含义{word:[meaning]} #这个字典里只会有找到释义的单词
            except:
                print("出现未知错误")
                pass
            else:
                for word2 in list(meaningdict.keys()):
                #将手动输入的混淆单词添加到单词本中
                    if word2 in self.vocabulary.keys():
                        pass
                    else:
                        self.vocabulary.update({word2: meaningdict[word2]})

                #将手动输入的混淆单词加入单词的混淆单词字典中
                    if word in self.messstatus:              #如果之前记忆错误过
                        if word2 in self.messstatus[word]:   #如果之前就错过这个单词
                            self.messstatus[word][word2] = 100
                        else:
                            self.messstatus[word][word2] = 100 #任意设定时间，确保这个单词能排在最前面，在复习完单词后优先复习这个单词
                    else:
                        self.messstatus[word] = {word2:100}
        self.store()

    #储存函数
    def store(self):
        json_fbdict = json.dumps(self.fbdict, sort_keys=False, ensure_ascii= False)
        json_messstatus = json.dumps(self.messstatus,sort_keys=False, ensure_ascii= False)
        json_status = json.dumps(self.status,sort_keys=False, ensure_ascii= False)
        json_vocabulary = json.dumps(self.vocabulary, sort_keys=False, ensure_ascii=False)

        with open('fbdict.json', 'w', encoding='utf-8') as json_file:
            json.dump(json_fbdict, json_file, ensure_ascii=  False)

        with open('messstatus.json', 'w', encoding='utf-8') as json_file:
            json.dump(json_messstatus, json_file, ensure_ascii=False)

        with open('status.json', 'w', encoding='utf-8') as json_file:
            json.dump(json_status, json_file, ensure_ascii=False)

        with open('vocabulary.json', 'w', encoding='utf-8') as json_file:
            json.dump(json_vocabulary, json_file, ensure_ascii=False)


#根据ui反馈的localtime 得到今次复习的单词list, 并调整单词顺序，分配单词释义
class randomize():
    def __init__(self):

        self.today_word_list = []

        #打开各种json文件
        with open('messstatus.json', 'r', encoding='utf-8') as json_file:
            messstatus = json.loads(json_file.read())
            self.messstatus = json.loads(messstatus)

        with open('status.json', 'r', encoding='utf-8') as json_file:
            status = json.loads(json_file.read())
            self.status = json.loads(status)

        try:
            with open('vocabulary.json', 'r', encoding='utf-8') as json_file:
                vocabulary = json.loads(json_file.read())
                self.vocabulary = json.loads(vocabulary)
        except:
                print("单词本中空空如也")

    #调用函数获得今天
    def get_today_word_list(self):

        localtime = time.localtime(time.time())
        localdate = str(localtime.tm_year) + "-" + str(localtime.tm_mon) + "-" + str(localtime.tm_mday)
        lyear = localtime.tm_year
        lmon = localtime.tm_mon
        lday = localtime.tm_mday
        new_word = 1

        #每一个单词都会有对应的status.json文件
        for word in list(self.status.keys()):
            try:
                a,b,c = self.status[word][0].split("-")
            except: #避免可能出现的时间缺失情况，虽然机率小，但毕竟存在时间为空的情况。
                a,b,c = [9999,9999,9999]

            #判断今天是否需要记忆
            if int(a) != 2000:
                if lyear >= int(a) and lmon >= int(b) and lday >= int(c):
                    self.today_word_list.append(word)
                else:
                    pass
            #在两种导入方式中，新导入的的单词都会初始化成2000-1-1，每天可以设置新单词的数量。
            elif int(a) == 2000 and new_word <= 5: #测试用，后面要改成20
                self.today_word_list.append(word)
                new_word += 1

        #将每天生成的单词都打乱
        random.shuffle(self.today_word_list)

    # 本函数目的在于将单词排序,并将混淆词汇放在一起
    def sort(self):
        for word in self.today_word_list:
            if word in list(self.messstatus.keys()): #判断是否有混淆单词
                messlist = list(self.messstatus[word].keys()) #得到混淆单词列表。

                for word2 in messlist:
                    if word2 in self.today_word_list: #判断混淆单词在不在今天要背的单词列表里
                        self.today_word_list.remove(word2)
                        self.today_word_list.insert( self.today_word_list.index(word) + 1 , word2) #插入到混淆单词的后边
                    else:
                        pass

    def get_meaning(self):
        self.get_today_word_list()
        self.sort()
        today_word_dict = {}
        meaninglist = []
        list1 = list(self.vocabulary.keys())

        for word in self.today_word_list:
            meaninglist = []
            #随机生成四个meanings,并去除要背的单词本身的释义
            list2 = [x for x in list1 if x!=word]

            random.shuffle(list2) #随机得到单词及其释义
            m1, m2, m3, m4 = self.vocabulary[list2[0]][0], \
                             self.vocabulary[list2[1]][0], \
                             self.vocabulary[list2[2]][0], \
                             self.vocabulary[list2[3]][0]

            meaninglist.insert(0,self.vocabulary[word][0]) #插入真实释义

            #补充迷惑释义
            if word in self.messstatus: #存在迷惑单词
                messlist = list(self.messstatus[word].keys())
                meaninglist.insert(1,self.vocabulary[messlist[0]][0]) #插入第一个迷惑释义
                meaninglist.insert(2, m3)
                meaninglist.insert(3, m2)
                if len(messlist) == 2:
                    meaninglist.insert(2,self.vocabulary[messlist[1]][0])
                    meaninglist.insert(3,m2)
                elif len(messlist) >= 3:
                    meaninglist.insert(2, self.vocabulary[messlist[1]][0])
                    meaninglist.insert(3,self.vocabulary[messlist[2]][0])
                today_word_dict[word] = tuple(meaninglist)

            else:
                meaninglist.insert(1,m1)
                meaninglist.insert(2,m2)
                meaninglist.insert(3,m3)
                today_word_dict[word] = tuple(meaninglist)

        return today_word_dict


