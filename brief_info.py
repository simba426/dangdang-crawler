from html.parser import HTMLParser
import requests
import re
# 设置http请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.933.400 QQBrowser/9.4.8699.400',
}

bookname = []
author = []
_class = []
publish = []
original_price = []
dd_price = []
date = []
ISBN = []


class BInfoParser(HTMLParser):
    # 判断是否进入所要找的tag所用的flag
    span_oprice = False
    span_dprice = False
    author_flg = False
    span_flg = False
    publish_flg = False
    dd_price_flg = False
    original_price_flg = False
    date_flg = False
    _class_flg = False
    # 存储作者的字符串
    author = ''
    # 存储分类的字符串
    _class = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'h1':
            for name, value in attrs:
                if name == 'title':
                    bookname.append(value)

        if tag == 'a':
            for name, value in attrs:
                if name == 'dd_name' and value == '出版社':
                    self.publish_flg = True

        if tag == 'span':
            for name, value in attrs:
                if name == 'class' and value == 't1':
                    self.date_flg = True
                if name == 'id' and value == 'author':
                    self.span_flg = True
                if name == 'dd_name' and value == '作者':
                    self.author_flg = True

        if tag == 'div':
            for name, value in attrs:
                if name == 'class' and value == 'section':
                    self.content_flg = True
                if name == 'id' and value == 'original-price':
                    self.original_price_flg = True

        if tag == 'p':
            for name, value in attrs:
                if name == 'id' and value == 'dd-price':
                    self.dd_price_flg = True

        if tag == 'li':
            for name, value in attrs:
                if name == 'dd_name' and value == '详情所属分类':
                    self._class_flg = True

    def handle_data(self, data):
        if self.lasttag == 'a' :
            if self.publish_flg == True:
                publish.append(data)
                self.publish_flg = False

        if (self.lasttag == 'span' or self.lasttag == 'a' or self.lasttag == 'p' ) and self.author_flg == True:
            self.author += data

        if (self.lasttag == 'span' or self.lasttag == 'li' or self.lasttag == 'a') and self._class_flg == True:
            self._class += data

        if self.span_dprice == True:
            dd_price.append(data.strip())
            self.dd_price_flg = False
            self.span_dprice = False

        if self.span_oprice == True:
            original_price.append(data.strip())
            self.original_price_flg = False
            self.span_oprice = False

        if self.lasttag == 'span':
            if self.date_flg == True and re.search(r'\d+[\u4e00-\u9fa5]\d+[\u4e00-\u9fa5]', data) != None:
                a = re.search(r'\d+[\u4e00-\u9fa5]\d+[\u4e00-\u9fa5]', data).span()[0]
                b = re.search(r'\d+[\u4e00-\u9fa5]\d+[\u4e00-\u9fa5]', data).span()[1]
                date.append(data[a:b])
                self.date_flg = False

        if self.lasttag == 'li' and re.search(r'(ISBN)\：\d+', data) != None:
            a = re.search(r'(ISBN)\：\d+', data).span()[0]
            b = re.search(r'(ISBN)\：\d+', data).span()[1]
            ISBN.append(data[a+5:b])

    def handle_endtag(self, tag):
        #解析嵌套的价格属性用到的标记
        if tag == 'span':
            if self.dd_price_flg == True:
                self.span_dprice = True
            if self.original_price_flg == True:
                self.span_oprice = True
            if self.span_flg == True:
                self.author_flg = False
        if tag == 'li' and self._class_flg == True:
            self._class_flg = False


# 使用requests库封装一个简单的通过get方式获取网页源码的函数
def getsource(url):
    # 利用requests获取网页数据
    html = requests.get(url, headers=headers)
    s = html.text
    return s

def info(url):
    '''
    :param url:
    :return:empty
    '''
    # 获取网页内容
    text = getsource(url)
    # 初始化解析器
    parser = BInfoParser()
    # 将网页内容放入解析器
    parser.feed(text)
    author.append(parser.author[3:].strip())
    _class.append(parser._class.strip())

def get_ISBN():
    if ISBN:
        return ''.join(ISBN)
    else:
        return 0

def get_bookname():
    if bookname:
        return ''.join(bookname)
    else:
        return 0

def get_author():
    if author:
        return ''.join(author)
    else:
        return '作者未知'

def get_publish():
    if publish:
        return ''.join(publish)
    else:
        return '未知出版社'

def get_original_price():
    if original_price:
        return ''.join(original_price)
    else:
        return '0'

def get_dd_price():
    if dd_price:
        return ''.join(dd_price)
    else:
        return '0'

def get_date():
    if date:
        return ''.join(date)
    else:
        return '2018年06月'

def get_class():
    if _class:
        return ''.join(_class)
    else:
        return '暂无分类'

#清空所有列表信息
def clear():
    bookname.clear()
    author.clear()
    _class.clear()
    publish.clear()
    original_price.clear()
    dd_price.clear()
    date.clear()
    ISBN.clear()

