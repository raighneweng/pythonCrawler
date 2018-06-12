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
from Model.Topics import Topic
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import sys   
sys.setrecursionlimit(1000000) #例如这里设置为一百万 

def getTopicOrg(id):
  return 'https://www.zhihu.com/topic/' + str(id) + '/organize'

def login(driver):
  driver.get("https://www.zhihu.com")
  time.sleep(3)
  driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[2]/span').click()
  time.sleep(2)

  driver.find_element_by_name('username').send_keys('username')
  time.sleep(2)
  driver.find_element_by_name('password').send_keys('passwd')
  time.sleep(5)

  driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/button').click()
  time.sleep(3)

def findWork():
  topic = Topic.objects(isDone = 0).order_by('createdTime')[0]
  return topic

def startCrawl(driver):
  nowTopic = findWork()
  href = getTopicOrg(nowTopic.topicId)

  # 获取当前窗口句柄
  topics_handle = driver.current_window_handle

  new_tab = 'window.open("' + href + '")'
  driver.execute_script(new_tab)
  now_handles = driver.window_handles
  driver.switch_to.window(now_handles[-1])
  
  time.sleep(4)

  current_url = driver.current_url
  if current_url.endswith("hot"):
    # get sameTopicId
    sameTopicId = int(current_url.split('/')[4])
    # 标记完成
    nowTopic.isDone = 2
    
    if sameTopicId not in nowTopic.sameTopic:
      nowTopic.sameTopic.append(sameTopicId)
    nowTopic.updatedTime = datetime.datetime.utcnow()
    nowTopic.save()
    
    #记录
    newTopicTitle = driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div[1]/div[1]/div[1]/div[1]/div/div[2]/h2/div/h1').get_attribute('innerHTML')
    newTopic = Topic(
      topicId = sameTopicId,
      title = newTopicTitle,
      isDone = 0,
      createdTime = datetime.datetime.utcnow()
    )
    try:
      newTopic.save()
    except:
      print("Error: 已经存在")
    else:
      print("内容写入文件成功")
  else:
    # XPATH
    focusPeople_xpath = '//*[@id="zh-topic-side-head"]/div/a/strong'
    fatherId_xpath = '//*[@id="zh-topic-organize-parent-editor"]/div/a'
    childId_xpath = '//*[@id="zh-topic-organize-child-editor"]/div/a'

    try:
      focusPeople = driver.find_element_by_xpath(focusPeople_xpath).get_attribute('innerHTML')
    except:
      print("当前话题关注人数为0")
      focusPeople = 0
    else:
      print("当前话题关注人数")
      print(focusPeople)

    fatherId_List = driver.find_elements_by_xpath(fatherId_xpath)
    childId_List = driver.find_elements_by_xpath(childId_xpath)
    # try:
    #   fatherId_List = driver.find_elements_by_xpath(fatherId_xpath)
    #   childId_List = driver.find_elements_by_xpath(childId_xpath)
    # except:
    #   nowTopic.isDone = 2
    #   nowTopic.updatedTime = datetime.datetime.utcnow()
    #   nowTopic.save()
    #   return startCrawl(driver)
    # else:
    #   print("话题合并失败") 

    fatherlist = []
    for fatherId in fatherId_List:
      fatherIdText = fatherId.text
      fatherIdData = fatherId.get_attribute('data-token')
      print(fatherIdText)
      print(fatherIdData)
      # save shuju
      topic = Topic(
        topicId = fatherIdData,
        title = fatherIdText,
        isDone = 0,
        createdTime = datetime.datetime.utcnow()
      )
      try:
        topic.save()
      except:
          print("Error: 已经存在")
      else:
          print("内容写入文件成功")
      fatherlist.append(fatherIdData)

    for childId in childId_List:
      childIdText = childId.text
      childIdData = childId.get_attribute('data-token')
      print(childIdText)
      print(childIdData)

      # save shuju
      topic = Topic(
        topicId = childIdData,
        title = childIdText,
        isDone = 0,
        createdTime = datetime.datetime.utcnow()
      )
      try:
        topic.save()
      except:
          print("Error: 已经存在")
      else:
          print("内容写入文件成功")

    # tag db isDone
    print(fatherlist)
    nowTopic.fatherId = fatherlist
    nowTopic.focusPeople = focusPeople
    nowTopic.isDone = 1
    nowTopic.updatedTime = datetime.datetime.utcnow()
    nowTopic.save()

  # close tag
  driver.close()
  driver.switch_to.window(topics_handle)
  time.sleep(2)
  
  # iteration operation
  return startCrawl(driver)

def main():
  connect('zhihu', host='localhost', port=27017)

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
  connect('zhihu', host='localhost', port=27017)

  options = webdriver.ChromeOptions()
  options.add_argument('--disable-infobars')
  driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=options)
  # driver = webdriver.Remote(
  #  command_executor='http://192.168.0.177:4444/wd/hub',
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