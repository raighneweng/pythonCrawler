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
from Model.DoubanAuthor import DoubanAuthor
from Model.DoubanSeries import DoubanSeries
from Model.DoubanBookComments import DoubanBookComments
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

  driver.find_element_by_xpath('//*[@id="email"]').send_keys('email')
  time.sleep(2)
  driver.find_element_by_xpath('//*[@id="password"]').send_keys('passwd')
  time.sleep(2)

  time.sleep(10)
  driver.find_element_by_xpath('//*[@id="lzform"]').submit()

def findwork():
  try:
    doubanBook = DoubanBook.objects(isDone = 0).order_by('createdTime')[0]
    print('findwork,doubanBook.bookId:',doubanBook.bookId)
  except Exception as ex:
    print(ex)
    sys.exit()
  else:
    print('findwork,ok')
    return doubanBook

def openBookurl(bookId):
  return 'https://book.douban.com/subject/' + str(bookId) + '/'

def regexData(info):
  regexAuthor = r'作者(.{1,30})href="(.{1,50})">(.{1,30})<\/a'
  regexPublisher = r'出版社(.{1,30})span>(.{1,15})<br'
  regexOriginalName = r'原作名(.{1,15})>(.{1,30})<br'
  regexTranslator = r'译者(.{1,35})href="(.{1,80})">(.{1,30})<\/a'
  regexPublishDate = r'出版年(.{1,20})>(.{1,20})<br'
  regexPage = r'页数(.{1,20})>([0-9]{1,10})<br'
  regexPrice = r'定价(.{1,20})>(.{1,10})<br'
  regexBinding = r'装帧(.{1,20})>(.{1,10})<br'
  regexSeries =  r'丛书(.{1,35})href="(.{1,80})">(.{1,30})<\/a'
  regexISBN = r'ISBN(.{1,20})>([0-9]{13})<br'

  try:
    authorUrl = re.search(regexAuthor, info).group(2)
    authorId = int(re.search(r'author\/([0-9]{1,20})', authorUrl).group(1))
  except:
    authorId = 0

  try:
    publisher = re.search(regexPublisher, info).group(2)
  except:
    publisher = ''
  # print("publisher:",publisher)

  try:
    originalName = re.search(regexOriginalName, info).group(2)
  except:
    originalName = ''
  # print("originalName:",originalName)

  try:
    translator = re.search(regexTranslator, info).group(3)
  except:
    translator = ''
  # print("translator:",translator)

  try:
    publishDate = re.search(regexPublishDate, info).group(2)
  except:
    publishDate = ''
  # print("publishDate:",publishDate)

  try:
    page = re.search(regexPage, info).group(2)
  except:
    page = 0
  # print("page:",page)

  try:
    price = re.search(regexPrice, info).group(2)
  except:
    price = ''
  # print("price:",price)
  
  try:
    seriesHref = re.search(regexSeries, info).group(2)
    seriesName = re.search(regexSeries, info).group(3)
    seriesId = int(re.search(r'series\/([0-9]{1,20})', seriesHref).group(1))
  except:
    seriesId = 0
    seriesName = ''

  try:
    binding = re.search(regexBinding, info).group(2)
  except:
    binding = ''
  # print("binding:",binding)

  try:
    ISBN = re.search(regexISBN, info).group(2)
  except:
    ISBN = 0
  # print("ISBN:",ISBN)

  return authorId,publisher,originalName,translator,publishDate,page,price,binding,seriesId,seriesName,ISBN

def startCrawl(driver):
  doubanBook = findwork()
  nowtag = openBookurl(doubanBook.bookId)

  # 获取当前窗口句柄
  topics_handle = driver.current_window_handle

  new_tab = 'window.open("' + nowtag + '")'
  driver.execute_script(new_tab)
  now_handles = driver.window_handles
  driver.switch_to.window(now_handles[-1])
  
  time.sleep(4)

  # Info Xpath
  infoXpath = '//*[@id="info"]'
  # 作者,出版社,原名,译者,出版年,页数,定价,装订,丛书,isbn
  try:
    info = driver.find_element_by_xpath(infoXpath)
  except:
    print("info未发现")
    doubanBook.isDone = 2
  else:
    info  = ''.join(info.get_attribute('innerHTML').split())
    print("info:",info)
  
  try:
    authorId,publisher,originalName,translator,publishDate,page,price,binding,seriesId,seriesName,ISBN = regexData(info)
    print(authorId,publisher,originalName,translator,publishDate,page,price,binding,seriesId,seriesName,ISBN)
  except:
    time.sleep(5)
    driver.close()
    driver.switch_to.window(topics_handle)
  else:
    if ISBN == 0:
      print("ISBN == 0")
      doubanBook.isDone = 2
    else:  
      # 评分 Xpath
      scoreXpath = '//*[@id="interest_sectl"]/div/div[2]/strong'
      introductionXpath = '//*[@id="link-report"]/div[1]/div'
      moreTagsXpath = '//*[@id="db-tags-section"]/div/span'
      alsoLikeListXpath = '//*[@id="db-rec-section"]/div/dl'
      commentsXpath = '//*[@id="comments"]/ul/li'

      try:
        BookScore = driver.find_element_by_xpath(scoreXpath).get_attribute('innerHTML')
      except:
        BookScore = '0'
        print("BookScore未发现")
      else:
        print("BookScore:",BookScore)

      try:
        introduction = driver.find_element_by_xpath(introductionXpath).get_attribute('innerHTML')
      except:
        try:
          introduction = driver.find_element_by_xpath('//*[@id="link-report"]/span[1]/div').get_attribute('innerHTML')
        except:
          introduction = ''
          print("introduction未发现")
      print("introduction:",introduction)

      try:
        moreTags = driver.find_elements_by_xpath(moreTagsXpath)
      except:
        moreTags = []
        print("moreTags未发现")
      else:
        print("moreTags.length:",len(moreTags))

      try:
        alsoLikeList = driver.find_elements_by_xpath(alsoLikeListXpath)
      except:
        alsoLikeList = []
        print("alsoLikeList未发现")
      else:
        print("alsoLikeList.length:",len(alsoLikeList))
      
      try:
        commentsList = driver.find_elements_by_xpath(commentsXpath)
      except:
        commentsList = []
        print("commentsList未发现")
      else:
        print("commentsList.length:",len(commentsList))

      moreTagList = []
      for moreTag in moreTags:
        name = moreTag.find_element_by_xpath('.//a').get_attribute('innerHTML')
        href = urllib.parse.unquote(moreTag.find_element_by_xpath('.//a').get_attribute('href'))
        print('moreTag.name:',name)
        print('moreTag.href:',href)
        moreTagList.append(name)

        doubanTag = DoubanTag(
          className = '',
          tag = name,
          url = href,
          bookNum = 0,
          isDone = 0,
          createdTime = datetime.datetime.utcnow()
        )
        try:
          doubanTag.save()
        except:
          print("已存在:",name)
        else:
          print("写入成功:",name)

      sameList = []
      for likeitem in alsoLikeList:
        try:
          bookId = likeitem.find_element_by_xpath('.//dt/a').get_attribute('href')
          avator = urllib.parse.unquote(likeitem.find_element_by_xpath('.//dt/a/img').get_attribute('src'))
          name = likeitem.find_element_by_xpath('.//dd/a').get_attribute('innerHTML')
          bookId = int(re.search(r'subject\/(\d+?)\/', str(bookId)).group(1))
        except:
          print('分割线')
        else:
          print('likeitem.bookId:',bookId)
          print('likeitem.avator:',avator)
          print('likeitem.name:',name)
          sameList.append(bookId)

          doubanBook1 = DoubanBook(
            bookId = bookId,
            title = name,
            avator = avator,
            isDone = 0,
            createdTime = datetime.datetime.utcnow()
          )
          try:
            doubanBook1.save()
          except:
            print("Error: 已经存在")
          else:
            print("内容写入文件成功")

      for comment in commentsList:
        try:
          score = comment.find_element_by_xpath('.//div/h3/span[2]/span[1]').get_attribute('title')
        except:
          score = ''
        print('comment.score:',score)
        try:
          content = comment.find_element_by_xpath('.//div/p').get_attribute('innerHTML')
        except:
          content = ''
        print('comment.content:',content)
        try:
          useful = int(comment.find_element_by_xpath('.//div/h3/span[1]/span[1]').get_attribute('innerHTML'))
        except:
          useful = 0
        print('comment.useful:',useful)
        if content != '':
          doubanBookComments = DoubanBookComments(
            bookId = doubanBook.bookId,
            score = score,
            content = content,
            useful = useful
          )
          doubanBookComments.save()

      if authorId > 0:
        tmpAuthor = DoubanAuthor(
          autherId = authorId,
          isDone = 0,
          createdTime = datetime.datetime.utcnow()
        )

        try:
          tmpAuthor.save()
        except:
          print("author已存在:",authorId)
        else:
          print("author写入成功:",authorId)

      if seriesId > 0:
        doubanSeries = DoubanSeries(
          seriesId = seriesId,
          seriesName = seriesName,
          isDone = 0,
          createdTime = datetime.datetime.utcnow()
        )
        try:
          doubanSeries.save()
        except:
          print("seriesId已存在:",authorId)
        else:
          print("seriesId写入成功:",authorId)
    
      doubanBook.authorId = authorId
      doubanBook.publisher = publisher
      doubanBook.originalName = originalName
      doubanBook.translator = translator
      doubanBook.publishDate = publishDate
      doubanBook.page = page
      doubanBook.price = price
      doubanBook.binding = binding
      doubanBook.seriesId = seriesId
      doubanBook.ISBN = ISBN
      doubanBook.score = BookScore
      doubanBook.introduction = introduction
      doubanBook.moreTags = moreTagList
      doubanBook.alsoLikeList = sameList
      doubanBook.isDone = 1

    doubanBook.save()

    # close tag
    time.sleep(5)
    driver.close()
    driver.switch_to.window(topics_handle)
    
  return startCrawl(driver)
      
def main():
  connect(host='mongodb://crawler:crawler123@localhost:37102/zhihu')

  options = webdriver.ChromeOptions()
  options.add_argument('--disable-infobars')
  driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=options)

  # Mac下全屏
  driver.fullscreen_window()

  # 登录
  login(driver)

  # 爬虫topic
  startCrawl(driver)

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

# test()
main()
