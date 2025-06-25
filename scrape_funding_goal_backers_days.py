import json
import time
import random
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 下載募資平台資料(抓 目標 / 過去集資   贊助人數  剩餘天數  專案期間起訖)
# (盡量在函數內例外處理)

DATA_PATH      = 'data.json'
SLEEP_ON_ERROR = 180  # 撞錯後等候秒數
SLEEP_BETWEEN  = 60   # 每筆處理完等候秒數

def load_projects(path):
    """讀取 JSON 檔案回傳 list of dict"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            projects = json.load(f)
        print(f"✅ 成功讀取 {path} ({len(projects)} 筆專案)")
        return projects
    except FileNotFoundError:
        print(f"⚠️ 找不到 {path}，回傳空列表")
        return []
    except Exception as e:
        print(f"❌ 讀取 {path} 失敗：{e!r}")
        raise

def collect_link_items(projects):
    """從 projects 裡找出所有有 link 的項目，回傳 list of (index, url)"""
    items = []
    for idx, proj in enumerate(projects):
        url = proj.get('link')
        if url:
            items.append((idx, url))
    print(f"🔗 共找到 {len(items)} 個含 link 的專案")
    return items

def init_driver():
    """啟動一個隱身且偽裝過的 Chrome driver"""
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
        print("  ✓ driver 啟動成功")
        return driver
    except Exception as e:
        print(f"  ❌ driver 啟動失敗：{e!r}")
        raise

def scrape_project(url, index):
    """
    負責：
      1. driver.get()
      2. 檢查 CAPTCHA
      3. 解析並回傳結果 dict
    """
    driver = init_driver()
    try:
        driver.get(url)
        time.sleep(random.uniform(1, 2))
        src = driver.page_source
        
        
           # 驗證字眼檢查
        if "驗證" in src or "CAPTCHA" in src.upper():
            print("    ⚠️ 偵測到驗證頁面字眼，可能被封鎖！")
            path = f"debug_block_{index}.png"
            driver.save_screenshot(path)
            print(f"    已存截圖: {path}")


        # CAPTCHA 偵測
        #if '驗證' in src or 'CAPTCHA' in src.upper():
         #   print("    ⚠️ 偵測到驗證頁面，截圖 & 等待重試")
          #  path = f"debug_block_{index}.png"
           # driver.save_screenshot(path)
           # time.sleep(SLEEP_ON_ERROR)
           # raise RuntimeError("CAPTCHA block")

        soup = BeautifulSoup(src, 'lxml')
        result = {}

        # 目標 / 過去集資金額
        for tag in soup.find_all(['span', 'a'], class_='text-gray-500'):
            txt = tag.get_text(strip=True)
            if txt.startswith('目標') or txt.startswith('過去'):
                m = re.search(r'NT\$ *([\d,]+)', txt)
                if m:
                    key = 'TargetPrice' if txt.startswith('目標') else 'PastPrice'
                    result[key] = int(m.group(1).replace(',', ''))

        # 贊助人數
        b = soup.select_one('span.js-backers-count')
        if b:
            result['Backers'] = int(b.get_text(strip=True).replace(',', ''))

        # 剩餘天數
        t_node = soup.select_one('h3.js-time-left.text-zec-green')
        if t_node:
            m = re.search(r'(\d+)', t_node.get_text())
            if m:
                result['TimeLeftDays'] = int(m.group(1))

        # 專案期間
        dur_txt = soup.select_one('h3.inline-block.text-gray-500.text-xs')
        if dur_txt:
            regex = (
                r"(\d{4}/\d{2}/\d{2}\s\d{2}:\d{2})"
                r"(?:\s–\s(\d{4}/\d{2}/\d{2}\s\d{2}:\d{2}))?"
            )
            mt = re.search(regex, dur_txt.get_text())
            if mt:
                result['Duration'] = {
                    'begin': mt.group(1),
                    'end': mt.group(2) or ''
                }

        return result

    except Exception:
        # 無法自行處理的錯誤往上丟
        raise

    finally:
        driver.quit()
        print("  driver.quit() 完成")

def save_projects(path, projects):
    """把 list of dict 寫回 JSON 檔案"""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(projects, f, ensure_ascii=False, indent=2)
        print(f"✅ 已成功將資料寫入 {path}")
    except Exception as e:
        print(f"❌ 寫入 {path} 失敗：{e!r}")

def main():
    projects   = load_projects(DATA_PATH)
    link_items = collect_link_items(projects)

    for i, (orig_idx, url) in enumerate(link_items, start=1):
        
        if i==5:
            print("🔧 停在第 5 筆做測試")
            break
        
        print(f"\n[{i}/{len(link_items)}] 處理：{url}")
        try:
            result = scrape_project(url, i)
        except Exception as e:
            print(f"  ↳ 此筆失敗：{e}，跳過")
            continue

        projects[orig_idx].update(result)
        print("    ↳ 成果：", result)

        time.sleep(SLEEP_BETWEEN)

    save_projects(DATA_PATH, projects)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"[FATAL] 程式異常結束：{e}")