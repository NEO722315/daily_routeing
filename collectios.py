import requests
import re
import pprint

class Grab_Jianshu():

    def __init__(self,url,headers):
        self.url = url
        self.headers = headers

    def getHomepage(self):
        resp = requests.get(url=self.url,headers=self.headers)
        return resp.text
        pprint.pprint(resp.text)

    # def target_SepcificStie(self):


    def run(self):
        self.getHomepage()



if __name__ == '__main__':
    j = Grab_Jianshu('https://www.jianshu.com',{'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 80.0.3987.149Safari / 537.36'})
    j.run()



