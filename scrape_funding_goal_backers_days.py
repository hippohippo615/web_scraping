import json
import time
import random
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

DATA_PATH = 'data.json'
SLEEP_ON_ERROR = 180  # 撞錯後等候秒數
SLEEP_BETWEEN = 60    # 每筆處理完等候秒數

# 下載募資平台資料(抓 目標 / 過去集資   贊助人數  剩餘天數  專案期間起訖)
# 把每個功能包裝成函數


def load_projects(path):
    """讀取 JSON 檔案回傳 list of dict"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            projects = json.load(f)
        print(f"✅ 成功讀取 {path} ({len(projects)} 筆專案)")
        return projects
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
    opts.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/94.0.4606.61 Safari/537.36'
    )
    return webdriver.Chrome(options=opts)

def scrape_project(driver, url, index):
    """
    負責：
      1. driver.get()
      2. 檢查 CAPTCHA 關鍵字
      3. BeautifulSoup 解析
      4. 回傳一個 dict，內含 TargetPrice, PastPrice, Backers, TimeLeftDays, Duration
    """
    result = {}
    print("  ✓ driver.get() 成功")
    src = driver.page_source
    # 驗證字眼檢查
    if "驗證" in src or "CAPTCHA" in src.upper():
        print("    ⚠️ 偵測到驗證頁面字眼，可能被封鎖！")
        path = f"debug_block_{index}.png"
        driver.save_screenshot(path)
        print(f"    已存截圖: {path}")

    soup = BeautifulSoup(src, 'lxml')

    # 3.5 目標 / 過去集資
    for tag in soup.find_all(['span', 'a'], class_='text-gray-500'):
        txt = tag.get_text(strip=True)
        if txt.startswith('目標') or txt.startswith('過去'):
            m = re.search(r'NT\$ *([\d,]+)', txt)
            if m:
                key = 'TargetPrice' if txt.startswith('目標') else 'PastPrice'
                result[key] = int(m.group(1).replace(',', ''))

    # 3.6 贊助人數
    b = soup.select_one('span.js-backers-count')
    if b:
        result['Backers'] = int(b.get_text(strip=True).replace(',', ''))

    # 3.7 剩餘時間（天數）
    t_node = soup.select_one('h3.js-time-left.text-zec-green')
    if t_node:
        m = re.search(r'(\d+)', t_node.get_text())
        if m:
            result['TimeLeftDays'] = int(m.group(1))

    # 3.8 專案期間起訖
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


def save_projects(path, projects):
    """把 list of dict 寫回 JSON 檔案"""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(projects, f, ensure_ascii=False, indent=2)
        print(f"✅ 已成功將資料寫入 {path}")
    except Exception as e:
        print(f"❌ 寫入 {path} 失敗：{e!r}")




def main():
    # 1. 讀取
    projects = load_projects(DATA_PATH)

    # 2. 收集所有 link
    link_items = collect_link_items(projects)

    # 3. 逐筆處理
    for i, (orig_idx, url) in enumerate(link_items, start=1):
        print(f"\n[{i}/{len(link_items)}] 處理：{url}")
        if i == 5:  # for debug，只跑前 5 筆
            print("🔧 停在第 5 筆做測試")
            break

        # 3.1 建 driver
        try:
            driver = init_driver()
            print("  ✓ 啟動 driver")
        except Exception as e:
            print(f"  X driver 啟動失敗：{e!r}")
            time.sleep(SLEEP_ON_ERROR)
            continue

        # 3.2 載入並爬資料
        try:
            driver.get(url)
            result = scrape_project(driver, url, i)
        except Exception as e:
            print(f"  X 爬取過程出錯：{e!r}")
            driver.quit()
            print("  driver 已關閉")
            time.sleep(SLEEP_ON_ERROR)
            continue
        finally:
            driver.quit()
            print("  driver.quit() 完成")

        # 3.3 更新回 projects
        for k, v in result.items():
            projects[orig_idx][k] = v
            #result.items() 會回傳一個由 (key, value) tuple 組成的迭代器 
            #例如：result = {'TargetPrice': 30000, 'Backers': 123} 
            #那麼 result.items() 會產生 ('TargetPrice', 30000)、('Backers', 123)。

        # 3.4 顯示結果
        print("    ↳", result)

        # 3.5 等待
        print(f"  ⏱ 等待 {SLEEP_BETWEEN} 秒後繼續…")
        time.sleep(SLEEP_BETWEEN)

    # 4. 寫回
    save_projects(DATA_PATH, projects)

if __name__ == '__main__':
    main()
