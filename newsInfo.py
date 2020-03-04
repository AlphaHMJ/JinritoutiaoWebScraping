# -*- coding: utf-8 -*-


from enum import Enum, unique

@unique
class NewsType(Enum):
    pass
   
class NewsInfo:

    # 标题
    title = ''

    # 发表时间
    publish_time = ''

    # 详情url
    detail_link = ''
    
    # 阅读数
    read = ''
    
    #评论数
    comment = ''

