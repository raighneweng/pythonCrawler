from mongoengine import *
import datetime
from Model.Topics import Topic
import time
from Model.DoubanTag import DoubanTag
# connect('test', host='localhost', port=27017)

# topic = Topic(
#   topicId = 19564496,
#   title = "女朋友",
#   isDone = 0,
#   createdTime = datetime.datetime.utcnow(),
#   updatedTime = datetime.datetime.utcnow()
# )

# def findWork():
#   topic = Topic.objects(isDone = 0).order_by('createdTime')[0]
#   return topic

# nowTopic = findWork()
# print(nowTopic.topicId)
# topic = Topic.objects(isDone = 0).order_by('createdTime')[0]
# if 3 not in topic.fatherId:
#   topic.fatherId.append(3)
#   topic.save()
# try:
#   sameTopic = topic.sameTopic
# except:
#   # nowTopic.sameTopic = 3
#   print(1)
# else:
#   print(2)
# if len(topic.sameTopic) = 0:
#   topic.sameTopic = 3

# if 3 not in topic.sameTopic:
#     topic.sameTopic.append(3)
# topic.save()


# try:
#   topic.save()
# except:
#     print("Error: 已经存在")
# else:
#     print("内容写入文件成功")

# try:
#   location = Topic.objects.get(topicId=19550377)
# except:
#   topic.save()
# else:
#   print
# time.sleep(30)

# doubanTag = DoubanTag.objects(isDone__lt = 1000).order_by('-createdTime')[0]
# print('doubanTag.tag:',doubanTag.tag)

try:
  # raise ValueError('oops!')
  print('qqq')
except:
  print('err')
else:
  print('11111')