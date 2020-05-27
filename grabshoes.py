from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

browser = webdriver.Chrome()

target_url = 'https://login.taobao.com/member/login.jhtml?spm=a21bo.2017.754894437.1.5af911d9B3MSbY&f=top&redirectURL=https%3A%2F%2Fwww.taobao.com%2F'

page = browser.get(target_url)

time.sleep(12)

search = browser.find_element_by_xpath("//*[@class='search-combobox-input']")


searchname="Nike官方 NIKE AIR FORCE 1 '07 / PARA?NOISE 男子运动鞋 AQ3692"

search.send_keys(searchname)

time.sleep(5)

searchbutton = browser.find_element_by_xpath("//*[@class='btn-search tb-bg']")
searchbutton.click()

WebDriverWait(browser,10).until(
    EC.presence_of_all_elements_located
)

shoes=browser.find_element_by_xpath("//*[@id='J_Itemlist_Pic_602215118670']")
shoes.click()

windows=browser.window_handles
browser.switch_to.window(windows[-1])

WebDriverWait(browser,10).until(
    EC.presence_of_all_elements_located
)

time.sleep(5)

while(1):
    print("正在进行抢购......")
    if(str(datetime.now())[0:19]=="2019-11-23 11:59:59"):
        browser.refresh()
        WebDriverWait(browser,60).until(
            EC.presence_of_element_located((By.XPATH,"*[@id='J_LinkBuy']"))
        )
        buybutton=browser.find_element_by_xpath("*[@id='J_LinkBuy']")
        buybutton.click()

        WebDriverWait(browser,20).until(
            EC.presence_of_element_located((By.XPATH,"//*[@title='提交订单']"))
        )

        submit=browser.find_element_by_xpath("//*[@title='提交订单']")
        submit.click()
        print("抢购成功！！！！！")

















