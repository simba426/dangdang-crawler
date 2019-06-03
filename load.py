import pymysql

ISBN = []
bookname = []
_class = []
publish = []
original_price = []
dd_price = []
date = []
goodrate = []
img = []
author = []
authorInfo = []
customer = []
comments = []
content = []

def load():
    try:
        conn = pymysql.connect(host='127.0.0.1', port=8889, user='root', passwd='root', db= 'ddbook3', charset='utf8')
        print('link start')
    except:
        print('fail to connect')

    cur = conn.cursor()

    cur.execute('select ISBN from book;')

    rows = cur.fetchall()


    for i in range(len(rows)):
        ISBN.append(''.join(list(rows[i])))

    #获取简要信息
    for element in ISBN:
        cur.execute('select bookname from book where ISBN =' + element + ';')
        rows = cur.fetchall()
        bookname.append(''.join(list(rows[0])))
        cur.execute('select class from book where ISBN =' + element + ';')
        rows = cur.fetchall()
        _class.append(''.join(list(rows[0])))
        cur.execute('select publish from book where ISBN =' + element + ';')
        rows = cur.fetchall()
        publish.append(''.join(list(rows[0])))
        cur.execute('select original_price from book where ISBN =' + element + ';')
        rows = cur.fetchall()
        original_price.append(str(list(rows[0])[0]))
        cur.execute('select dd_price from book where ISBN =' + element + ';')
        rows = cur.fetchall()
        dd_price.append(str(list(rows[0])[0]))
        cur.execute('select date from book where ISBN =' + element + ';')
        rows = cur.fetchall()
        date.append(''.join(list(rows[0])))
        cur.execute('select goodrate from book where ISBN =' + element + ';')
        rows = cur.fetchall()
        goodrate.append(str(list(rows[0])[0]))
        cur.execute('select cover from book where ISBN =' + element + ';')
        rows = cur.fetchall()
        img.append(''.join(list(rows[0])))
        cur.execute('select content from book where ISBN =' + element + ';')
        rows = cur.fetchall()
        content.append(''.join(list(rows[0])))

    #获取作者信息
    for element in ISBN:
        cur.execute('select authorName from author where ISBN =' + element + ';')
        rows = cur.fetchall()
        author.append(''.join(list(rows[0])))
        cur.execute('select authorInfo from author where ISBN =' + element + ';')
        rows = cur.fetchall()
        authorInfo.append(''.join(list(rows[0])))

    #获取评论信息
    for element in ISBN:
        customerone = []
        commentsone = []
        cur.execute('select customerName from comment where ISBN =' + element + ';')
        rows = cur.fetchall()
        for i in range(len(rows)):
            customerone.append(rows[i][0])
        customer.append(customerone)
        cur.execute('select comment from comment where ISBN =' + element + ';')
        rows = cur.fetchall()
        for i in range(len(rows)):
            commentsone.append(rows[i][0])
        comments.append(commentsone)

def get_ISBN():
    return ISBN

def get_booname():
    return bookname

def get_class():
    return _class

def get_publish():
    return publish

def get_original_price():
    return original_price

def get_dd_price():
    return dd_price

def get_date():
    return date

def get_goodrate():
    return goodrate

def get_img():
    return img

def get_author():
    return author

def get_authorInfo():
    return authorInfo

def get_customer():
    return customer

def get_comments():
    return comments

def get_content():
    return content