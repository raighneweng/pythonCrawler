from mongoengine import *
import datetime

class Topic(Document):
  topicId = IntField(max_length=32,required=True,unique=True)
  title = StringField(max_length=200)
  fatherId = ListField(IntField())
  focusPeople = IntField()
  isDone = IntField(required=True)
  sameTopic = ListField(IntField())
  createdTime = DateTimeField(defualt = datetime.datetime.utcnow())
  updatedTime = DateTimeField(defualt = datetime.datetime.utcnow())