from mongoengine import *
import datetime

class DoubanAuthor(Document):
  autherId =  IntField(required=True,unique=True)
  autherName = StringField(max_length=200)
  avator = StringField(max_length=200)
  gender = StringField(max_length=20)
  birthdate = StringField(max_length=200)
  deathdate = StringField(max_length=200)
  nation = StringField(max_length=200)
  introduction = StringField()
  mostLikedBooks = ListField(IntField())
  latestPublicedBooks = ListField(IntField())
  isDone = IntField(required=True)
  createdTime = DateTimeField(defualt = datetime.datetime.utcnow())
  updatedTime = DateTimeField(defualt = datetime.datetime.utcnow())