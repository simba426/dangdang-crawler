#!/usr/bin/python
# -*- coding: UTF-8 -*-
from tkinter import *  # 导入 Tkinter 库
from PIL import Image, ImageTk
import image_download
import load
import main
import os

class GUI():
    i = 0
    len = 0
    keyword = ''
    number = ''
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
    comment = []
    content = []
    downloaded = True

    def clear(self):
        self.ISBN.clear()
        self.bookname.clear()
        self._class.clear()
        self.publish.clear()
        self.original_price.clear()
        self.dd_price.clear()
        self.date.clear()
        self.goodrate.clear()
        self.img.clear()
        self.author.clear()
        self.authorInfo.clear()
        self.customer.clear()
        self.comment.clear()
        self.content.clear()

    def run(self):
        root = Tk()  # 创建窗口对象的背景色
        root.title('当当网图书信息检索')
        root.geometry('750x700')
        text1 = StringVar()
        text2 = StringVar()
        text3 = StringVar()
        text4 = StringVar()
        text5 = StringVar()
        text6 = StringVar()
        text7 = StringVar()
        text8 = StringVar()
        text9 = StringVar()
        #root.resizable(width=False, height=False)

        '''为组件定义事件'''

        # 获取关键字和数值
        def get():
            self.clear()
            self.keyword = keywordEntry.get()
            self.number = numberEntry.get()
            #删除原来的图片文件
            try:
                for i in range(self.len):
                    os.remove('./img/' + str(i) + '.jpg')
            except:
                print('No img')
            main.run(self.keyword, int(self.number))

        def change():
            text1.set(self.bookname[self.i])
            text2.set(self.author[self.i])
            text3.set(self.publish[self.i])
            text4.set(self.date[self.i])
            text5.set(self.original_price[self.i])
            text6.set(self.dd_price[self.i])
            text7.set(self.ISBN[self.i])
            text8.set(self._class[self.i])
            text9.set(self.goodrate[self.i])
            img_open = Image.open('./img/' + str(self.i) + '.jpg')
            img_png = ImageTk.PhotoImage(img_open)
            img_label.configure(image=img_png)
            img_label.image = img_png
            #插入书本简介
            contentText.delete('1.0', '7999.0')
            contentText.insert(INSERT, self.content[self.i])
            #插入作者简介
            authorText.delete('1.0', '7999.0')
            authorText.insert(INSERT, self.authorInfo[self.i])
            #插入评论
            commentText.delete('1.0', '7999.0')
            for j in range(len(self.customer[self.i])):
                cmt = self.customer[self.i][j] + ':' + self.comment[self.i][j] + '\n'
                commentText.insert(INSERT, cmt)


        # 从数据库获取信息
        def init():
            #初始化参数
            self.clear()
            self.downloaded = True
            self.i = 0
            self.len = 0

            load.load()
            self.ISBN = load.get_ISBN()
            self.bookname = load.get_booname()
            self._class = load.get_class()
            self.publish = load.get_publish()
            self.original_price = load.get_original_price()
            self.dd_price = load.get_dd_price()
            self.date = load.get_date()
            self.goodrate = load.get_goodrate()
            self.img = load.get_img()
            self.author = load.get_author()
            self.authorInfo = load.get_authorInfo()
            self.customer = load.get_customer()
            self.comment = load.get_comments()
            self.content = load.get_content()
            self.len = len(self.ISBN)
            #print(len(self.ISBN))
            if self.downloaded:
                for i in range(self.len):
                    image_download.save(self.img[i], i)
                self.downloaded = False
            change()

        #查看下一本书
        def up():
            self.i = self.i + 1
            if self.i >= self.len:
                self.i = self.len - 1
            change()

        #查看上一本书
        def down():
            self.i = self.i - 1
            if self.i < 0:
                self.i = 0
            change()


        Mainframe0 = Frame(root, width=500, height=80)
        Mainframe1 = Frame(root, width=500, height=80)
        Mainframe2 = Frame(root, width=500, height=250)
        Mainframe3 = Frame(root, width=500, height=600)
        Mainframe4 = Frame(root, width=500, height=80)

        #Mainframe0内容
        Label(Mainframe0, text='关键字:').pack(side=LEFT)
        keywordEntry = Entry(Mainframe0)
        keywordEntry.pack(side=LEFT)
        Label(Mainframe0, text='数量:').pack(side=LEFT)
        numberEntry = Entry(Mainframe0)
        numberEntry.pack(side=LEFT)
        #Button(Mainframe0, text=' 提交 ', command=get_keyword_and_number).pack(side=LEFT)
        Button(Mainframe0, text=' 提交 ', command=get).pack(side=LEFT)

        #Mainframe1内容
        Label(Mainframe1, text='******************************************************************************', font=('Arial', 15)).grid(row=1)
        Label(Mainframe1, text='图书信息', font=('Arial', 15)).grid(row=2)

        #Mainframe2内容
        Subframe21 = Frame(Mainframe2, height=250, width=180)
        Subframe22 = Frame(Mainframe2, height=250, width=300)
        Subframe221 = Frame(Subframe22)
        Subframe222 = Frame(Subframe22)
        img_open = Image.open('./img/empty.png')
        img_png = ImageTk.PhotoImage(img_open)
        img_label = Label(Subframe21, image=img_png)
        img_label.pack()
        Label(Subframe221, text='书名:', font=('Arial', 10)).grid(row=1)
        Label(Subframe221, text='作者:', font=('Arial', 10)).grid(row=2)
        Label(Subframe221, text='出版社:', font=('Arial', 10)).grid(row=3)
        Label(Subframe221, text='出版日期:', font=('Arial', 10)).grid(row=4)
        Label(Subframe221, text='原价:', font=('Arial', 10)).grid(row=5)
        Label(Subframe221, text='当当价:', font=('Arial', 10)).grid(row=6)
        Label(Subframe221, text='ISBN号:', font=('Arial', 10)).grid(row=7)
        Label(Subframe221, text='图书分类:', font=('Arial', 10)).grid(row=8)
        Label(Subframe221, text='好评率:', font=('Arial', 10)).grid(row=9)

        Label(Subframe222, textvariable=text1, font=('Arial', 10)).grid(row=1)
        Label(Subframe222, textvariable=text2, font=('Arial', 10)).grid(row=2)
        Label(Subframe222, textvariable=text3, font=('Arial', 10)).grid(row=3)
        Label(Subframe222, textvariable=text4, font=('Arial', 10)).grid(row=4)
        Label(Subframe222, textvariable=text5, font=('Arial', 10)).grid(row=5)
        Label(Subframe222, textvariable=text6, font=('Arial', 10)).grid(row=6)
        Label(Subframe222, textvariable=text7, font=('Arial', 10)).grid(row=7)
        Label(Subframe222, textvariable=text8, font=('Arial', 10)).grid(row=8)
        Label(Subframe222, textvariable=text9, font=('Arial', 10)).grid(row=9)

        # Mainframe3内容
        Label(Mainframe3, text='内容简介\n', font=('Arial', 15)).grid(row=1)
        contentText = Text(Mainframe3, height=4)
        contentText.grid(row=2)
        Label(Mainframe3, text='作者简介\n', font=('Arial', 15)).grid(row=4)
        authorText = Text(Mainframe3, height=4)
        authorText.grid(row=5)
        Label(Mainframe3, text='评论\n', font=('Arial', 15)).grid(row=7)
        commentText = Text(Mainframe3, height=4)
        commentText.grid(row=8)
        #用于制造空行的Label
        Label(Mainframe3, text='\n').grid(row=9)

        # Mainframe4内容
        Button(Mainframe4, text=' 上一本 ', command=down).pack(side=LEFT)
        Label(Mainframe4, text='\t\t').pack(side=LEFT)
        Button(Mainframe4, text=' 刷新 ', command=init).pack(side=LEFT)
        Label(Mainframe4, text='\t\t').pack(side=LEFT)
        Button(Mainframe4, text=' 下一本 ', command=up).pack(side=RIGHT)

        Subframe21.pack(side=LEFT)
        Subframe22.pack(side=RIGHT)
        Subframe221.pack(side=LEFT)
        Subframe222.pack(side=RIGHT)
        Mainframe0.pack()
        Mainframe1.pack()
        Mainframe2.pack()
        Mainframe3.pack()
        Mainframe4.pack()

        root.mainloop()

GUI = GUI()
GUI.run()
