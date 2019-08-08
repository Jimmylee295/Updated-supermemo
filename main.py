from tkinter import *
import tkinter as tk
import datetime
import time
import sys
import random
import backstage
import json
from add import importdict
import zidian_1
import mindmap
from tkinter import messagebox
import Chinadaily
import updatelinks
import getwordcloud
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from tkinter.filedialog import askopenfilename, asksaveasfilename

class App: #封装程序
    def __init__(self, master,dic=dict): #创建master画布，统一master为主窗口，Toplevel是子窗口

        #构建画布
        self.frame3 = Frame(master)
        self.frame3.pack(side=TOP, expand=YES, fill="x")
        self.frame1 = Frame(master)
        self.frame1.pack(side = TOP, expand = YES, fill = "x")
        self.frame4 = Frame(master)
        self.frame4.pack(side = TOP, expand = YES, fill = "x")
        self.frame2 = Frame(master)
        self.frame2.pack(side = TOP, expand = YES, fill = "x")
        self.frame4L = Frame(self.frame4)
        self.frame4L.pack(side=LEFT, expand=YES, fill="x")
        self.frame4R = Frame(self.frame4)
        self.frame4R.pack(side=RIGHT, expand=YES, fill="x")

        #变量定义/初始化
        self.text0 = StringVar()#定义变量
        self.text1 = StringVar()
        self.text2 = StringVar()
        self.text3 = StringVar()
        self.text4 = StringVar()
        self.text5 = StringVar()
        self.text10 = StringVar()
        self.v = StringVar()

        #初始化显示内容
        self.text0.set('点击任意按钮开始')
        self.text1.set('')
        self.text2.set('')
        self.text3.set('')
        self.text4.set('')
        self.text5.set("")
        self.text10.set("")

        # 定义变量
        self.a = -1
        self.word = ""
        self.meaning1 = ""
        self.meaning2 = ""
        self.meaning3 = ""
        self.meaning4 = ""
        self.truemeaning = "" #定义变量
        self.promt = ""
        self.val = ""
        self.fbdict = {}
        self.color = ["Green","Red"]
        self.time_start = 0
        self.time_end = 0
        self.time = 0
        self.fbdict2 = {}
        self.num = 0
        self.truenum = 0
        self.wrongnum = 0
        self.z = 0
        self.fbxmind = []
        self.articledic = {}

        #得到今天要背的单词，如果今天没有需要记忆的单词，就将所有内容禁用，关闭软件即可
        dic = backstage.randomize()                                      #调用函数得到今天的随机单词字典
        if len(dic.get_meaning()) != 0:                              #如果长度不为零，即初始化背诵界面
            self.dic = dic.get_meaning()
            self.num = len(list(self.dic.keys()))
        else:
            self.dic = {"本次没有要背的单词":("","","","")}         #长度为零，即今天没有要背的单词，就更改初始界面的显示
            self.text0.set('本次没有要背的单词\n右上角关闭程序即可')
        ######################################

        self.createwidgets()      #引用函数，生成部件
        self.setupfeedbackdict()    #生成记录记忆情况的各个list/dictionary


    def createwidgets(self):

        #菜单条
        self.casbutton = Menubutton(self.frame3, text = "选项", font = ("Times New Roman",10),underline = 0)
        self.casbutton.pack(side = LEFT)

        self.casbutton2 = Menubutton(self.frame3, text = "复习", font = ("Times New Roman",10),underline = 0)
        self.casbutton2.pack(side = LEFT)
        self.casbutton2.menu = Menu(self.casbutton2)
        self.casbutton2.menu.choice = Menu(self.casbutton2.menu)
        self.casbutton2.menu.add_cascade(label = "获取文章",menu = self.casbutton2.menu.choice)
        self.casbutton2.menu.choice.add_command(label="从China Daily", command=lambda: self.create())
        self.casbutton2.menu.choice.add_command(label="更新文章列表", command=lambda: self.updatelinks())

        self.label = Label(self.frame3, textvariable = self.text10, font = ("Times New Roman",15))
        self.label.pack(side = RIGHT)

        self.casbutton.menu = Menu(self.casbutton)
        self.casbutton.menu.choice = Menu(self.casbutton.menu)
        self.casbutton.menu.more = Menu(self.casbutton.menu)

        self.casbutton.menu.choice.add_command(label = "从互联网",command = lambda: self.addtxt())
        self.casbutton.menu.choice.add_command(label="从本地",command = lambda: self.add())

        self.casbutton.menu.more.add_command(label="生成思维导图",command = lambda: self.create2(1))
        self.casbutton.menu.more.add_command(label="生成词云", command=lambda: self.getwordcloud())
        self.casbutton.menu.more.add_command(label="生成excel表", command=lambda: self.create2(2))

        self.casbutton.menu.add_cascade(label = "添加",menu = self.casbutton.menu.choice)
        self.casbutton.menu.add_cascade(label="更多",menu = self.casbutton.menu.more)

        self.casbutton['menu'] = self.casbutton.menu
        self.casbutton2['menu'] = self.casbutton2.menu
        #单词显示窗口
        self.label = Label(self.frame1, textvariable = self.text0, font = ("Times New Roman",20), width = 25, height = 13)
        self.label.pack(side = TOP)

        #生成各个按钮
        self.buttonnext = Button(self.frame4L, text = "next",width = 20, height = 2, command = lambda: self.next())
        self.buttonnext.pack(side = TOP)

        self.entry = Entry(self.frame4R, width = 40, borderwidth = 3, textvariable= self.v)
        self.entry.pack(side = TOP)

        self.button1 = Button(self.frame2, textvariable = self.text1, width = 65, height = 2, command = lambda : self.change(self.meaning1))
        self.button1.pack(side = TOP)                   #在“frame”上显示, 文字是单词释义，选中之后又把单词释义返回到函数中，记录下来

        self.button2 = Button(self.frame2, textvariable = self.text2, width = 65, height = 2, command = lambda :self.change(self.meaning2))
        self.button2.pack(side = TOP)

        self.button3 = Button(self.frame2, textvariable = self.text3, width = 65, height = 2, command = lambda: self.change(self.meaning3))
        self.button3.pack(side = TOP)

        self.button4 = Button(self.frame2, textvariable = self.text4, width = 65, height = 2, command = lambda: self.change(self.meaning4))
        self.button4.pack(side = TOP)

        #定义按钮状态
        self.buttonnext["state"] = "disabled"
        self.entry["state"] = "disabled"

        if self.dic == {"本次没有要背的单词":("","","","")}:   #如果今天没有要背的单词，就禁用所有的函数和按钮
            self.button1["state"] = "disabled"
            self.button2["state"] = "disabled"
            self.button3["state"] = "disabled"
            self.button4["state"] = "disabled"
            self.buttonnext["state"] = "disabled"
            self.entry["state"] = "disabled"

    #按下四个有单词含义的按钮后，触发change函数
    def change(self, choice):
        self.time_end = time.time()                                                   #作出选择后停止计时

        # 初始化，出现第一个单词
        if self.a == -1:
            self.time_start = time.time()                                             #开始计时（只有第一个单词需要）
            item = list(self.dic.items())                                             #导出下一个单词的单词+释义(tuple)
            word_meaning = item[0]
            self.word = word_meaning[0]                                               #下一个单词
            self.truemeaning = word_meaning[1][0]                                     #储存单词的正确含义，并在后面判断对错中使用
                                                                                      #这个在后台生成四个选项的时候就默认第一个释义是正确的，这里是在打乱顺序

            # 打乱释义的顺序
            randomnum = list(range(4))
            random.shuffle(randomnum)
            num1, num2, num3, num4 = randomnum[0],randomnum[1],randomnum[2],randomnum[3]

            # 生成下一个单词的随机释义
            self.meaning1 = word_meaning[1][num1]
            self.meaning2 = word_meaning[1][num2]
            self.meaning3 = word_meaning[1][num3]
            self.meaning4 = word_meaning[1][num4]

            #点击后更新单词和释义
            self.text0.set(self.word)
            self.text1.set(self.meaning1)
            self.text2.set(self.meaning2)
            self.text3.set(self.meaning3)
            self.text4.set(self.meaning4)

            self.text10.set("1" + "/" + str(self.num))

        #除了一头一尾的单词，都是按照这个运行
        if self.a <= len(self.dic)-1 and self.a != -1:
            self.time_end = time.time()                                                 #停止计时

            #记录本单词作出反应所需的时间
            print("%.2f" % (self.time_end - self.time_start))
            time_cost = str(self.time_end - self.time_start)                            # 返回小数两位，为简便，四舍五不入
            a, b, c = time_cost.partition(".")
            self.time = float(".".join([a, c[:2]]))                                     #统一记录时间的格式

            #更新反馈给后台的数据fbdict 并更改显示窗口的颜色，显示正确的释义
            if choice == self.truemeaning:                                              #如果答案正确，则用绿色显示
                self.fbdict[self.word] = ["True", self.time]
                self.text0.set("True")
                self.label["fg"] = "green"
                self.truenum +=1
            else:                                                                       #答案错误，则显示正确答案，红色显示
                self.fbdict[self.word] = [choice, self.time]
                self.text0.set("False!\n The true meaning of\n " + str(self.word) + " \nshould be\n" + str(self.truemeaning))
                self.label["fg"] = self.color[1]
                self.wrongnum +=1

            #将按钮禁用，避免误触。这个时候可以慢慢背这个单词
            self.text1.set("")
            self.text2.set("")
            self.text3.set("")
            self.text4.set("")
            self.button1["state"] = "disabled"
            self.button2["state"] = "disabled"
            self.button3["state"] = "disabled"
            self.button4["state"] = "disabled"
            self.buttonnext["state"] = "normal"
            self.entry["state"] = "normal"

        #更新状态变量a
        self.a = self.a +1

    def next(self):
        self.time_start = time.time()                                                   #按下next会出现下一个单词，开始计时。
        self.label["fg"] = "black"
        self.text10.set(str(self.a+1)+"/"+str(self.num))                                #更新“剩余单词”的显示

        #获取用户手动输入（如有）的单词
        confusedword = self.v.get()
        if len(confusedword) != 0:
            self.fbdict2[self.word]= [str(a.strip()) for a in confusedword.split(" ")]               #生成文件记录下来，交由后台查找释义

        self.v.set("")                                                                                #清空显示

        #显示下一组单词及释义
        if self.a < len(self.dic):          #防止over indexed
            item = list(self.dic.items())   #导出下一个单词的单词+释义(tuple)
            word_meaning = item[self.a]
            self.word = word_meaning[0]     #下一个单词
            self.truemeaning = word_meaning[1][0]   #默认第一个是正确答案

            randomnum = list(range(4)) #打乱顺序
            random.shuffle(randomnum)
            num1, num2, num3, num4 = randomnum[0],randomnum[1],randomnum[2],randomnum[3]
            self.meaning1 = word_meaning[1][num1] #下一个单词的释义
            self.meaning2 = word_meaning[1][num2]
            self.meaning3 = word_meaning[1][num3]
            self.meaning4 = word_meaning[1][num4]

            self.text0.set(self.word) #点击后，更新单词
            self.text1.set(self.meaning1) #点击后，更新释义
            self.text2.set(self.meaning2)
            self.text3.set(self.meaning3)
            self.text4.set(self.meaning4)
            self.text5.set(self.promt)

            #更新按钮和输入框的状态，使得next按钮，输入框都禁用
            self.button1["state"] = "normal"
            self.button2["state"] = "normal"
            self.button3["state"] = "normal"
            self.button4["state"] = "normal"
            self.buttonnext["state"] = "disabled"
            self.entry["state"] = "disabled"

        # 当单词背诵完毕后，更新显示内容
        if self.a == len(self.dic):
            self.text0.set("本次单词记忆结束,软件正在记录") #当单词背诵完毕后，更新显示

            self.text5.set("")
            self.text10.set("")
            self.button1.destroy() #删除所有的按钮，输入框
            self.button2.destroy()
            self.button3.destroy()
            self.button4.destroy()
            self.entry.destroy()
            self.buttonnext.destroy()
            self.text0.set("本次单词记忆结束")

            self.end()                      #调用end函数，作好储存、运算工作。


    def end(self):
        #储存手动输入的混淆词汇
        if len(self.fbdict2) !=0:
            print(self.fbdict2)
            c = backstage.caculate()
            try:
                c.add_new_word(self.fbdict2)  # 将手动输入的混淆单词查找含义，写入字典，更新fbdict
            except:
                print("出现网络错误")         #存在一定几率无法连接
                pass

        # 对feedbackdictionary(fbdict)进行初步的处理，写入json文件，引用后台函数记录/计算
        del self.fbdict["localtime"]
        if "本次没有要背的单词" in self.fbdict:
            del self.fbdict["本次没有要背的单词"]
        if len(self.fbdict) != 0:
            json_fbdict = json.dumps(self.fbdict, sort_keys=False, ensure_ascii=False)
            with open('fbdict.json', 'w', encoding='utf-8') as json_file:               #覆盖写入软件
                json.dump(json_fbdict, json_file, ensure_ascii=False)

            c = backstage.caculate() #引用后台函数 更新messstatus等json文件
            c.cnt()
            self.end = 1            #更新状态变量，方便开启部分功能（下拉菜单没有状态可选，只能用此下策）

    #引用add函数，添加本地单词
    def add(self):
        try:
            a = importdict()
            a.add()
        except:
            messagebox.showinfo('提示', '发生错误')

    #引用mindmap函数生成思维导图
    def mindmap(self):
        if self.end == 1:
            c = mindmap.mindmap()
            c.get_xmind(self.fbxmind)
            messagebox.showinfo('提示', '已生成思维导图')
        else:
            messagebox.showinfo('提示', '今天的单词未完成记忆')
            pass

    #引用addtxt函数，打开txt文档，网络查询释义并储存
    def addtxt(self):
        try:
            zidian_1.openfile()
        except:
            messagebox.showinfo('提示', '网络错误')

    #得到本地时间，共各种分析使用
    def getlocaltime(self):
        local_time = time.localtime(time.time())

        return time.asctime(local_time) #得到标准化的时间

    #建立反馈字典 feedback dictionary (fbdict)
    def setupfeedbackdict(self):
        local_time = self.getlocaltime()
        self.fbdict["localtime"] = local_time

    #计时模块，计算单词实际反应时间
    def timemodule(self):
        self.time_end = time.time()
        if self.a != -1:
            print("%.2f" %(self.time_end -self.time_start))
            time_cost = str(self.time_end - self.time_start) #返回小数两位，为简便，四舍五不入
            a,b,c = time_cost.partition(".")
            return float(".".join([a,c[:2]]))

    #定义关闭窗口事件
    def on_closing(self):
        #如果单词没有背完，记录记忆情况（调用end（）），并弹出窗口
        if self.end != 1:
            if messagebox.askokcancel("Quit", "今日单词没有背完，确认要关闭？"):
                self.end() #如果单词还没有被完，先调用end函数记录好
                root.destroy()

        # 如果今天已经背完 显示今天的记忆情况
        else:
            if messagebox.askokcancel("Quit", "确认要关闭？"):
                if messagebox.askokcancel("quit","今日单词记忆个数："+str(self.num)+
                        "\n"+"错误个数："+str(self.wrongnum)+
                        "\n"+"正确个数："+str(self.truenum)+
                        "\n"+"正确率："+str((round(self.truenum/self.num,2))*100)+"%"):
                    root.destroy()

    #生成词云
    def getwordcloud(self):
        getwordcloud.getwordcloud()

    #生成单词excel，储存爬取的同义词，近义词和例句
    def getexcel(self):
        try:
            a = mindmap.mindmap()
            a.get_excel(self.fbxmind)
        except FileNotFoundError:
            messagebox.showinfo('提示', 'vocabulary.xlsx缺失，应在本地创建空白文档')

    #弹出窗口，更新单词列表
    def updatelinks(self):
        if messagebox.askokcancel("继续", "耗时较长，确定继续？"):
            try:
                a = updatelinks.getlinks()
                a.setuplinks()
            except:
                pass
                messagebox.showinfo('提示', '更新列表操作已停止')

    #子窗口 生成文章目录
    def create(self):
        if self.end ==1:
            top = Toplevel()
            top.title('China daily')
            top.geometry("300x400")
            frame1 = Frame(top)
            frame1.pack(side=TOP, expand=YES, fill="x")
            frame2 = Frame(top)
            frame2.pack(side = TOP, expand = YES, fill = "x")
            frame3 = Frame(top)
            frame3.pack(side = TOP, expand = YES, fill = "x")
            links, self.articledic = Chinadaily.getlinks()
            button1 = Button(frame2, text = "随机打开下一个", width = 30, height = 2, command = lambda: self.openlink(links))
            button1.pack(side = TOP)

            theLB = Listbox(frame1, selectmode=SINGLE, height=11)  # height=11设置listbox组件的高度，默认是10行。
            theLB.pack()
            button1 = Button(frame3, text = "打开复习文章", width = 30, height = 2, command = lambda: self.Call_Entry(theLB))
            button1.pack(side = TOP)
            print(self.val)
            sb = Scrollbar(root)  # 垂直滚动条组件
            sb.pack(side=RIGHT, fill=Y)
            sb.config(command=theLB.yview)
            for item in list(self.articledic.keys()):
                theLB.insert(END, item)  # END表示每插入一个都是在最后一个位置
        else:
            messagebox.showinfo('提示', '今天的单词没背完')

    #具体的，打开链接的函数。弹出Chrome
    def openlink(self,links):
        if len(links) > 0:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--start-maximized')
            driver = webdriver.Chrome()
            driver.maximize_window()
            driver.get(links[self.z])
        else:
            pass
            messagebox.showinfo('提示', '今天的单词还未生成链接')

        self.z = self.z +1

    #生成小窗口，可以选择单词对应的链接。
    def Call_Entry(self,theLB):
        self.val=theLB.get(theLB.curselection())
        link = self.articledic[self.val]
        if len(link) > 0:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--start-maximized')
            driver = webdriver.Chrome()
            driver.maximize_window()
            driver.get(link)
        else:
            pass
            messagebox.showinfo('提示', '此单词还未生成链接')

    #生成子窗口-选择选择思维导图、excel表内容
    def create2(self,num):
        top = Toplevel()
        top.title('Mindmap')
        top.geometry("300x270")

        #1-释义 2-同义词 3-反义词 4-同根词 5-易混淆 6-词组 7-例句
        #生成多选框
        self.CheckVar1 = IntVar()
        self.CheckVar2 = IntVar()
        self.CheckVar3 = IntVar()
        self.CheckVar4 = IntVar()
        self.CheckVar5 = IntVar()
        self.CheckVar6 = IntVar()
        self.CheckVar7 = IntVar()
        #生成各个按钮
        C1 = Checkbutton(top, text="释义", variable=self.CheckVar1, onvalue=1, offvalue=0, height=1,width=20)
        C1.pack(side = TOP)
        C2 = Checkbutton(top, text="同义词", variable=self.CheckVar2, onvalue=2, offvalue=0, height=1,width=20)
        C2.pack(side=TOP)
        C3 = Checkbutton(top, text="反义词", variable=self.CheckVar3, onvalue=3, offvalue=0, height=1, width=20)
        C3.pack(side=TOP)
        C4 = Checkbutton(top, text="同根词", variable=self.CheckVar4, onvalue=4, offvalue=0, height=1, width=20)
        C4.pack(side=TOP)
        C5 = Checkbutton(top, text="易混淆词", variable=self.CheckVar5, onvalue=5, offvalue=0, height=1, width=20)
        C5.pack(side=TOP)
        C6 = Checkbutton(top, text="词组", variable=self.CheckVar6, onvalue=6, offvalue=0, height=1, width=20)
        C6.pack(side=TOP)
        C7 = Checkbutton(top, text="例句", variable=self.CheckVar7, onvalue=7, offvalue=0, height=1, width=20)
        C7.pack(side=TOP)
        button = Button(top, text="下一步",width = 50, height = 2, command = lambda: self.status_get(num))
        button.pack(side = TOP)

    #同时为生成excel和生成思维导图创建小窗口，方便选择生成内容。
    def status_get(self,num):
        for number in [a.get() for a in [self.CheckVar1,self.CheckVar2,self.CheckVar3,self.CheckVar4,
                                         self.CheckVar5,self.CheckVar6,self.CheckVar7]]:
            if number != 0:
                self.fbxmind.append(int(number))
            else:
                pass
        #在调用这个函数时会传入参数，如果参数为1则是点开思维导图的，2就是点开excel的，分别调用对应函数
        if num == 1:
            self.mindmap()
        if num == 2:
            self.getexcel()
        self.fbxmind=[] #每次生成完毕就清空fbxmind


root = Tk()
root.title("易背单词v2.1") #定义窗口的名字
root.geometry("500x700") #定义窗口的大小
app = App(root)
root.protocol("WM_DELETE_WINDOW", lambda: app.on_closing()) #引用函数，定义关闭事件
#主循环
root.mainloop()


