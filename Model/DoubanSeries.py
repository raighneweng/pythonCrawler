from mongoengine import *
import datetime

class DoubanSeries(Document):
  seriesId =  IntField(required=True,unique=True)
  seriesName = StringField(max_length=200)
  isDone = IntField(required=True)
  createdTime = DateTimeField(defualt = datetime.datetime.utcnow())
  updatedTime = DateTimeField(defualt = datetime.datetime.utcnow())