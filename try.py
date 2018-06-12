import re

info = "<spanclass="pl">作者:</span>&nbsp;<ahref="https://book.douban.com/author/1039386/">[哥伦比亚]加西亚·马尔克斯</a><br><spanclass="pl">出版社:</span>南海出版公司<br><spanclass="pl">原作名:</span>Cienañosdesoledad<br><spanclass="pl">译者:</span>&nbsp;<ahref="https://book.douban.com/author/4608209/">范晔</a><br><spanclass="pl">出版年:</span>2011-6<br><spanclass="pl">页数:</span>360<br><spanclass="pl">定价:</span>39.50元<br><spanclass="pl">装帧:</span>精装<br><spanclass="pl">丛书:</span>&nbsp;<ahref="https://book.douban.com/series/10489">新经典文库:加西亚·马尔克斯作品</a><br><spanclass="pl">ISBN:</span>9787544253994<br>"


regexAuthor = r'作者(.{1,30})href="(.{1,50})">(.{1,30})<\/a'
  # regexAuthor222 = r'作者<\/span>:<.*href="(.*)">(.*)<\/a'

m = re.search(regexAuthor, info)
print(m.group())