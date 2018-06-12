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
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import re
import urllib.parse
from env import mysqlConf
import pymysql
import pprint
import json

options = webdriver.ChromeOptions()
options.add_argument('--disable-infobars')
driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=options)

driver.fullscreen_window()

driver.get("https://book.douban.com/subject/6082808/")

def regexData(data):
  regexAuthor = r'作者(.{1,30})href="(.{1,50})">(.{1,30})<\/a'
  regexPublisher = r'出版社(.{1,30})span>(.{1,15})<br'
  regexOriginalName = r'原作名(.{1,15})>(.{1,30})<br'
  regexTranslator = r'译者(.{1,35})href="(.{1,80})">(.{1,30})<\/a'
  regexPublishDate = r'出版年(.{1,20})>(.{1,20})<br'
  regexPage = r'页数(.{1,20})>(.{1,10})<br'
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

if True:
  # Info Xpath
  # infoXpath = '//*[@id="info"]'
  # # 作者,出版社,原名,译者,出版年,页数,定价,装订,丛书,isbn
  # try:
  #   info = driver.find_element_by_xpath(infoXpath)
  # except:
  #   print("info未发现")
  #   doubanBook.isDone = 2
  # else:
  #   info  = ''.join(info.get_attribute('innerHTML').split())
  # print("info:",info)


  # authorId,publisher,originalName,translator,publishDate,page,price,binding,seriesId,seriesName,ISBN = regexData(info)
  # print(authorId,publisher,originalName,translator,publishDate,page,price,binding,seriesId,seriesName,ISBN)

  commentsXpath = '//*[@id="comments"]/ul/li'
  try:
    commentsList = driver.find_elements_by_xpath(commentsXpath)
  except:
    commentsList = []
    print("commentsList未发现")
  else:
    print("commentsList.length:",len(commentsList))

  for comment in commentsList:
    try:
      score = comment.find_element_by_xpath('.//div/h3/span[2]/span[1]').get_attribute('title')
    except:
      score = 0
    print(score)
    try:
      content = comment.find_element_by_xpath('.//div/p').get_attribute('innerHTML')
    except:
      content = ''
    print(content)
    try:
      useful = comment.find_element_by_xpath('.//div/h3/span[1]/span[1]').get_attribute('innerHTML')
    except:
      useful = 0
    print(useful)
  # score = StringField(max_length=200)
  # commentTime = DateTimeField(defualt = datetime.datetime.utcnow())
  # content = StringField(max_length=200)
  # useful = IntField()

  # # print(str(info.=get_attribute('innerHTML')).replace(" ", ""))
  # # 评分 Xpath
  # scoreXpath = '//*[@id="interest_sectl"]/div/div[2]/strong'
  # introductionXpath = '//*[@id="link-report"]/div[1]/div'
  # moreTagsXpath = '//*[@id="db-tags-section"]/div/span'
  # alsoLikeListXpath = '//*[@id="db-rec-section"]/div/dl'

  # try:
  #   score = driver.find_element_by_xpath(scoreXpath).get_attribute('innerHTML')
  # except:
  #   score = 0
  #   print("score未发现")
  # else:
  #   print("score：",score)

  # try:
  #   introduction = driver.find_element_by_xpath(introductionXpath).get_attribute('innerHTML')
  # except:
  #   introduction = ''
  #   print("introduction未发现")
  # else:
  #   print("introduction:",introduction)

  # try:
  #   moreTags = driver.find_elements_by_xpath(moreTagsXpath)
  # except:
  #   moreTags = []
  #   print("moreTags未发现")
  # else:
  #   print("moreTags:",moreTags)

  # try:
  #   alsoLikeList = driver.find_elements_by_xpath(alsoLikeListXpath)
  # except:
  #   alsoLikeList = []
  #   print("alsoLikeList未发现")
  # else:
  #   print("alsoLikeList:",alsoLikeList)

  # for moreTag in moreTags:
  #   name = moreTag.find_element_by_xpath('.//a').get_attribute('innerHTML')
  #   href = urllib.parse.unquote(moreTag.find_element_by_xpath('.//a').get_attribute('href'))
  #   print('moreTag.name:',name)
  #   print('moreTag.href:',href)

  # for likeitem in alsoLikeList:
  #   try:
  #     bookId = likeitem.find_element_by_xpath('.//dt/a').get_attribute('href')
  #     avator = urllib.parse.unquote(likeitem.find_element_by_xpath('.//dt/a/img').get_attribute('src'))
  #     name = likeitem.find_element_by_xpath('.//dd/a').get_attribute('innerHTML')
  #     bookId = int(re.search(r'subject\/(\d+?)\/', str(bookId)).group(1))
  #   except:
  #     print('分割线')
  #   else:
  #     print('likeitem.bookId:',bookId)
  #     print('likeitem.avator:',avator)
  #     print('likeitem.name:',name)