from mongoengine import *
import datetime

class DoubanBook(Document):
  bookId = IntField(required=True,unique=True)
  title = StringField(max_length=200,required=True)
  avator = StringField(max_length=200,required=True)
  tagName = StringField(max_length=200)
  isDone = IntField(required=True)
  createdTime = DateTimeField(defualt = datetime.datetime.utcnow())
  updatedTime = DateTimeField(defualt = datetime.datetime.utcnow())
  
  authorId = IntField()
  publisher = StringField(max_length=200)
  originalName = StringField(max_length=200)
  translator = StringField(max_length=200)
  publishDate = StringField(max_length=200)
  page = IntField()
  seriesId = IntField()
  price = StringField(max_length=200)
  binding = StringField(max_length=200)
  ISBN = IntField()
  score = StringField(max_length=200)
  introduction = StringField()
  moreTags =  ListField(StringField())
  alsoLikeList =  ListField(IntField())