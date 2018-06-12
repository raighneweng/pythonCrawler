from selenium import webdriver 
# from selenium.webdriver.common.keys import Keys
import time
import datetime
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from mongoengine import *
from Model.DoubanTag import DoubanTag
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re
import urllib.parse
from env import mysqlConf
import pymysql

import sys   
sys.setrecursionlimit(1000000) #例如这里设置为一百万 

conn = pymysql.connect(
  host='host',
  port=3306,
  user='user',
  password='passwd',
  db='db',
  charset='utf8mb4',
  cursorclass=pymysql.cursors.DictCursor
)

def openUrl(driver):
  driver.get("https://book.douban.com/tag/?view=type&icn=index-sorttags-all")
  time.sleep(3)

def startCrawl(driver):
  # XPATH
  xpath = '//*[@id="content"]/div/div[1]/div[2]/div'
  TagList = driver.find_elements_by_xpath(xpath)
  # print(TagList)

  for item in TagList:
    className = item.find_element_by_xpath('.//a').get_attribute('name')
    
    tbody = item.find_element_by_xpath('.//table/tbody')
    tagList = tbody.find_elements_by_xpath('.//td')

    for tagItem in tagList:
      tagName = tagItem.find_element_by_xpath('.//a').get_attribute('innerHTML')
      href = urllib.parse.unquote(tagItem.find_element_by_xpath('.//a').get_attribute('href'))
      bookNum = tagItem.find_element_by_xpath('.//b').get_attribute('innerHTML')
      print(tagName)
      print(href)
  
      bookNum = int(re.match(r'\((\d+?)\)', str(bookNum)).group(1))
      print(bookNum)
      
      ## MongoDB
      # doubanTag = DoubanTag(
      #   className = className,
      #   tag = tagName,
      #   url = href,
      #   bookNum = bookNum,
      #   isDone = 0,
      #   createdTime = datetime.datetime.utcnow()
      # )
      # doubanTag.save()
      
      ## Mysql
      # try:
      #   with conn.cursor() as cursor:
      #     sql1 = "INSERT INTO `douban_tag` (`className`, `tag`,`url`,`bookNum`,`isDone`) VALUES ('{0}','{1}','{2}',{3},{4})".format(className,tagName,href,bookNum,0)
      #       # Create a new record
      #     cursor.execute(sql1,())
      #   conn.commit()
      # except:
      #   print('已经存在')

def main():
  connect(host='mongodb://crawler:crawler123@localhost:37102/zhihu')

  options = webdriver.ChromeOptions()
  options.add_argument('--disable-infobars')
  driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=options)

  # Mac下全屏
  driver.fullscreen_window()

  openUrl(driver)

  # 爬虫topic
  startCrawl(driver)
  time.sleep(100)
  options.close()
  
main()