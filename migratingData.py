from mongoengine import *
from Model.Topics import Topic
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

def main():
  # mongodb
  connect(host='mongodb://crawler:crawler123@localhost:37102/zhihu')

  topic = Topic.objects(isDone__ne = 0).order_by('createdTime') 
  # for s in topic:
  #   topicId= s.topicId
  #   title = str(s.title)
  #   fatherId = s.fatherId if s.fatherId else None
  #   focusPeople = s.focusPeople if s.focusPeople else 0
  #   isMerge = 1 if s.isDone == 2 else 0
  #   mergeId = s.sameTopic if s.sameTopic else 0
    
    # sql1 = "INSERT INTO `topic` (`topicId`, `title`,`focusPeople`,`isMerge`,`mergeId`) VALUES ({0},'{1}',{2},{3},{4})".format(topicId,title,focusPeople,isMerge,mergeId)
    # print(sql1)
    #  cursor.executemany("INSERT INTO `topic` (`topicId`, `title`,`focusPeople`,`isMerge`,`mergeId`) VALUES (19589903,'网站建设',0,0,0)",)
    # conn.commit()
    # conn.close()
  #   # try:
      # cursor.executemany(sql1,(topicId,title,focusPeople,isMerge,mergeId))
    # except:
    #   print("内容重复").close()
    # else:
    #   print("内容写入文件成功")

  for s in topic:
    topicId= s.topicId
    title = s.title
    fatherId = s.fatherId if s.fatherId else None
    focusPeople = s.focusPeople if s.focusPeople else 0
    isMerge = 1 if s.isDone == 2 else 0
    mergeId = s.sameTopic if s.sameTopic else 0

    print(topicId)
    try:
      with conn.cursor() as cursor:
        sql1 = "INSERT INTO `zhihu_topic` (`topicId`, `title`,`focusPeople`,`isMerge`,`mergeId`) VALUES ({0},'{1}',{2},{3},{4})".format(topicId,title,focusPeople,isMerge,mergeId)
          # Create a new record
        cursor.execute(sql1,())
      conn.commit()
    except:
      print('已经存在')
    
    if fatherId:
      for k in fatherId:
        try:
          with conn.cursor() as cursor:
            sql1 = "INSERT INTO `zhihu_topic_link` (`fatherId`, `childId`) VALUES ({0},{1})".format(k,topicId)
              # Create a new record
            cursor.execute(sql1,())
          conn.commit()
        except:
          print('已经存在')
  
main()
# print(mysql)

