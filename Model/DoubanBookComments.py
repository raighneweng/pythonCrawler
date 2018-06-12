from mongoengine import *
import datetime

class DoubanBookComments(Document):
  bookId = IntField(required=True)
  score = StringField(max_length=200)
  content = StringField()
  useful = IntField()
  createdTime = DateTimeField(defualt = datetime.datetime.utcnow())
  updatedTime = DateTimeField(defualt = datetime.datetime.utcnow())