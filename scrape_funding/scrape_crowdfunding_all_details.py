import json
import time
import random
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

#下載募資平台資料(標題、圖片網址、連結、目標 / 過去集資、 贊助人數  、剩餘天數 、 專案期間起訖)


DOMAIN        = 'https://www.zeczec.com/'
PAGES         = 1
OUTPUT_FILE   = 'data.json'
SLEEP_ON_ERROR= 180
SLEEP_BETWEEN = 60

def init_driver():
    """初始化一個隱身且偽裝過的 Chrome driver"""
    opts = Options()
    opts.add_argument('--headless=new')
    opts.add_argument('--disable-blink-features=AutomationControlled')
    opts.add_argument('--incognito')
    opts.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/94.0.4606.61 Safari/537.36'
    )
    try:
        driver = webdriver.Chrome(options=opts)
        return driver
    except Exception as e:
        print(f"❌ 無法啟動 ChromeDriver：{e}")
        raise

def get_main_list():
    """
    抓取首頁分類列表，回傳 list of dict：
      [{ 'cover':…, 'link':…, 'title':… }, …]
    """
    driver = init_driver()
    result = []
    try:
        for p in range(1, PAGES+1):
            url = f"{DOMAIN}categories?page={p}"
            driver.get(url)
            time.sleep(2)

            soup = BeautifulSoup(driver.page_source, 'lxml')
            for a in soup.select('div[class="flex lg:-mx-4"] a.inline-block'):
                img = a.find('img')
                cover = img.get('data-src') or img.get('src')
                m = re.match(r"https://assets\.zeczec\.com/asset_\d+_image_big\.(?:jpe?g|png)", cover)
                if not m:
                    # 如果格式不對，就跳過
                    continue

                title = a.select_one('h3').get_text(strip=True)
                link  = DOMAIN + a['href']
                result.append({'cover': cover, 'link': link, 'title': title})

        print(f"✅ 共抓到首頁列表 {len(result)} 筆")
        return result

    except Exception as e:
        print(f"❌ get_main_list 發生錯誤：{e}")
        raise

    finally:
        driver.quit()

def scrape_detail(item, idx):
    """
    對單一 item (dict) 補抓細節，會在 item 裡新增：
      TargetPrice, PastPrice, Backers, TimeLeftDays, Duration
    """
    driver = init_driver()
    try:
        driver.get(item['link'])
        time.sleep(random.uniform(1, 2))
        html = driver.page_source
        
        
              # 驗證字眼檢查
        if "驗證" in html  or "CAPTCHA" in html .upper():
            print( f" ⚠️ 第 {idx} 筆偵測到驗證頁面字眼，可能被封鎖！")
            path = f"debug_block_{idx}.png"
            driver.save_screenshot(path)
            print(f" 已存截圖: {path}")

        
        

        # CAPTCHA 偵測
       # if '驗證' in html or 'CAPTCHA' in html.upper():
        #    print(f"⚠️ 第 {idx} 筆被 CAPTCHA 擋下，略過")
         #   return  # 不往上拋，這筆就不更新
            #遇到 return 那一行，函式後面不管還有什麼程式碼，都不會繼續跑。

        soup = BeautifulSoup(html, 'lxml')
        detail = {}

        # 目標 / 過去集資金額
        for tag in soup.find_all(['span','a'], class_='text-gray-500'):
            txt = tag.get_text(strip=True)
            if txt.startswith('目標') or txt.startswith('過去'):
                m = re.search(r'NT\$ *([\d,]+)', txt)
                if m:
                    key = 'TargetPrice' if txt.startswith('目標') else 'PastPrice'
                    detail[key] = int(m.group(1).replace(',', ''))

        # 贊助人數
        b = soup.select_one('span.js-backers-count')
        if b:
            detail['Backers'] = int(b.get_text(strip=True).replace(',', ''))

        # 剩餘天數
        t = soup.select_one('h3.js-time-left.text-zec-green')
        if t:
            m = re.search(r'(\d+)', t.get_text())
            if m:
                detail['TimeLeftDays'] = int(m.group(1))

        # 期間
        d = soup.select_one('h3.inline-block.text-gray-500.text-xs')
        if d:
            regex = (
                r"(\d{4}/\d{2}/\d{2}\s\d{2}:\d{2})"
                r"(?:\s–\s(\d{4}/\d{2}/\d{2}\s\d{2}:\d{2}))?"
            )
            mt = re.search(regex, d.get_text())
            if mt:
                detail['Duration'] = {'begin': mt.group(1), 'end': mt.group(2) or ''}

        # 把 detail 塞回原 item
        item.update(detail)
        print(f"✅ 第 {idx} 筆更新細節：{detail}")

    except Exception as e:
        print(f"❌ scrape_detail 第 {idx} 筆出錯：{e}")
        # 這裡不 raise，讓 main 繼續處理下一筆
        # raise 關鍵字的作用是「拋出（引發）一個例外」，讓程式立刻中斷當前流程，並將控制權交給最接近的 except 區塊去處理
    finally:
        driver.quit()

def save_json(data):
    """把最終 data 寫成 JSON 檔"""
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"✅ 已寫入 {OUTPUT_FILE}，共 {len(data)} 筆")
    except Exception as e:
        print(f"❌ save_json 失敗：{e}")
        raise

def main():
    # 1. 抓首頁列表
    projects = get_main_list()

    # 2. 逐筆補抓細節
    for i, item in enumerate(projects, start=1):
        scrape_detail(item, i)
        time.sleep(SLEEP_BETWEEN)

    # 3. 寫檔
    save_json(projects)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"[FATAL] 程式異常結束：{e}")
