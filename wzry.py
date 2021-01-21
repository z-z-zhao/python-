import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import time
import re

class wzry():
    path=r"E:\wzry"
    rootUrl="https://pvp.qq.com/web201605/herolist.shtml"
    allHeroUrl={}
    driver = webdriver.Chrome()
    H={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}
    H1 = {"user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75"}
    def __init__(self):
        isE=os.path.exists(self.path)
        if not isE:
            os.makedirs(self.path)
        os.chdir(self.path)

    def getAllHero(self):
        HeadUrl="https://pvp.qq.com/web201605/"
        r=requests.get(self.rootUrl,headers=self.H1,stream=True)
        r.encoding="gbk"
        Html=BeautifulSoup(r.text,"lxml")

        #selenium +xpath
        self.driver.get('https://pvp.qq.com/web201605/herolist.shtml')
        # 全屏
        self.driver.maximize_window()
        # wait=WebDriverWait(driver,3)
        self.driver.implicitly_wait(3)  # 使用隐式等待
        resWZRY = self.driver.find_elements_by_xpath("//ul[@class='herolist clearfix']//a")
        print(resWZRY)
        for ares in resWZRY:
            self.allHeroUrl[ares.text]=ares.get_attribute("href")
        print(self.allHeroUrl)

        i=1
        for k in self.allHeroUrl.keys():
            self.getEverHeroImg(self.allHeroUrl[k], k,i)
            i+=1
            #
            # self.driver.get('https://pvp.qq.com/web201605/herolist.shtml')


    def getEverHeroImg(self,url,heroName,i):
        #请求到每个英雄的页面
        j=1
        self.driver.get(url)
        # wait=WebDriverWait(driver,3)
        self.driver.implicitly_wait(3)  # 使用隐式等待
        Hero_imgs = self.driver.find_elements_by_xpath("//ul[@class='pic-pf-list pic-pf-list3']//img")
        for img in Hero_imgs:
            aurl="http:"+img.get_attribute("data-imgname")
            skinName=img.get_attribute("data-title")
            self.saveImg(aurl, heroName,skinName,i,j)
            j+=1

    def saveImg(self,url,HeroName,SkinName,i,j):
        img=requests.get(url,headers=self.H1)
        f = open(str(i)+"."+str(j)+" "+HeroName+"_"+SkinName+".jpg",mode="ab")
        f.write(img.content)
        print(str(i)+"."+str(j)+" "+HeroName+"_"+SkinName+"成功爬取："+url)
        f.close()

    def close(self):
        self.driver.close()
if __name__=="__main__":
    t0=time.clock()
    Wz=wzry()
    Wz.getAllHero()
    t1=time.clock()
    print("总耗时：",t1-t0)

    # Wz.getEverHeroImg("https://pvp.qq.com/web201605/herodetail/106.shtml","小乔")
