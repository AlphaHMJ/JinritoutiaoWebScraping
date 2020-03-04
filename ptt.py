# -*- coding: utf-8 -*-

#一次2000篇，不用去重
#一天两次，早9:30上一次晚上21:30，一次共4000篇
#ssh root@10.1.1.227
#password: ceh@1234

# 引入模拟浏览器框架支持库
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 引入ActionChains鼠标操作类支持库
from selenium.webdriver.common.action_chains import ActionChains

# xpath解析支持库
from lxml import etree

# 自定义的新闻结构体
from newsInfo import NewsInfo

# 自定义解析html结构的实现类
from parseNews import PaseNews

import time

class ParseTouTiao(object):

    
#    构造函数，初始化资源
  
    def __init__(self):
        
        self.__firefox_options = webdriver.FirefoxOptions()
        self.__firefox_options.add_argument('--headless')
        self.__firefox_options.add_argument('--disable-gpu')
        #self.__browser = webdriver.Firefox(firefox_options=self.__firefox_options)
        self.__browser = webdriver.Firefox()
   
#    析构函数，释放资源
   
    def __del__(self):
        if self.__browser:
            try:
                self.__browser.close()
                self.__browser.quit()
            except Exception as ex:
                print(ex)
   
#    获取头条首页内容
    def __getTouTiaoHtml(self, url):
        
        # 简单的入参校验
        if url and '' != url and url.startswith("http"):
            
            # 浏览器打开页面
            self.__browser.get(url)

            try:
                # 此处等到我们所需的热文元素加载出来了再进行下一步，避免页面还没加载完成就去解析内容导致内容为空
                element = WebDriverWait(self.__browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//ul/li/div"))
                )
                    
            except Exception as ex:
                print(ex)
            finally:
                pass
                        
            try:
                 # 模拟滚动到底部100
                # for i in range(100):
                for i in range(1):
                    self.__browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                    time.sleep(4)
            except Exception as ex:
                print(ex)

            resHtml = self.__browser.page_source
##            print(resHtml)
            return resHtml


    def _parseNews(self, url):
        resHtml = self.__getTouTiaoHtml(url)

        if not resHtml:
            print("解析内容出错")
            return

        # 转换为etree解析模式内容
        etree_html = etree.HTML(resHtml)

        # 通过前面对每条新闻dom结构分析，由xpath方式提取所有新闻所在的<li>布局
        li_elements = etree_html.xpath('//ul/li')
#        print(li_elements)
       
        # 解析得到的新闻列表
        parseNewsInfo = []

        # 新闻解析类
        parseNew = PaseNews()
        
        new_file=open('news.txt','w')

        if li_elements and len(li_elements) > 0:
            for li in li_elements:
                
                newinf = parseNew.parse(li)
#                print(parseNewsInfo)

                if newinf:
                    parseNewsInfo.append(newinf)
                    
                    new_file.write(newinf.title+';'+newinf.detail_link+';'+newinf.publish_time+';'+newinf.comment+';'+newinf.read+'\n')
                    
#                    print(" 标题：'%s'\n 链接：'%s'\n 时间：'%s'\n 评论: '%s'\n 阅读: '%s'\n" % 
#                          (newinf.title, newinf.detail_link,newinf.publish_time, newinf.comment, newinf.read)
#                         )
            print('Parsing Finished')
            new_file.close()
        else:
            new_file.close()
#            return
def main():
   print('Parsing Start')
   # ptt = ParseTouTiao()
   # ptt._parseNews("https://www.toutiao.com/c/user/98951151553/#mid=1601313613346829")
   
    while True:
#        print("Start : %s" % time.ctime())
        time_now = time.strftime("%H:%M:%S", time.localtime()) # 刷新
        if time_now == "09:30:00":
            subject = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " Start parsing"
            print(subject)
            ptt = ParseTouTiao()
            ptt._parseNews("https://www.toutiao.com/c/user/98951151553/#mid=1601313613346829")
        elif time_now == "21:30:00":
            print(subject)
            ptt = ParseTouTiao()
            ptt._parseNews("https://www.toutiao.com/c/user/98951151553/#mid=1601313613346829")


    # 程序主入口
if __name__ == '__main__':
    main()
        
