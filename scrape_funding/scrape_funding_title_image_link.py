#下載募資平台資料(標題、圖片網址、連結)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json,re
import time
import random
# --- 參數設定 ---
domain = 'https://www.zeczec.com/'
pages = 1           # 總頁數
output_file = 'data.json'

# Selenium 選項（headless + 隱藏自動化特徵）
opts = Options()
opts.add_argument('--headless=new') #讓 Chrome 在沒有視窗介面的情況下執行。
opts.add_argument('--disable-blink-features=AutomationControlled') #關閉瀏覽器自動化標記，減少被反爬機制偵測的可能性。
opts.add_argument('--incognito')
# 加上常見瀏覽器標頭
opts.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/94.0.4606.61 Safari/537.36 Edg/94.0.992.31')

driver = webdriver.Chrome(options=opts)
results = []
# --- 抓首頁列表函式 ---
def getMainData():
    
    for p in range(1, pages + 1):
        url = f'{domain}categories?page={p}'
        driver.get(url)
        time.sleep(2)   # 等待 JS、圖片 lazy load
        
        soup = BeautifulSoup(driver.page_source, 'lxml')
        for a in soup.select('div[class="flex lg:-mx-4"] a.inline-block'):
        #for a in soup.select('div.flex.lg\\:-mx-4 a.inline-block'):
            # 圖片 URL
            img = a.find('img')
            cover = img.get('data-src') or img.get('src')
            regexImg = r"https:\/\/assets.zeczec.com\/asset_\d+_image_big.(jpe?g|png)"
            matchImg =re.match(regexImg,cover) 
            strImg = matchImg[0]
            
                     
            
            
            # 專案連結（補上 domain）
            #link = urljoin(domain, a['href'])
            link = domain + a['href']
            
            # 標題文字
            #title = a.find('h3').get_text(strip=True)
            title = a.select_one('h3').get_text(strip=True)
            
            results.append({
                'cover': strImg,
                'link': link,
                'title': title
            })
    return results


        



# --- 存成 JSON ---
def saveJson(data):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)  #設定成 False，則能保留原本字元，讓輸出檔案裡直接看到中文。
    print(f'已寫入 {output_file}，共 {len(data)} 筆資料') #：設定縮排層級為 4 個空格

# --- 主程式 ---
if __name__ == '__main__':
    try:
        data = getMainData()
        saveJson(data)
    except Exception as e:
        # 你可以這裡做更進一步的錯誤紀錄或重試機制
        print(f'執行過程發生錯誤：{e}')
    finally:
        driver.quit()
