import json
import time
import random
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


# 下載募資平台資料(抓 目標 / 過去集資   贊助人數  剩餘天數  專案期間起訖)
# 有函數 例外處理

# 1. 先讀取 data.json
with open('data.json', 'r', encoding='utf-8') as f:
    projects = json.load(f)

# 2. 收集所有有 link 的專案
link_items = []
for idx, proj in enumerate(projects):
    url = proj.get('link')
    if url: #i f url is not None and url != ''
        link_items.append((idx, url))

# 3. 逐筆處理，每次都新啟動一個 driver，處理完就 quit，並印出完整偵錯資訊，最後 sleep 3 分鐘
for i, (orig_idx, url) in enumerate(link_items, start=1):
    print(f"\n[{i}/{len(link_items)}] 開始處理：{url}")
    if i == 5:
        break

    # 3.1 建立新的 Selenium driver
    opts = Options()
    opts.add_argument('--headless=new')
    opts.add_argument('--disable-blink-features=AutomationControlled')
    opts.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/94.0.4606.61 Safari/537.36'
    )
    driver = webdriver.Chrome(options=opts)
    print("  ✓ 已啟動新 driver")

    # 3.2 嘗試載入頁面
    try:
        driver.get(url)
        print("  ✓ driver.get() 成功")
    except Exception as e:
        print(f"  X 載入失敗: {e!r}")
        driver.quit()
        print("  driver 已關閉")
        print("  等待 3 分鐘後繼續…")
        time.sleep(180)
        continue

    # 3.3 印出頁面資訊
    print("    頁面標題:", driver.title)
    print("    當前網址:", driver.current_url)

    src = driver.page_source
    print("    page_source 長度:", len(src))
    print("    前 200 字：", src[:200].replace('\n', ' ').strip())

    # 3.4 偵測是否有驗證字眼
    if "驗證" in src or "CAPTCHA" in src.upper(): #把 HTML 轉大寫後，檢查英文「CAPTCHA」
        print("    ⚠️ 偵測到疑似驗證頁面字眼，可能已被擋！")
        screenshot_path = f"debug_block_{i}.png"
        driver.save_screenshot(screenshot_path)
        print(f"    已存 screenshot: {screenshot_path}")
        # 如果要跳過這筆，取消下面註解：
        # driver.quit()
        # print("  driver 已關閉，等待 3 分鐘後繼續…")
        # time.sleep(180)
        # continue

    soup = BeautifulSoup(src, 'lxml')

    # 3.5 提取：目標 / 過去集資
    for tag in soup.find_all(['span', 'a'], class_='text-gray-500'):
        txt = tag.get_text(strip=True)
        if txt.startswith('目標') or txt.startswith('過去'):
            m = re.search(r'NT\$ *([\d,]+)', txt)
            if m:
                amt = int(m.group(1).replace(',', ''))
                key = 'TargetPrice' if txt.startswith('目標') else 'PastPrice'
                projects[orig_idx][key] = amt

    # 3.6 提取：贊助人數
    b = soup.select_one('span.js-backers-count')
    if b:
        projects[orig_idx]['Backers'] = int(b.get_text(strip=True).replace(',', ''))

    # 3.7 提取：剩餘時間（天數）
    t_node = soup.select_one('h3.js-time-left.text-zec-green')
    if t_node:
        m = re.search(r'(\d+)', t_node.get_text())
        projects[orig_idx]['TimeLeftDays'] = int(m.group(1)) if m else None

    # 3.8 提取：專案期間起訖
    dur_txt = soup.select_one('h3.inline-block.text-gray-500.text-xs')
    if dur_txt:
        # regex = r"(\d{4}\/\d{2}\/\d{2}\s\d{2}:\d{2})(\s–\s(\d{4}\/\d{2}\/\d{2}\s\d{2}:\d{2}))?"
        regex = (
            r"(\d{4}/\d{2}/\d{2}\s\d{2}:\d{2})"  # group 1：開始時間
            r"(?:\s–\s(\d{4}/\d{2}/\d{2}\s\d{2}:\d{2}))?"  ## (?:…)：非捕獲式分組，包住「 – 」＋結束時間
        )# group 2：單純的結束時間
        mt = re.search(regex, dur_txt.get_text())
        if mt:
            projects[orig_idx].setdefault('Duration', {})
            projects[orig_idx]['Duration']['begin'] = mt.group(1)
            projects[orig_idx]['Duration']['end'] = mt.group(2) or ''

    # 3.9 印出剛抓到的結果
    print("    抓到 TargetPrice: ", projects[orig_idx].get('TargetPrice'))
    print("    抓到 PastPrice:   ", projects[orig_idx].get('PastPrice'))
    print("    抓到 Backers:     ", projects[orig_idx].get('Backers'))
    print("    抓到 TimeLeftDays:", projects[orig_idx].get('TimeLeftDays'))
    print("    抓到 Duration:    ", projects[orig_idx].get('Duration'))

    # 3.10 關閉這次的 driver
    driver.quit()
    print("  driver.quit() 完成")

    # 3.11 等待 1 分鐘後繼續
    print("  等待 1 分鐘後繼續…")
    time.sleep(60)

# 4. 全部跑完後一次性寫回 data.json（
try:
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(projects, f, ensure_ascii=False, indent=2)
    print("✅ 已成功將資料寫入 data.json")
except Exception as e:
    print(f"❌ 寫入 data.json 失敗：{e!r}")