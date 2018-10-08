# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import JobBoleArticleItem
from ArticleSpider.utils.common import get_md5
from scrapy.loader import ItemLoader


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    #起始页，注意url的值
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self,response):

        # #re1_selector=response.xpath("/html/body/div[1]/div[3]/div[1]/div[1]/h1/text()")
        # #re2_selector=response.xpath('//*[@id="post-114391"]/div[1]/h1/text()')
        # #re3_selctor=response.xpath('//div[@class="entry-header"]/h1/text()')
        '''
        1、获取文章列表页中的文章url并且交给scrapy下载后进行解析
        2、获取下一页的并且交给scrapy进行下载，下载完成后交给parse
        '''

        # #解析列表页中所有的额文章，并且交给scrapy下载后进行解析
        # #post_urls为一页的url的集合，通过css选择器将每个url进行提取，提取的方式是class下面的两个值的其中一个href，class省略掉了，提取href属性的时候使用attr方法
        # #改成post_nodes为了直接获取a的节点，里面含有图片
        # post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        # for post_node in post_nodes:
        #     #callback为回调函数，将提取的url所在页进行具体提取
        #     #为了解决url不是全部，将其进行构建形成完整url，出现url初始化
        #     #meta方法是为了获取图片链接进行
        #     image_url = post_node.css("img::attr(src)").extract_first("")
        #     post_url = post_node.css("::attr(href)").extract_first("")
        #     yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},callback=self.parse_detail)
        #
        # #提取下一页并且交给scrapy进行下载
        # next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        # if next_url:
        #     yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

        #解析列表页中的所有文章url并交给scrapy下载后并进行解析
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url":image_url}, callback=self.parse_detail)

        #提取下一页并交给scrapy进行下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)





    #提取文章的具体字段
    def parse_detail(self,response):
        #导入后进行初始化
        article_item = JobBoleArticleItem()
        # #提取图片(文章封面图)
        # front_image_url = response.meta.get("front_image_url","")
        # #提取标题
        # title= response.css(".entry-header h1 ::text").extract()[0]
        # #小标题提取（时间节点）
        # create_date=response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace("·"," ").strip()
        #
        # #提取点赞数
        # praise_nums = response.css("span.vote-post-up h10::text").extract()[0]
        # #底部收藏数的提取
        # fav_nums= response.css("span.bookmark-btn ::text").extract()[0]
        # match_re=re.match(".*?(\d+).*","fav_nums")
        # if match_re:
        #      fav_nums=int(match_re.group(1))
        # else:
        #     fav_nums=0
        # # 底部评论数的提取
        # comm_nums = response.css("a[href='#article-comment'] span::text").extract()[0]
        # match_re = re.match(".*?(\d+).*", "comm_nums")
        # if match_re:
        #      comm_nums = int(match_re.group(1))
        # else:
        #     comm_nums=0
        # #主体正文内容
        # content = response.css("div.entry").extract()[0]
        # # 小标题节点的提取,里面将某个节点去重进行
        # tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        # tags = ",".join(tag_list)
        #
        #
        #
        #
        # # title=response.xpath('//div[@class="entry-header"]/h1/text()')
        # # #小标题的提取（时间）
        # # create_date= response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace("·"," ").strip()
        # # #小标题节点的提取,里面将某个节点去重进行
        # # tag_list=response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        # # tag_list=[element for element in tag_list if not element.strip().endswith("评论")]
        # # tags=",".join(tag_list)
        # # #底部点赞数的提取
        # # praise_nums=response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract()[0]
        # # #底部收藏数的提取
        # # fav_nums=response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract()[0]
        # # match_re1 = re.match(r".*?(\d+).*",fav_nums)
        # # if match_re1:
        # #     fav_nums=match_re1.group(1)
        # # #底部评论数的提取
        # # comm_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()
        # # match_re2 = re.match(".*?(\d+).*",comm_nums)
        # # if match_re2:
        # #     comm_nums = match_re2.group(1)
        # # #主体正文内容
        # # content=response.xpath("//div[@class='entry']").extract()[0]
        #
        # article_item["url_object_id"]=get_md5(response.url)
        # article_item["title"]=title
        # article_item["url"]=response.url
        # try:
        #     create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
        # except Exception as e:
        #     create_date = datetime.datetime.now().date()
        # article_item["create_date"] = create_date
        # article_item["front_image_url"] = [front_image_url]
        # article_item["praise_nums"] = praise_nums
        # article_item["comm_nums"] = comm_nums
        # article_item["fav_nums"] = fav_nums
        # article_item["tags"] = tags
        # article_item["content"] = content


        #通过itemloader加载item
        front_image_url = response.meta.get("front_image_url", "")#文章封面
        item_loader=ItemLoader(item=JobBoleArticleItem(),response=response)
        item_loader.add_css("title",".entry-header h1 ::text")
        item_loader.add_value("url",response.url)
        item_loader.add_value("url_object_id",get_md5(response.url))
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_css("praise_nums", ".vote-post-up h10::text")
        item_loader.add_css("comm_nums", "a[href='#article-comment'] span::text")
        item_loader.add_css("fav_nums", ".bookmark-btn::text")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("content", "div.entry")

        article_item=item_loader.load_item()


        yield article_item





