from Cryptodome.Cipher import AES
from Cryptodome import Random
import binascii
import requests
import re
from lxml import etree

class MyAES(object):

    def __init__(self,key,iv=None,mode=AES.MODE_CFB):
        self.key=key
        self.mode=mode
        if iv:
            self.iv = iv
        else:
            self.iv = Random.new().read(AES.block_size)


    def encrypt(self,data):
        if not isinstance(data,bytes):
            data = data.encode()
        aes_encrypter = AES.new(self.key,self.mode,self.iv)
        result = aes_encrypter.encrypt(data)
        return binascii.b2a_hex(result)


    def decrtper(self,data):
        if isinstance(data,bytes):
            data = data.decode()
            data = binascii.a2b_hex(data)
        aes_decrpter = AES.new(self.key,self.mode,self.iv)
        result = aes_decrpter.decrypt(data).decode()
        return result


class JianshuHomePage():

    def __init__(self,url):
        self.url = url
        self.ua = {
            'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 72.0.3626.96Safari / 537.36'
        }
        self.articles = []
        self.token = None
        self.note_id = []


    def get_homepage(self):
        resp = requests.get(self.url,headers=self.ua).text
        self.token = re.findall(r'<meta name="csrf-token" content="(.*?)" />',resp)[0]
        self.parse(resp)


    def get_ajax(self,page):
        headers = {
            'x-csrf-token': self.token,
            'x-requested-with': 'XMLHttpRequest'
        }

        if page <= 3:
            headers['x-infinitescroll'] = 'true'
        else:
            headers['x-pjax'] = 'true'


        headers.update(self.ua)
        params = {
            'seen_snote_ids[]':self.note_id,
            'page':page
        }
        resp = requests.get(self.url,headers=headers,params=params).text
        self.parse(resp)


    def parse(self,resp):
        page = etree.HTML(resp)
        title = page.xpath('//div[@class="content"]/a/text()')
        passage = page.xpath('//div[@class="content"]/p/text()')
        self.articles.extend(zip(title, passage))
        note_id = page.xpath('//li[@class="have-img"]/@data_note_id/text()')
        self.note_id.extend(note_id)

    def run(self):
        self.get_homepage()
        for i in range(2,4):
            self.get_ajax(i)
        for i in self.articles:
            print(i)



if __name__ == '__main__':
    key = b'aaaabbbbccccdddd'
    data = 'ASD是什么意思_ASD在线翻译、解释、发音、同义词、反义词_英语...'
    j = MyAES(key)
    result = j.encrypt(data)
    print(result)
    x = JianshuHomePage('https://www.jianshu.com')
    x.run()















