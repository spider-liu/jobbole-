# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import MySQLdb
import MySQLdb.cursors
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi



class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWithEncodingPipeline(object):
    #自定义json文件的导出
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding="utf-8")
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item
    def spider_closed(self, spider):
        self.file.close()


#jsonexporter的使用
class JsonExporterPipleline(object):
    #调用scrapy提供的json export导出json文件
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


# #mysql的配置
# class MysqlPipeline(object):
#     #采用同步的机制写入mysql
#     def __init__(self):
#         self.conn = MySQLdb.connect('192.168.0.116', 'root', 'spiderliu', 'article_spider', charset="utf8", use_unicode=True)
#         self.cursor = self.conn.cursor()
#
#     def process_item(self, item, spider):
#         insert_sql = """
#             insert into jobbole_article(title,create_date,url,url_object_id,front_image_url,comm_nums,fav_nums,praise_nums,tags )
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#         """
#         self.cursor.execute(insert_sql,(item["title"],item["create_date"],item["url"],item["url_object_id"],item["front_image_url"],item["comm_nums"],item["fav_nums"],item["praise_nums"],item["tags"]))
#         self.conn.commit()
#     def spider_closed(self,spider):
#         self.conn.close()



#mysql插入的异步化
class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) #处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print (failure)

    def do_insert(self, cursor, item):
        insert_sql = """
                    insert into jobbole_article(title,create_date,url,url_object_id,front_image_url,comm_nums,fav_nums,praise_nums,tags )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        cursor.execute(insert_sql, (item["title"], item["create_date"], item["url"], item["url_object_id"], item["front_image_url"],item["comm_nums"], item["fav_nums"], item["praise_nums"], item["tags"]))


class ArticleImagePipeline(ImagesPipeline):
    #从内置的ImagesPipeline获取的，这是下载图片的存放路径，从这可以获取路径
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            #获取图片的存放路径，将存放路径提取图片
            for ok, value in results:
                image_file_path=value["path"]
            item["front_image_path"]=image_file_path
        return item


    pass