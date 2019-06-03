# coding: utf-8

import requests
from html.parser import HTMLParser
import re


# 设置http请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.933.400 QQBrowser/9.4.8699.400',
}

class MainParser(HTMLParser):

    flg = False         #标志，用以标记是否找到我们需要的标签
    img_flg = False
    tempstr = str()     #字符串类，存储标签中间的内容
    subhref = []        #将tempstr整合为列表
    img = []            #图片链接

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            # 判断标签<li>的属性
            for name, value in attrs:
                if name == 'dd_name' and value == '单品标题':
                    self.flg = True
                if name == 'dd_name' and value == '单品图片':
                    self.img_flg = True

        if self.flg == True:
            for name, value in attrs:
                # 用正则表达式匹配URL
                if name == 'href' and re.match(r'^(http://product.dangdang.com/)\d*\.\w+\?\w+', value.strip()) != None:
                    self.subhref.append(value)
                    self.flg = False

        if tag == 'img' and self.img_flg == True:
            for name, value in attrs:
                if name == 'data-original':
                    self.img.append(value)
                    self.img_flg = False
                if name == 'src' and re.match('http',value) != None:
                    self.img.append(value)
                    self.img_flg = False


    def handle_endtag(self, tag):
        if tag == 'a':
            self.img_flg = False


# 使用requests库封装一个简单的通过get方式获取网页源码的函数
def getsource(url):
    # 利用requests获取网页数据
    html = requests.get(url, headers=headers)
    s = html.text
    return s

def get_url_and_img(keyword, num):
    '''
    input: string:keyword int:num
    :return: url_list, img_list
    '''
    url_list = []
    img_list = []
    for i in range(1, num):
        str_num = str(i)
        url = 'http://search.dangdang.com/?key=' + keyword + '&act=input' + '&page_index=' + str_num
        # 获取网页内容
        text = getsource(url)
        # 初始化解析器
        parser = MainParser()
        # 将网页内容放入解析器
        parser.feed(text)
        url_list += parser.subhref
        parser.subhref.clear()
        img_list += parser.img
        parser.img.clear()
    return url_list, img_list
