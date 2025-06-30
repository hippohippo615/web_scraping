# -*- coding: utf-8 -*-
"""
優化後的 Gutenberg 中文電子書批次下載與儲存程式
— 每個階段都有自己的例外處理
— main() 只做呼叫與全域中止控制
"""
import os
import json
import re
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# --- 全域設定 ---
GUTEN_URL    = 'https://www.gutenberg.org/browse/languages/zh'
DRIVER_PATH  = './chromedriver.exe'
OUTPUT_DIR   = 'homework'
MAX_MAIN     = 5      # 只取前幾本測試用
TIMEOUT      = 5      # WebDriverWait 最長秒數

# --- 啟動 WebDriver ---
def init_driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--start-maximized')
    opts.add_argument('--incognito')
    opts.add_argument('--disable-popup-blocking')
    opts.add_argument('--disable-notifications')
    opts.add_argument('--lang=zh-TW')
    try:
        driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=opts)
        print("✅ ChromeDriver 啟動成功")
        return driver
    except WebDriverException as e:
        print(f"❌ 無法啟動 ChromeDriver：{e}")
        raise SystemExit("程式結束：瀏覽器無法啟動")

driver = init_driver()

# --- 建立輸出資料夾 ---
def ensure_output_dir(path):
    try:
        os.makedirs(path, exist_ok=True)
        print(f"✅ 輸出資料夾準備：{path}")
    except Exception as e:
        print(f"❌ 無法建立資料夾 {path}：{e}")
        raise SystemExit("程式結束：I/O 權限問題")

ensure_output_dir(OUTPUT_DIR)

# --- 階段 1：抓主頁書目連結 ---
def get_main_links():
    data = []
    try:
        driver.get(GUTEN_URL)
        WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'li.pgdbetext a'))
        )
        elems = driver.find_elements(By.CSS_SELECTOR, 'li.pgdbetext a')
        for idx, a in enumerate(elems):
            if idx >= MAX_MAIN:
                break
            data.append({
                'title': a.get_attribute('innerText').strip(),
                'link':  a.get_attribute('href')
            })
        print(f"✅ 抓到 {len(data)} 本書的主連結")
    except Exception as e:
        print(f"❌ get_main_links 階段錯誤：{e}")
        raise
    return data

# --- 階段 2：對每本書抓「Plain Text UTF-8」子連結 ---
def get_sub_links(listData):
    for i, item in enumerate(listData):
        item['sub'] = []
        try:
            driver.get(item['link'])
            WebDriverWait(driver, TIMEOUT).until(
                EC.presence_of_element_located((By.LINK_TEXT, 'Plain Text UTF-8'))
            )
            anchors = driver.find_elements(By.LINK_TEXT, 'Plain Text UTF-8')
            for a in anchors:
                item['sub'].append(a.get_attribute('href'))
            print(f"  ✅ [{i}] {item['title']}：抓到 {len(item['sub'])} 個文本連結")
        except TimeoutException:
            print(f"  ⚠️ [{i}] {item['title']}：找不到純文字下載連結，略過")
        except Exception as e:
            print(f"  ❌ [{i}] {item['title']}：sub 階段錯誤：{e}")
    return listData

# --- 階段 3：儲存 metadata JSON ---
def save_metadata(listData):
    meta_path = os.path.join(OUTPUT_DIR, 'homework_meta.json')
    try:
        with open(meta_path, 'w', encoding='utf-8') as fp:
            json.dump(listData, fp, ensure_ascii=False, indent=2)
        print(f"✅ 已寫入 metadata：{meta_path}")
    except Exception as e:
        print(f"❌ 寫入 metadata 失敗：{e}")

# --- 階段 4：逐本逐章下載並清洗存 TXT & 聚合 train.json ---
def download_and_write(listData):
    train_contents = []
    for i, item in enumerate(listData):
        for url in item.get('sub', []):
            try:
                driver.get(url)
                pre = WebDriverWait(driver, TIMEOUT).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'body > pre'))
                )
                raw = pre.get_attribute('innerText')
                # 同時保留中／英文、數字與常用標點
                #clean = re.findall(r"[A-Za-z\u4E00-\u9FFF0-9，。：“”；、？！‘’\'\",\.]+", raw)
                #text = "".join(clean)
                text=raw
                # 產生檔名
                safe_title = item['title'].replace('\\',' ').replace('\n',' ').replace(':',' ')
                filename = os.path.join(OUTPUT_DIR, f"{safe_title}.txt")
                with open(filename, 'w', encoding='utf-8') as fp:
                    fp.write(text)
                train_contents.append(text)
                print(f"  ✓ 寫出：{filename} ({len(text)} 字)")
            except TimeoutException:
                print(f"  ⚠️ [{i}] {item['title']}：章節載入逾時，略過 {url}")
            except Exception as e:
                print(f"  ❌ [{i}] {item['title']}：寫入失敗：{e}")
    # train.json
    train_path = os.path.join(OUTPUT_DIR, 'train.json')
    try:
        with open(train_path, 'w', encoding='utf-8') as fp:
            json.dump(train_contents, fp, ensure_ascii=False, indent=2)
        print(f"✅ 已寫入訓練集：{train_path}")
    except Exception as e:
        print(f"❌ 寫入 train.json 失敗：{e}")

# --- 主流程 ---
if __name__ == '__main__':
    try:
        mains = get_main_links()
        subs  = get_sub_links(mains)
        save_metadata(subs)
        download_and_write(subs)
    except Exception:
        print("[FATAL] 主流程異常，程式中止")
    finally:
        driver.quit()
        print("✅ 瀏覽器已關閉")