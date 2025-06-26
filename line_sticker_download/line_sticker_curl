import os
import json
import requests
from bs4 import BeautifulSoup

# 下載LINE貼圖(最後用CURL下載)

FOLDER_PATH = './line_stickers'
URL         = 'https://store.line.me/stickershop/product/17555/zh-Hant'
HEADERS     = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/135.0.0.0 Safari/537.36'
}

def prepare_folder(path):
    """建立資料夾（若不存在則新增）"""
    try:
        os.makedirs(path, exist_ok=True)
        print(f"✅ 資料夾 {path} 就緒")
    except Exception as e:
        print(f"❌ 建立資料夾失敗：{e}")
        raise

def fetch_page(url, headers):
    """下載網頁，回傳 HTML 文字"""
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        print(f"✅ 網頁取得成功，狀態碼 {resp.status_code}")
        return resp.text
    except Exception as e:
        print(f"❌ 取得網頁失敗：{e}")
        raise

def parse_li_elements(html):
    """解析 HTML，回傳所有帶 data-preview 的 <li> 列表"""
    try:
        soup = BeautifulSoup(html, 'lxml')
        li_list = soup.find_all("li", attrs={"data-preview": True})
        print(f"✅ 找到 {len(li_list)} 個貼圖預覽元素")
        return li_list
    except Exception as e:
        print(f"❌ 解析貼圖列表失敗：{e}")
        raise

def extract_stickers(li_list):
    """從 <li> 元素中擷取貼圖 id 和下載連結"""
    stickers = []
    for li in li_list:
        try:
            info = json.loads(li["data-preview"])
            stickers.append({"id": info["id"], "url": info["staticUrl"]})
        except Exception as e:
            print(f"⚠️ 擷取貼圖資訊失敗：{e}")
            continue
    print(f"✅ 共解析出 {len(stickers)} 張貼圖")
    return stickers

def download_stickers_with_curl(stickers, folder):
    """
    使用 curl 逐張下載貼圖並儲存本機
    -k 跳過 SSL 憑證驗證
    -o <路徑> 指定檔名輸出
    """
    for s in stickers:
        try:
            dest = os.path.join(folder, f"{s['id']}.png")
            cmd = f"curl -k {s['url']} -o {dest}"
            ret = os.system(cmd)
            if ret != 0:
                raise RuntimeError(f"curl 回傳值 {ret}")
            print(f"✅ 貼圖 {s['id']} 下載完成：{dest}")
        except Exception as e:
            print(f"❌ 貼圖 {s['id']} 下載失敗：{e}")
            continue

def main():
    prepare_folder(FOLDER_PATH)
    html       = fetch_page(URL, HEADERS)
    li_list    = parse_li_elements(html)
    stickers   = extract_stickers(li_list)
    download_stickers_with_curl(stickers, FOLDER_PATH)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"[FATAL] 程式異常結束：{e}")
