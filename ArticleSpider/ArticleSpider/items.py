# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
#item.py的作用保存爬取数据的容器，类似python字典，并且提供了额外的保护机制防止避免拼写错误导致的未定义的字段错误。
import scrapy
from scrapy.loader.processors import MapCompose ,TakeFirst,Join
import datetime
from scrapy.loader import ItemLoader
import re




class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

#用在标题中或者其它位置进行添加名称等
def add_jobbole(value):
        return value+"-bobby"

#进行时间的修改，变成对象
def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()

    return create_date

def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


def remove_comment_tags(value):
    if "评论" in value:
        return ""
    else:
        return value


def return_value(value):
    return value

#自定义itemloader
class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


#将提取的字段进行实例化
class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(lambda x: x + "-jobbole",add_jobbole)
    )
    create_date=scrapy.Field(
        input_processor=MapCompose(date_convert),
        output_processor=TakeFirst()
    )
    url=scrapy.Field()
    url_object_id=scrapy.Field()
    front_image_url=scrapy.Field(
        input_processor=MapCompose(return_value)
    )
    front_image_path=scrapy.Field()
    praise_nums=scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comm_nums=scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags=scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(",")
    )
    content=scrapy.Field()