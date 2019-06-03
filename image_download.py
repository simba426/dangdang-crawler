import requests

def save(url, name):
    # 这是一个图片的url
    #url = 'http://img3m0.ddimg.cn/20/24/23898620-1_b_3.jpg'
    response = requests.get(url)
    # 获取的文本实际上是图片的二进制文本
    img = response.content
    # 将他拷贝到本地文件 w 写  b 二进制  wb代表写入二进制文本
    with open( './img/' + str(name) + '.jpg','wb' ) as f:
        f.write(img)
