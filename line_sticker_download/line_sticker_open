import os
import json
import requests
from bs4 import BeautifulSoup
#用with open 下載

FOLDER_PATH = 'line_stickers'
URL         = 'https://store.line.me/stickershop/product/17555/zh-Hant'
HEADERS     = {'user-agent': 'Mozilla/5.0'}

def prepare_folder(path):
    """建立資料夾（若已存在不錯誤）"""
    try:
        os.makedirs(path, exist_ok=True)
        print(f"✅ 資料夾 {path} 準備完成")
    except Exception as e:
        print(f"❌ 建立資料夾失敗：{e}")
        raise

def fetch_page(url, headers):
    """下載網頁並檢查狀態碼"""
    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        print(f"✅ 網頁取得成功，狀態碼 {res.status_code}")
        return res.text
    except Exception as e:
        print(f"❌ 取得網頁失敗：{e}")
        raise

def parse_li_list(html):
    """從 HTML 找出所有帶 data-preview 的 <li>"""
    try:
        soup = BeautifulSoup(html, 'lxml')
        li_list = soup.find_all("li", attrs={"data-preview": True})
        print(f"✅ 找到 {len(li_list)} 個貼圖預覽")
        return li_list
    except Exception as e:
        print(f"❌ 解析 HTML 失敗：{e}")
        raise

def extract_stickers(li_list):
    """從 data-preview 屬性取出每張貼圖的 id 與 url"""
    stickers = []
    for li in li_list:
        try:
            info = json.loads(li["data-preview"])
            stickers.append({
                "id":  info["id"],
                "url": info["staticUrl"]
            })
        except Exception as e:
            print(f"⚠️ 解析貼圖資料失敗：{e}")
            continue
    print(f"✅ 共解析 {len(stickers)} 張貼圖")
    return stickers

def download_stickers(stickers, folder):
    """下載每張貼圖並存檔"""
    for s in stickers:
        try:
            r = requests.get(s["url"], stream=True)
            r.raise_for_status()
            path = os.path.join(folder, f"{s['id']}.png")
            with open(path, "wb") as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            print(f"✅ 下載完成：{path}")
        except Exception as e:
            print(f"❌ 貼圖 {s['id']} 下載失敗：{e}")
            continue

def main():
    prepare_folder(FOLDER_PATH)
    html     = fetch_page(URL, HEADERS)
    li_list  = parse_li_list(html)
    stickers = extract_stickers(li_list)
    download_stickers(stickers, FOLDER_PATH)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"[FATAL] 程式異常結束：{e}")
