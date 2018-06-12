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
from Model.DoubanBook import DoubanBook
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import re
import urllib.parse
from env import mysqlConf
import pymysql
import pprint
import json

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

def login(driver):
  driver.get("https://accounts.douban.com/login")
  time.sleep(3)

  driver.find_element_by_xpath('//*[@id="email"]').send_keys('eamil@163.com')
  time.sleep(2)
  driver.find_element_by_xpath('//*[@id="password"]').send_keys('passwd')
  time.sleep(2)

  driver.find_element_by_xpath('//*[@id="lzform"]').submit()
  time.sleep(8)

def findTag(tag,start,type):
  return 'https://book.douban.com/tag/' + tag + '?start=' + str(start) + '&type=' + type

def findwork():
  try:
    doubanTag = DoubanTag.objects(isDone__lt = 1000).order_by('createdTime')[0]
    print('doubanTag.tag:',doubanTag.tag)
  except Exception as ex:
    print(ex)
    sys.exit()
  else:
    print('ok')
    return doubanTag

def startCrawl(driver):
  nowwork = findwork()
  nowtag = findTag(nowwork.tag,nowwork.isDone,'T')

  # driver.get(nowtag)

  # 获取当前窗口句柄
  topics_handle = driver.current_window_handle

  new_tab = 'window.open("' + nowtag + '")'
  driver.execute_script(new_tab)
  now_handles = driver.window_handles
  driver.switch_to.window(now_handles[-1])
  
  time.sleep(2)

  # XPATH
  xpath = '//html/body/div[3]/div[1]/div/div[1]/div/ul/li'
  BooksList = driver.find_elements_by_xpath(xpath)

  print('len(BooksList):',len(BooksList))
  if(len(BooksList) == 0):
    nowwork.isDone = 1000
    nowwork.save()
  else :
    for item in BooksList:
      avator = item.find_element_by_xpath('.//div[1]/a/img').get_attribute('src')
      bookId = item.find_element_by_xpath('.//div[2]/h2/a').get_attribute('href')
      title = item.find_element_by_xpath('.//div[2]/h2/a').get_attribute('title')
      bookId = int(re.search(r'subject\/(\d+?)\/', str(bookId)).group(1))
      doubanBook = DoubanBook(
        bookId = bookId,
        title = title,
        avator = avator,
        tagName = nowwork.tag,
        isDone = 0,
        createdTime = datetime.datetime.utcnow()
      )
      try:
        doubanBook.save()
      except:
        print("Error: 已经存在")
      else:
        print("内容写入文件成功")
      
    nowwork.isDone = nowwork.isDone + len(BooksList)
    nowwork.save()

  # close tag
  time.sleep(10)
  driver.close()
  driver.switch_to.window(topics_handle)
  
  return startCrawl(driver)
      
def main():
  connect(host='mongodb://crawler:crawler123@localhost:37102/zhihu')

  options = webdriver.ChromeOptions()
  options.add_argument('--disable-infobars')
  driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=options)

  # driver = webdriver.Remote(
  #  command_executor='http://192.168.199.111:4444/wd/hub',
  #  desired_capabilities=DesiredCapabilities.CHROME)
  # Mac下全屏
  driver.fullscreen_window()

  # 爬虫topic
  # startCrawl(driver)
  time.sleep(100)
  options.close()

def test():
  connect(host='mongodb://crawler:crawler123@localhost:37102/zhihu')

  options = webdriver.ChromeOptions()
  options.add_argument('--disable-infobars')
  driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=options)

  # driver = webdriver.Remote(
  #  command_executor='http://192.168.199.111:4444/wd/hub',
  #  desired_capabilities=DesiredCapabilities.CHROME)
  # Mac下全屏
  driver.fullscreen_window()

  # 登录
  login(driver)

  # 爬虫topic
  startCrawl(driver)

  time.sleep(100)
  options.close()

test()
# main()
