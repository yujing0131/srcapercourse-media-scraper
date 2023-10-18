#不需要操作網頁，只需要下載m3u8檔案ts檔案
import requests
import os
import glob #合併ts檔案時需要取得名稱

#1.下載m3u8檔案
response = requests.get('https://edgecast-cf-prod.yahoo.net/cp-video-transcode/production/4053cabc-8a9b-3b88-9002-357db5cdebfb/2023-10-13/03-00-58/3fa816b6-765d-5c50-a635-0d55be7d43a8/stream_1280x720x935_v2.m3u8')
#若專案裡面沒有video的資料夾則進行建立
if not os.path.exists("video"):
    os.mkdir('video')

with open('video\\trailer.m3u8','wb') as file:
    file.write(response.content)
ts_url_list = []
##建立trailer.m3u8的二進位碼模式檔案 
#2.下載ts檔案
with open("video\\trailer.m3u8", 'r',encoding='utf-8') as file:
    contents = file.readlines()
    #用一個變數儲存ts網址
    base_url = "https://edgecast-cf-prod.yahoo.net/cp-video-transcode/production/4053cabc-8a9b-3b88-9002-357db5cdebfb/2023-10-13/03-00-58/3fa816b6-765d-5c50-a635-0d55be7d43a8/" 
    #用for迴圈讀取m3u8檔案內每一行內容，判斷每一行的結尾是否為.ts
    for content in contents:
        if content.endswith('ts\n'):#若結尾是ts換行，則該ts檔案網址就是base_url+檔案名稱，但需要將換行符號移除
            ts_url = base_url+ content.replace('\n',' ')
            #將ts檔案打包成一格串列
            ts_url_list.append(ts_url)

#用for迴圈讀取每一個ts網址，依序發送每一個請求到ts檔案網址
for index, url in enumerate(ts_url_list):
    ts_response = requests.get(url)
    #利用with陳述式建立檔案物件
    with open(f"video\\{index+1}.ts",'wb') as file:#寫入二進位碼模式
        file.write(ts_response.content)

#3.合併ts檔案
#利用glob模組取得video資料夾所有ts檔案名稱
ts_files = glob.glob('video\\*.ts')
with open('video\\trailer.mp4','wb') as file: #建立一個trailer.mp4的二進位模式檔案
    #用for迴圈讀取所有ts檔名
    for ts_file in ts_files:
        #依序讀取每一個ts檔案且為二進位碼模式下讀取出來
        file.write(open(ts_file,'rb').read())
