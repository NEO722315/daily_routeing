import requests
import base64
import json
import re
import rsa
import time
import binascii
from lxml import etree



class WeiboAcess(object):

    def __init__(self,url,username,password):
        self.url = url
        self.pw = password
        self.un = self.username_encrypter(username)
        self.session = requests.session()
        self.headers = {
            'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 72.0.3626.121Safari / 537.36'
        }
        self.result = None
        self.key_words = '我的首页'


    def username_encrypter(self,username):
        result = base64.b64encode(username.encode())
        return result


    def password_processor(self):
        password = (str(self.result['servertime'])+'\t'+self.result['nonce']+'\n')+self.pw
        rsa_key = self.rsakey_produce()
        self.pw = binascii.b2a_hex(rsa.encrypt(password.encode(),rsa_key)).decode()


    def rsakey_produce(self):
        rsa_key = rsa.PublicKey(int(self.result['pubkey'],16),int('10001',16))
        return rsa_key


    def pre_login(self):
        url = 'https://login.sina.com.cn/sso/prelogin.php'
        params={
        'entry':'weibo',
        'callback':'sinaSSOController.preloginCallBack',
        'su':'',
        'rsakt':'mod',
        'client':'ssologin.js(v1.4.19)',
        '_': '1552182809745'
        }
        resp = self.session.get(url,headers=self.headers,params=params,verify=False)
        self.result = json.loads(re.findall(r'preloginCallBack\((.*?)\)',resp.text)[0])


    def login(self):
        url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
        data = {
        'entry':'weibo',
        'gateway':'1',
        'from':'',
        'savestate':'7',
        'qrcode_flag':'false',
        'useticket':'1',
        'pagerefer':'' ,
        'vsnf':	'1',
        'su':self.un,
        'service':'miniblog',
        'servertime':round(time.time()*1000),
        'nonce':self.result['nonce'],
        'pwencode':'rsa2',
        'rsakv':'1330428213',
        'sp':self.pw,
        'sr':'1600*900',
        'encoding':'UTF-8',
        'prelt':'118',
        'url':'https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype':'META'
        }
        resp = self.session.post(url,headers=self.headers,data=data,verify=False)
        next_url = re.findall(r'url=&#39;(.*?)&#39;"/>',resp.text)[0]
        resp2 = self.session.get(next_url,headers=self.headers,verify=False)
        return resp2


    def login_userhomepage(self):
        resp2 = self.login()
        link_urls = re.findall(r'"arrURL":\["(.*?)","(.*?)","(.*?)","(.*?)"\]',resp2.text)[0]
        for new_url in link_urls:
            new_url=new_url.replace('\\', '')
            self.session.get(new_url,headers=self.headers,verify=False)


    def verify(self):
        url = 'https://weibo.com/u/6499906882/home'
        resp = self.session.get(url,headers=self.headers,verify=False)
        page = etree.HTML(resp.text)
        result = page.xpath('//title[1]/text()')[0]
        if self.key_words in result:
            print('login successfully')
        else:
            print('login failed')


    def run(self):
        self.pre_login()
        self.password_processor()
        self.login_userhomepage()
        self.verify()


if __name__ =='__main__':
    j=WeiboAcess('https://weibo.com','18130443356','CZQ19990722')
    j.run()

