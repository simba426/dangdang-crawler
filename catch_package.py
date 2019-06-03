#coding：utf-8
from html.parser import HTMLParser
import requests
import re
import json

# 设置http请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.933.400 QQBrowser/9.4.8699.400',
}

contents_html = []
comments_html = []
goodrate = []

def isJson(jsonstr):
    try:
        json.dump(jsonstr)
        return True
    except:
        return False

class DInfoParser(HTMLParser):
    head = ''  # 原页面头部信息
    # 抓包所需的三个头部参数
    productId = ''
    categoryPath = ''
    mainProductId = ''
    # 判断是否找到正确的script
    script_flg = False
    is_ID = False
    comment_url = ''  # 评论数据包地址
    content_url = ''  # 内容简介数据包地址
    comments_html = ''  # 评论页源码
    contents_html = ''  # 内容页源码
    comments = []  # 评论列表
    contents = ''  # 内容字符串
    goodrate = ''  # 好评率

    def handle_data(self, data):
        if self.lasttag == 'script' and self.is_ID == False:
            if re.search(r'prodSpuInfo', data) != None:
                self.head = data
                self.is_ID = True

    #获取三个头部参数
    def get_elements(self):
        if re.search(r'\"productId\"\:\"\d+', self.head) != None:
            a = re.search(r'\"productId\"\:\"\d+', self.head).span()[0]
            b = re.search(r'\"productId\"\:\"\d+', self.head).span()[1]
            self.productId = self.head[a + 13:b]
        if re.search(r'\"mainProductId\"\:\"\d+', self.head) != None:
            a = re.search(r'\"mainProductId\"\:\"\d+', self.head).span()[0]
            b = re.search(r'\"mainProductId\"\:\"\d+', self.head).span()[1]
            self.mainProductId = self.head[a + 17:b]
        if re.search(r'\"categoryPath\"\:\"(\d+\.)+\d+', self.head) != None:
            a = re.search(r'\"categoryPath\"\:\"(\d+\.)+\d+', self.head).span()[0]
            b = re.search(r'\"categoryPath\"\:\"(\d+\.)+\d+', self.head).span()[1]
            self.categoryPath = self.head[a + 16:b]

    # 用于加载请求AJAX并获取json数据的方法
    def getJsonText(self, url):
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except:
            print('获取失败')
            return ''

#获取comments和contents的html源码
def detailInfo(self):
    #调用获取头部参数的函数
    self.get_elements()

    self.comment_url = 'http://product.dangdang.com/index.php?r=comment/list&productId=' \
                       + self.productId + '&categoryPath=' + self.categoryPath + \
                       '&mainProductId=' + self.mainProductId + \
                       '&mediumId=0&pageIndex=1&sortType=1&filterType=1&isSystem=1&tagId=0&tagFilterCount=0&template=publish'

    self.content_url = 'http://product.dangdang.com/index.php?r=callback/detail&productId=' + self.productId \
                       + '&templateType=publish&describeMap=&shopId=0&categoryPath=' + self.categoryPath

    print(requests.get(self.comment_url))
    #判断字符串是否符合json格式

    try:
        json_comments = requests.get(self.comment_url).json()
        json_contents = requests.get(self.content_url).json()
    except:
        return False

    jcomments = json_comments['data']['list']
    try:
        self.goodrate = jcomments['summary']['goodRate']  # 好评率
    except:
        return False

    self.comments_html = jcomments['html']

    jcontents = json_contents['data']
    self.contents_html = jcontents['html']

    contents_html.append(self.contents_html)
    comments_html.append(self.comments_html)
    goodrate.append(self.goodrate)

# 使用requests库封装一个简单的通过get方式获取网页源码的函数
def getsource(url):
    # 利用requests获取网页数据
    html = requests.get(url, headers=headers)
    s = html.text
    return s

def catch(url):
    '''
    global variables:
    list: goodrate
    list: contents_html
    list: comments_html
    :param url:
    :return: None
    '''
    # 获取网页内容
    text = getsource(url)
    # 初始化解析器
    parser = DInfoParser()
    # 将网页内容放入解析器
    parser.feed(text)
    return detailInfo(parser)

def clear():
    contents_html.clear()
    comments_html.clear()
    goodrate.clear()
