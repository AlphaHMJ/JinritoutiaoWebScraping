# -*- coding: utf-8 -*-


# xpath解析支持库
from lxml import etree

# 正则表达式支持库
import re

# 自定义的新闻结构体
from newsInfo import NewsInfo, NewsType

class PaseNews(object):

#    解析纯文本类型新闻
    def __parseTextNew(self, li_etree):
        
        new_info = NewsInfo()

        # 获取标题
        new_info.title = li_etree.xpath('./div[contains(@class, "item-inner")]/div[contains(@class, "no-image")]/div/div[@class="title-box"]/a/text()')[0]

        # 获取详情的相对地址
        new_info.detail_link = li_etree.xpath('./div[contains(@class, "item-inner")]/div[contains(@class, "no-image")]/div/div[@class="title-box"]/a/@href')[0]

#        # 获取新闻发布时间
        publish_time = li_etree.xpath('./div[contains(@class, "item-inner")]/div[contains(@class, "no-image")]/div/div[contains(@class, "footer")]/div/span[@class="lbtn"]/text()')
        if publish_time and len(publish_time) > 0:
            new_info.publish_time = publish_time[0].replace("⋅", '').strip()

        # 获取评论数
        comment = li_etree.xpath('./div[contains(@class, "item-inner")]/div[contains(@class, "no-image")]/div/div[contains(@class, "footer")]/div/a[@ga_event="article_comment_click"]/text()')
        if comment and len(comment) > 0:
            new_info.comment = comment[0].replace(" ", '').strip()
            
        # 获取阅读数
        read = li_etree.xpath('./div[contains(@class, "item-inner")]/div[contains(@class, "no-image")]/div/div[contains(@class, "footer")]/div/a[@ga_event="article_read_count"]/text()')
        if read and len(read) > 0:
            new_info.read = read[0].replace("⋅", '').strip()

        return new_info

  
#    解析图文类型新闻
    def __parseImageNew(self, li_etree):
        new_info = NewsInfo()

        # 获取标题
        new_info.title = li_etree.xpath('./div[contains(@class, "item-inner")]/div[contains(@class, "rbox")]/div/div[@class="title-box"]/a/text()')[0]

        # 获取详情的相对地址
        new_info.detail_link = li_etree.xpath('./div[contains(@class, "item-inner")]/div[contains(@class, "rbox")]/div/div[@class="title-box"]/a/@href')[0]

        # 获取新闻发布时间
        publish_time = li_etree.xpath('./div[contains(@class, "item-inner")]/div[contains(@class, "rbox")]/div/div[contains(@class, "footer")]/div/span[@class="lbtn"]/text()')
        if publish_time and len(publish_time) > 0:
            new_info.publish_time = publish_time[0].replace("⋅", '').strip()

        # 获取评论数
        comment = li_etree.xpath('./div[contains(@class, "item-inner")]/div[contains(@class, "rbox")]/div/div[contains(@class, "footer")]/div/a[@ga_event="article_comment_click"]/text()')
        if comment and len(comment) > 0:
            new_info.comment = comment[0].replace(" ", '').strip()
            
#        # 获取阅读数
        read = li_etree.xpath('./div[contains(@class, "item-inner")]/div[contains(@class, "rbox")]/div/div[contains(@class, "footer")]/div/a[@ga_event="article_read_count"]/text()')
        if read and len(read) > 0:
            new_info.read = read[0].replace("⋅", '').strip()
        
        return new_info



    def parse(self, li_etree):
        
        newsInfo = None

        # 获取当前新闻类型
        if li_etree.xpath('./div[contains(@class, "item-inner")]/div[contains(@class, "no-image")]'):

            # 纯文本类型
            newsInfo = self.__parseTextNew(li_etree)

        elif li_etree.xpath('./div[contains(@class, "item-inner")]/div[contains(@class, "rbox")]'):

            # 图文类型
            newsInfo = self.__parseImageNew(li_etree)
        

        return newsInfo