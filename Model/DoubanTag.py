from mongoengine import *
import datetime

class DoubanTag(Document):
  className = StringField(max_length=200)
  tag = StringField(max_length=200,required=True)
  url = StringField(max_length=200,required=True)
  bookNum = IntField()
  isDone = IntField(required=True)
  createdTime = DateTimeField(defualt = datetime.datetime.utcnow())
  updatedTime = DateTimeField(defualt = datetime.datetime.utcnow())