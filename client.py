import requests
import pprint
import re

class Grabing():

    def __init__(self,url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }


    def GetHomepage(self):
        page = requests.get(self.url,headers=self.headers)
        return page.text


    def FindKeywords(self,page):
        model = r'<a class="title" target="_blank" href=".*?">(.*?)</a>'
        results = re.findall(model,page)
        return results


    def main(self):
        page = self.GetHomepage()
        results = self.FindKeywords(page)
        pprint.pprint(results)



s = Grabing('https://www.jianshu.com')
s.main()
