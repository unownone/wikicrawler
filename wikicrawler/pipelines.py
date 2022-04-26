# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from wikicrawler import settings
import mongoengine as db
from scrapy.exceptions import DropItem


class Article(db.Document):
    title = db.StringField()
    url = db.StringField()
    

class Topic(db.Document):
    subtitle = db.StringField()
    body = db.StringField()
    article = db.ReferenceField(Article)


class MongoDBPipeline(object):
    
    def __init__(self):
        db.connect(settings.MONGODB_COLLECTION,
            host=settings.MONGODB_HOST)


    def process_item(self,item,spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("missing {0}!".format(data))
        if valid:
            if Article.objects.get(url=item['url']):
                raise DropItem("Duplicate item found: {0}".format(item))
            Article.objects.create(
                title=item['title'],
                data='\n'.join(item['data']),
                url=item['url']
            )
        return item
    
    
class WikicrawlerPipeline:
    def process_item(self, item, spider):
        return item
