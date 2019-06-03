# coding: utf-8
import url
import pandas as pd
import brief_info
import catch_package
import detailed_info
import pymysql

def run(keyword, num):

    bookname = []
    author = []
    publish = []
    _class = []
    original_price = []
    dd_price = []
    date = []
    ISBN = []
    goodrate = []
    contents = []
    authorInfo = []
    customers = []
    comments = []
    img = []

    page = (num / 60) + 2
    url_list, img_list = url.get_url_and_img(keyword, int(page))
    for i in range(len(url_list[:num])):
        #抓取简要信息
        brief_info.info(url_list[i])
        #获取各类信息
        catch_bookname = brief_info.get_bookname()
        catch_ISBN = brief_info.get_ISBN()
        catch_author = brief_info.get_author()
        catch_class = brief_info.get_class()
        catch_publish = brief_info.get_publish()
        catch_original_price = brief_info.get_original_price()
        catch_dd_price = brief_info.get_dd_price()
        catch_date = brief_info.get_date()

        if catch_ISBN == 0 or catch_bookname == 0:          #如果这两者为空，抓取错误
            continue
        bookname.append(catch_bookname)                 #书名
        ISBN.append(catch_ISBN)                         #IBSN号
        author.append(catch_author)                     #作者
        _class.append(catch_class)                      #图书分类
        publish.append(catch_publish)                   #出版社
        original_price.append(catch_original_price)     #原价
        dd_price.append(catch_dd_price)                 #当当价
        date.append(catch_date)                         #日期
        print(i, ':', catch_bookname)
        #清空以上列表中的信息
        brief_info.clear()

        #获取好评率以及评论、内容的数据包源码
        if catch_package.catch(url_list[i]) == False:
            if catch_package.contents_html:
                parser = detailed_info.feed(''.join(catch_package.contents_html))
                contents.append(detailed_info.get_contents(parser))
                authorInfo.append(detailed_info.get_authorInfo(parser))
                customer, comment = detailed_info.get_comments(''.join(catch_package.comments_html))
                new_customer = customer.copy()
                new_comment = comment.copy()                #因为函数返回的是列表的地址，在clear之后append的值会消失，所以将值复制给另一个list来防止信息丢失
                customers.append(new_customer)
                comments.append(new_comment)
            else:
                contents.append('该书无内容简介')
                authorInfo.append('作者无简介信息')
                customers.append(['该书暂无人评论'])
                comments.append(['暂无评论'])
            if catch_package.goodrate:
                goodrate.extend(catch_package.goodrate)
            else:
                goodrate.append(0)
        else:
            goodrate.extend(catch_package.goodrate)
            parser = detailed_info.feed(''.join(catch_package.contents_html))
            if detailed_info.get_contents(parser) == '':
                contents.append('该书无内容简介')
            else:
                contents.append(detailed_info.get_contents(parser))
            if detailed_info.get_authorInfo(parser) == '':
                authorInfo.append('作者无简介信息')
            else:
                authorInfo.append(detailed_info.get_authorInfo(parser))

            customer, comment = detailed_info.get_comments(''.join(catch_package.comments_html))
            new_customer = customer.copy()
            new_comment = comment.copy()
            if new_customer:
                customers.append(new_customer)
            else:
                customers.append(['该书暂无人评论'])

            if new_comment:
                comments.append(new_comment)
            else:
                comments.append((['暂无评论']))
            customer.clear()
            comment.clear()
            catch_package.clear()
        img.append(str(img_list[i]))

    inform_dic = {'书名': bookname,
                  '作者': author,
                  '出版社': publish,
                  '分类': _class,
                  '原价': original_price,
                  '当当价': dd_price,
                  '出版日期': date,
                  'ISBN号': ISBN,
                  '好评率': goodrate,
                  '内容简介': contents,
                  '作者信息': authorInfo,
                  '图片链接': img}

    inform_pd = pd.DataFrame(inform_dic)
    inform_pd.to_csv('to.csv', encoding='utf_8_sig')


    try:
        conn = pymysql.connect(host='127.0.0.1', port=8889, user='root', passwd='root', db= 'ddbook3', charset='utf8')
    except:
        print('fail to connect')
        return

    cur = conn.cursor()

    #首先清空数据库中信息
    cur.execute('delete from book;')
    cur.execute('delete from author;')
    cur.execute('delete from comment;')

    for i in range(len(bookname)):
        list = []
        try:
            list.insert(0,ISBN[i])
            list.insert(1,bookname[i])
            list.insert(2,publish[i])
            list.insert(3,date[i])
            list.insert(4,_class[i])
            list.insert(5,original_price[i])
            list.insert(6,dd_price[i])
            list.insert(7,goodrate[i])
            list.insert(8,img[i])
            list.insert(9,contents[i])
        except:
            continue
        new_list = list.copy()
        try:
            dbcommand_book = 'insert ignore into book values ('
            for element in new_list:
                dbcommand_book = dbcommand_book + '\'' + str(element) + '\'' + ','
            dbcommand_book = dbcommand_book[:-1] + ');'
            cur.execute(dbcommand_book)
        except:
            print('No:',i,' data lost')

        list2 = []
        try:
            list2.insert(0,ISBN[i])
            list2.insert(1,author[i])
            list2.insert(2,authorInfo[i].replace('\n',''))
        except:
            continue
        new_list2 = list2.copy()
        try:
            dbcommand_book2 = 'insert ignore into author values ('
            for element in new_list2:
                dbcommand_book2 = dbcommand_book2 + '\'' + str(element) + '\'' + ','
            dbcommand_book2 = dbcommand_book2[:-1] + ');'
            cur.execute(dbcommand_book2)
        except:
            print('No:', i, ' data lost')

        lcustomers = customers[i]
        lcomments = comments[i]
        for j in range(len(lcustomers)):
            try:
                dbcommand_comment = 'insert ignore into comment values ('
                dbcommand_comment = dbcommand_comment + '\'' + new_list[0] + '\',' + '\'' + str(j) + '\',' + '\'' + lcustomers[j] + '\',' + '\'' + lcomments[j] + '\'' + ','
                dbcommand_comment = dbcommand_comment[:-1] + ');'
                cur.execute(dbcommand_comment)
            except:
                continue
        list.clear()
        list2.clear()

    conn.commit() #提交事务
    cur.close()
    conn.close()
