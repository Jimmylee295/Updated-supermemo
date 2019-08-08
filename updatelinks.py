from urllib.request import urlopen
import urllib
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image, ImageEnhance



# 打开浏览器
#chrome_options=chrome_options
dict = {}
link = {}
class getlinks():
    def __init__(self):
        self.b = 0

    def getitems(self,word,driver):
        self.b = 1
        while True:
            try:
                element = driver.find_elements_by_class_name("art_pic")
                list = []
                for a in element:
                    print(a.get_attribute("href"))
                    list.append(a.get_attribute("href"))
                link[word] = list
                if self.b == 1:
                    driver.find_element_by_xpath("/html/body/div[5]/div[2]/div[5]/div[1]/div[2]/span/a[5]").click()
                    self.b += 1
                    time.sleep(1)
                elif self.b > 1 and self.b < 10:
                    driver.find_element_by_xpath("/html/body/div[5]/div[2]/div[5]/div[1]/div[2]/span/a[6]").click() #用xpath定位模拟点击
                    self.b += 1
                    time.sleep(1)
                else:
                    print("爬取结束")
                    break
            except:
                print("未知错误")
                break


    def setuplinks(self):
        with open('vocabulary.json', 'r', encoding='utf-8') as json_file:
            vocabulary2 = json.loads(json_file.read())
            vocabulary = json.loads(vocabulary2)
        #设置浏览器参数，包括禁止加载，打开最大化
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--start-maximized')
        driver = webdriver.Chrome()
        driver.maximize_window()
        for word in list(vocabulary.keys()):
            try:
                driver.get("http://newssearch.chinadaily.com.cn/en/search?query="+str(word.strip()))
            except:
                pass
            else:
                time.sleep(1)
                self.getitems(word,driver)

        link_json = json.dumps(link, sort_keys=False, ensure_ascii=False)
        with open('link.json', 'w', encoding='utf-8') as json_file:
            json.dump(link_json, json_file, ensure_ascii=  False)