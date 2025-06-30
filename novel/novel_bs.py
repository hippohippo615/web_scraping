# -*- coding: utf-8 -*-
"""
Gutenberg 中文電子書批次下載（Requests + BeautifulSoup 版）

流程：
 1. fetch_main_links(): 取得主頁 li.pgdbetext a 文字書目與連結
 2. fetch_sub_links():  進入每本書的頁面，找 Plain Text UTF-8 下載連結
 3. save_metadata():    把 metadata 寫成 JSON
 4. download_and_write(): 依照子連結逐本下載、清洗並寫 TXT，匯集 train.json
"""

import os
import re
import json
import time
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from typing import List, Dict

# --- 全域設定 ---
GUTEN_URL   = 'https://www.gutenberg.org/browse/languages/zh'
OUTPUT_DIR  = Path('homework_bs')
MAX_MAIN    = 5            # 範例只取前 5 本
HEADERS     = {'User-Agent': 'Mozilla/5.0'}
SLEEP_BETW  = 1.0          # requests 間隔秒數

# 建立 HTTP session
session = requests.Session()
session.headers.update(HEADERS)


def fetch_main_links() -> List[Dict[str, str]]:
    """抓取主頁書目連結與書名"""
    mains: List[Dict[str, str]] = []
    try:
        resp = session.get(GUTEN_URL, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'lxml')
        for i, a in enumerate(soup.select('li.pgdbetext a')):
            if i >= MAX_MAIN:
                break
            mains.append({
                'title': a.get_text(strip=True),
                'link':  requests.compat.urljoin(GUTEN_URL, a['href']),
            })
        print(f"✅ 抓取到 {len(mains)} 本主書目")
    except Exception as e:
        print(f"❌ fetch_main_links 失敗：{e}")
    return mains


def fetch_sub_links(mains: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """對每本書進入其頁面，蒐集 Plain Text UTF-8 連結"""
    for idx, item in enumerate(mains):
        item['sub'] = []
        try:
            r = session.get(item['link'], timeout=10)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, 'lxml')
            for a in soup.find_all('a', string='Plain Text UTF-8'):
                href = a.get('href')
                full = requests.compat.urljoin(item['link'], href)
                item['sub'].append(full)
            print(f"  ✅ [{idx}] {item['title']}：共 {len(item['sub'])} 個子連結")
        except Exception as e:
            print(f"  ⚠️ [{idx}] {item['title']} 子連結蒐集失敗：{e}")
        time.sleep(SLEEP_BETW)
    return mains


def save_metadata(mains: List[Dict[str, str]]) -> None:
    """把書目與子連結寫成 JSON"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    meta_path = OUTPUT_DIR / 'metadata.json'
    try:
        with open(meta_path, 'w', encoding='utf-8') as fp:
            json.dump(mains, fp, ensure_ascii=False, indent=2)
        print(f"✅ metadata 寫入：{meta_path}")
    except Exception as e:
        print(f"❌ metadata 寫入失敗：{e}")


def download_and_write(mains: List[Dict[str, str]]) -> None:
    """對每本書、每個子連結下載純文字，清洗後寫 TXT 並累積 train.json"""
    train: List[str] = []
    for idx, item in enumerate(mains):
        safe_title = re.sub(r'[\\/:*?"<>|]', '_', item['title'])
        for sub_url in item.get('sub', []):
            try:
                r = session.get(sub_url, timeout=10)
                r.raise_for_status()
                p = BeautifulSoup(r.text, 'lxml').find('p')
                
                raw = p.get_text() if p else ""   #r.text 也可以拿到小說內容
                #print(raw)
                #clean = re.findall(
                 #   r"[A-Za-z\u4E00-\u9FFF0-9，。：“”；、？！‘’'\",\.]+",
                  #  raw
                #)
                #content = "".join(clean)
                content = raw
                fname = OUTPUT_DIR / f"{safe_title}.txt"
                with open(fname, 'w', encoding='utf-8') as fp:
                    fp.write(content)
                print(f"  ✓ [{idx}] {safe_title} → {fname.name} ({len(content)} 字)")
                train.append(content)
            except Exception as e:
                print(f"  ⚠️ [{idx}] {safe_title} 下載/寫入失敗：{e}")
            time.sleep(SLEEP_BETW)
    train_path = OUTPUT_DIR / 'train.json'
    try:
        with open(train_path, 'w', encoding='utf-8') as fp:
            json.dump(train, fp, ensure_ascii=False, indent=2)
        print(f"✅ train.json 寫入：{train_path}")
    except Exception as e:
        print(f"❌ train.json 寫入失敗：{e}")


def main():
    mains = fetch_main_links()
    if not mains:
        print("❌ 未抓到任何書目，程式結束")
        return
    mains = fetch_sub_links(mains)
    save_metadata(mains)
    download_and_write(mains)


if __name__ == '__main__':
    main()
