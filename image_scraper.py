from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
from bs4 import BeautifulSoup
import os #利用此套件建立資料存放爬取的圖片

#圖片類型的網站大部分都會黨網頁爬蟲，若用靜態網頁爬取圖片連結無法爬取，建議搭配selenium套件實際打開連覽器網頁發送請求，再利用beautifulsoup爬取圖片


#1.利用selenium特見操作網頁
driver = webdriver.Chrome()
driver.get('https://pixabay.com/images/search/car/')
#設定滑鼠滾動10次
for i in range(2):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(5) #每次滾動卷軸等待5秒


#2.利用Beautifulsoup套件爬取網頁圖片的連結
soup = BeautifulSoup(driver.page_source,'lxml')
images = soup.find_all("a",{"class":"imageLink--NPmzb"})#先訂位到<a>標籤再定位置底下的圖片<img>元素
images1 = soup.find_all("a",{"class":"link--WHWzm"})
images_links = [image.find("img").get("src")  for image in images]
images_links1 = [image.find("img").get("src")  for image in images1]
# print(images_links1)
#3.下載圖片
for index,link in enumerate(images_links):#利用enumerate函式取得圖片的index來命名
    #若專案裡面沒有image的資料夾則進行建立
    if not os.path.exists("image"):
        os.mkdir('image')
    #利用request模組發送請求到圖片連結進行下載
    img = requests.get(link)
    #將回應的二進位碼寫到檔案才完成下載，使用with陳述建立檔案物件
    with open(f"image\\{index+1}.jpg",'wb') as file:#用formatString語法打開image資料夾並命名下載的圖片檔名，wb即為二進位碼
        file.write(img.content)#將下載圖片的二進位碼寫入完成後with陳述式會自動關閉資料夾

for index,link in enumerate(images_links1):#利用enumerate函式取得圖片的index來命名
    #若專案裡面沒有image的資料夾則進行建立
    if not os.path.exists("image"):
        os.mkdir('image')
    #利用request模組發送請求到圖片連結進行下載
    if link!='/static/img/blank.gif':
        img = requests.get(link)
        #將回應的二進位碼寫到檔案才完成下載，使用with陳述建立檔案物件
        with open(f"image\\{index+1.1}.jpg",'wb') as file:#用formatString語法打開image資料夾並命名下載的圖片檔名，wb即為二進位碼
            file.write(img.content)#將下載圖片的二進位碼寫入完成後with陳述式會自動關閉資料夾