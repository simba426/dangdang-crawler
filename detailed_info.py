from html.parser import HTMLParser

# 设置http请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.933.400 QQBrowser/9.4.8699.400',
}

class contentParser(HTMLParser):
    content_flg = False
    authorInfo_flg = False
    cdescrip_flg = False
    adescrip_flg = False
    contents = ''
    authorInfo = ''
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for name, value in attrs:
                if name == 'id' and value == 'content':
                    self.content_flg = True
                if name == 'id' and value == 'authorIntroduction':
                    self.authorInfo_flg = True

        if tag == 'div':
            for name, value in attrs:
                if name == 'class' and value == 'descrip' and self.content_flg == True:
                    self.cdescrip_flg = True
                if name == 'class' and value == 'descrip' and self.authorInfo_flg == True:
                    self.adescrip_flg = True

    def handle_data(self, data):
        if (self.lasttag == 'span' or self.lasttag == 'br' or self.lasttag == 'p' ) and self.cdescrip_flg == True:
            self.contents += data
        if (self.lasttag == 'span' or self.lasttag == 'br' or self.lasttag == 'p' ) and self.adescrip_flg == True:
            self.authorInfo += data

    def handle_endtag(self, tag):
        if tag == 'div' and self.cdescrip_flg == True:
            self.content_flg = False
            self.cdescrip_flg = False
        if tag == 'div' and self.adescrip_flg == True:
            self.authorInfo_flg = False
            self.adescrip_flg = False


class commentParser(HTMLParser):
    comment_flg = False
    customer_flg = False
    comments = []
    customers = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'target' and value == '_blank':
                    self.comment_flg = True

        if tag == 'span':
            for name, value in attrs:
                if name == 'class' and value == 'name':
                    self.customer_flg = True


    def handle_data(self, data):
        if self.lasttag == 'a' and self.comment_flg == True:
            self.comments.append(data)
            self.comment_flg = False

        if self.lasttag == 'span' and self.customer_flg == True:
            self.customers.append(data)
            self.customer_flg = False

    def handle_endtag(self, tag):
        if tag == 'a':
            self.comment_flg = False

def feed(contents_html):
    content_parser = contentParser()
    content_parser.feed(contents_html)
    return content_parser

def get_contents(content_parser):
    #获取内容简介
    return content_parser.contents.strip()

def get_authorInfo(content_parser):
    # 获取内容简介
    return content_parser.authorInfo.strip()

def get_comments(comments_html):
    '''
    :param comments_html:
    :return: list: customers, comments
    '''
    #获取评论
    comment_parser = commentParser()
    comment_parser.feed(comments_html)
    return comment_parser.customers, comment_parser.comments