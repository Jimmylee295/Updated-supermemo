import json
from tkinter import *
from tkinter.filedialog import askopenfilename

class importdict():
    def __init__(self):
        #打开旧的字典
        with open('vocabulary.json', 'r', encoding='utf-8') as json_file:
            vocabulary2 = json.loads(json_file.read())
            self.vocabulary = json.loads(vocabulary2)
        #打开status.json
        with open('status.json', 'r', encoding='utf-8') as json_file:
            status2 = json.loads(json_file.read())
            self.status = json.loads(status2)


    def add(self):
        try:
            filename = askopenfilename()
            #打开新的词典
            with open(filename, 'r', encoding='utf-8') as json_file:
                vocabulary_new2 = json.loads(json_file.read())
                vocabulary_new = json.loads(vocabulary_new2)


            vocabulary = dict(self.vocabulary,**vocabulary_new)
            #更新本地文件
            json_vo = json.dumps(vocabulary, sort_keys=False, ensure_ascii=False)
            with open('vocabulary.json', 'w', encoding='utf-8') as json_file:
                json.dump(json_vo, json_file, ensure_ascii=False)

            #更新status文件，以便导入后立刻可以背
            status_new = {}
            for word in list(vocabulary_new.keys()):
                status_new[word] = ["2000-1-1",0,1,2.5]

            status = dict(self.status,**status_new)

            #写入status.json
            json_sta = json.dumps(status, sort_keys=False, ensure_ascii=False)
            with open('status.json', 'w', encoding='utf-8') as json_file:
                json.dump(json_sta, json_file, ensure_ascii=False)

        except:
            pass

