
import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import zipfile


#1.操作網頁的查詢功能
driver = webdriver.Chrome()
driver.get('https://www.twse.com.tw/zh/trading/statistics/list05-225.html')
#操作查詢區間的下拉選單
start_year = Select(driver.find_element(By.ID,"label0"))
start_year.select_by_value('2020')
start_season = Select(driver.find_element(By.XPATH,'//*[@id="form"]/div/div/div[1]/span[1]/select[4]'))
start_season.select_by_value('Q1')
end_year = Select(driver.find_element(By.ID,"datePick1"))
end_year.select_by_value('2022')
end_season = Select(driver.find_element(By.XPATH,'//*[@id="form"]/div/div/div[1]/span[2]/select[4]'))
end_season.select_by_value('Q4')
search = driver.find_element(By.CSS_SELECTOR,"button[class='search']")
search.submit()
time.sleep(3)
#2.爬取zip檔案的連結
soup = BeautifulSoup(driver.page_source,'lxml')
# print(soup)
links = soup.find('tbody',{'class':"is-last-page"}).find_all('a')
print(links)
#3.下載zip檔案解壓縮
for index,link in enumerate(links):
    zip_response = requests.get('https://www.twse.com.tw'+link.get('href'))

    if not os.path.exists('zip'):
        os.mkdir('zip')
    #用with陳述式建立檔案並用二進位碼寫入檔案，用format String命名
    with open(f'zip\\{index+1}.zip','wb') as file:
        file.write(zip_response.content)

    # 利用zipfile模組建立壓縮檔物件，傳入已經下載的zip檔案路徑
    zip = zipfile.ZipFile(f'zip\\{index+1}.zip')
    #利用extrall方法解壓縮所有的zip檔案
    zip.extractall('zip\\.')
