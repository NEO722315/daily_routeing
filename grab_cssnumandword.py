"""Grab the phone numbers from 大众点评"""
import re
import requests
import lxml.html
from lxml import etree


css_url ='http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/29e76c3da845ca8b35251e24d615703a.css'
# 文字位置坐标的url
headers ={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate'

}
next_url = 'http://www.dianping.com/nanjing/ch35/g33831p2'
session = requests.session()



def get_css_number(represent):      # represent为e标签的class属性值
    resp =session.get(css_url,headers=headers)
    # 获取css位置标准参数
    element = r'%s{background:-(\d+).0px -(\d+).0px;}'% represent
    # 获取数字对象的横纵坐标
    complie = re.compile(element)
    result = complie.findall(resp.text)[0]
    a,b,c,d = get_posiotion_informat()  # 调用获取数字css页面的数字
    num = get_number(a,b,c,d,result)
    return num


def get_posiotion_informat():
    resp = session.get('http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/2416ff021a8fccb10b15e20ca8d5711c.svg',headers=headers)
    # 获取数字页面的源码
    text = lxml.html.fromstring(resp.content)
    # 分别生成四行数字，以纵坐标作为区分标准
    a = text.xpath('//text[@y="36"]/text()')[0]
    b = text.xpath('//text[@y="78"]/text()')[0]
    c = text.xpath('//text[@y="127"]/text()')[0]
    d = text.xpath('//text[@y="172"]/text()')[0]
    return a,b,c,d


def get_number(a,b,c,d,result):
    x,y = result
    x,y = int(x),int(y)
    # 每个数字在页面中的位置的间距是14px，以\s和汉字作为一个单元，长度为14px
    if y<=36:
        number = a[x//14]       # 整除横坐标，获取索引值
    elif y<=72:
        number = b[x//14]
    elif y<=127:
        number = c[x//14]
    else:
        number = d[x//14]

    return number


def get_css_word(represent):            # 获取汉字
    resp = session.get(css_url,headers=headers)
    # 获取位置坐标页面
    element  = r'%s{background:-(\d+).0px -(\d+).0px;}' % represent
    # 获取对象的横纵坐标像素
    compile = re.compile(element)
    result = compile.findall(resp.text)[0]
    # 将横纵坐标数值作为单个元组进行传递
    word = get_word_position(result)
    return word


def get_word_position(result):
    resp = session.get('http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/91820d40a4345b469d0eeff70a6bec93.svg',headers=headers)
    # 获取汉字图像页面
    x,y = result
    x,y = int(x),int(y)
    y += 23         # 每一行的纵坐标都是文字上方 path标签 中的 d属性 中间数值减去 23
    x //= 14        # 每个汉字之间的间距为14px，整除获取索引值
    element = '<path id="(\d)" d="M0 %d H600"/>' % y
    compile = re.compile(element)
    y_position = compile.findall(resp.text)[0]
    # 获取id数值，通过id值在textpath标签中进行提取标签内文字
    a = get_words(y_position,resp)
    return a[x] # 输出汉字


def get_words(num,resp):
    element = r'<textPath xlink:href="#%s" textLength="\d+">(.*?)</textPath>' % num
    compile = re.compile(element)
    a = compile.findall(resp.text)[0]
    # 通过id数值获取textpath标签中的内容
    return a


def verify_choose(element):         # 通过输入对象的首字母判断获取汉字 or 数字 ，并调用不同的方法
    if element[0] == 'e':
        return get_css_number(element)
    elif element[0] == 's':
        return  get_css_word(element)




def grab_address(url):
    resp = session.get(url,headers=headers)        # 对页面进行请求
    address_result = re.findall(r'<span class="item" itemprop="street-address" id="address">(.*?)</span>',resp.text,re.S)[0]
    # 获取景点地址加密部分
    phone_number_result = re.findall(r'<p class="expand-info tel"> <span class="info-name">电话：</span>(.*?)</p>',resp.text,re.S)[0]
    # 获取电话加密部分
    money_result = re.findall(r'<span id="avgPriceTitle" class="item">(.*?)</span>',resp.text,re.S)[0]
    # 获取景点门票费用加密部分

    # 对获取的数据进行清洗与解密
    str = wash_data(address_result)
    num = wash_data(phone_number_result)
    money = wash_data(money_result)
    print("地址："+str)
    print("电话："+num)
    print(money)


def wash_data(result):                              # 对于数据进行清洗，提取字母与数字部分，去除标签及属性名
    result2 = result.replace('<e class=', '')
    result3 = result2.replace('></e>', '')
    result4 = result3.replace('<d class=', '')
    result5 = result4.replace('></d>', '')
    result6 = result5.replace('\n', '')
    result7 = result6.replace('\"\"',',')
    result8 = result7.replace('\"',',')
    result8 = result8.split(',')            # 对数据进行通过都好进行分割处理，并添加在列表中
    str =  decrypt(result8)
    print(str)# 对数据进行解码
    return str


def decrypt(result):
    str = ' '
    for i in result:
        if len(i) == 5:                # 当数据长度为五时，为加密部分
             str += verify_choose(i)
        else:
             str += i                   # 其他则是汉字部分，直接进行字符串拼接
    return str


def grab_cyclelly():
    for i in range(1,51):
        url = 'http://www.dianping.com/nanjing/ch35/g33831p%s' % str(i)
        resp = session.get(url,headers=headers)
        print(resp.text)
        print(resp.url)
        element = r'\t<a onclick="LXAnalytics(\'moduleClick\', \'shoppic\')" target="_blank" href="(.*?)" data-click-name="shop_img_click" data-shopid=".*?" rel="nofollow" title=""  >\n'
        compile = re.compile(element)
        result = compile.findall(resp.text,re.S)
        print(result)
        exit()
        get_view_message(result)


def get_view_message(result):
    for url in result:
        print(url)
        grab_address(url)


grab_cyclelly()













