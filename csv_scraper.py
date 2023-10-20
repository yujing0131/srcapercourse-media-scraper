import requests
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
import time
from datetime import date
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

driver.get('https://www.twse.com.tw/zh/trading/historical/stock-day.html')

#設定月份
months =Select(driver.find_element(By.NAME,"mm"))
select_box = driver.find_element(By.NAME,"mm")
options = [x for x in select_box.find_elements(By.TAG_NAME,"option")]

#輸入股票代碼2330
stock = driver.find_element(By.ID,"label1")
stock.send_keys('2330')

for op in options:
    print(op.get_attribute("value"))
    
data=pd.DataFrame()
#顯示目前系統時間
today = date.today()
for op in options:
    #若選項小於當前月份時間則可以點選，反之則不選
    if int(op.get_attribute("value")) < today.month:
        months.select_by_value(op.get_attribute("value"))

        time.sleep(3)

        #定位送出查詢的位置
        # csv_download = driver.find_element(By.CSS_SELECTOR,"button[class='csv']")
        search = driver.find_element(By.CSS_SELECTOR,"button[class='search']")
        search.submit()
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source,'lxml')
        main_content = soup.find("div" ,{"class":"main-content"})
        table = main_content.find("tbody",{"class":"is-last-page"})
        # print(table)
        rows = table.find_all("tr")
        for index,row in enumerate(rows):
            values = row.find_all("td")
            result = []
            for value in values:
                result.append(value.getText())
            data = pd.concat([data,pd.DataFrame(result)],axis=1)


data = data.T#將data矩陣轉置
data.columns=['日期','成交股數','成交金額','開盤價','最高價','最低價','收盤價','漲跌價差','成交筆數']
print(data)

#若專案裡沒有csv資料夾則建立一個csv的資料夾
if not os.path.exists('csv'):
    os.mkdir('csv')

data.to_csv('csv\\2330.csv',encoding='utf-8-sig',index=False)
