# 匯入套件
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import json
import os
import subprocess
import sys

# Selenium 啟動參數
my_options = webdriver.ChromeOptions()
# my_options.add_argument("--headless")
my_options.add_argument("--start-maximized")
my_options.add_argument("--incognito")
my_options.add_argument("--disable-popup-blocking")
my_options.add_argument("--disable-notifications")
my_options.add_argument("--lang=zh-TW")

driver_exec_path = './chromedriver.exe'

# 啟動 WebDriver
try:
    driver = webdriver.Chrome(options=my_options,
                              executable_path=driver_exec_path)
    print("✅ ChromeDriver 啟動成功")
except WebDriverException as e:
    print(f"❌ 無法啟動 ChromeDriver：{e}")
    raise SystemExit("無法啟動瀏覽器，程式結束。")

# 建立存放資料夾
folderPath = 'youtube'
if not os.path.exists(folderPath):
    try:
        os.makedirs(folderPath)
        print(f"✅ 資料夾 '{folderPath}' 建立完成")
    except Exception as e:
        print(f"❌ 建立資料夾失敗：{e}")
        raise SystemExit("請確認檔案權限或路徑正確，程式結束。")

listData = []


def visit():
    try:
        driver.get('https://www.youtube.com/')
        print("✅ 開啟 YouTube 首頁")
    except Exception as e:
        print(f"❌ visit() 階段錯誤：{e}")
        raise


def search():
    try:
        txt = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="search_query"]'))
        )
        txt.send_keys('張學友')
        print("✅ 已輸入關鍵字 '張學友'")
        sleep(2)

        btn = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Search"]')
        btn.click()
        print("✅ 已點擊搜尋")
        sleep(2)
    except Exception as e:
        print(f"❌ search() 階段錯誤：{e}")
        raise


def filterFunc():
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div#filter-button button[aria-label='搜尋篩選器']"))
        )
        driver.find_elements(
            By.CSS_SELECTOR,
            "div#filter-button button[aria-label='搜尋篩選器']"
        )[0].click()
        print("✅ 已點擊篩選")
        sleep(2)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a#endpoint div#label[title='搜尋「4 分鐘內」']"))
        ).click()
        print("✅ 已選擇『4 分鐘內』")
        sleep(2)
    except TimeoutException:
        print("⚠️ filterFunc() 等待逾時，略過篩選")
    except Exception as e:
        print(f"❌ filterFunc() 階段錯誤：{e}")
        raise


def scroll():
    innerHeight = 0
    offset = 0
    count = 0
    limit = 3
    wait_second = 3

    try:
        while count <= limit:
            offset = driver.execute_script(
                'return window.document.documentElement.scrollHeight;'
            )
            driver.execute_script(f'''
                window.scrollTo({{top: {offset}, behavior:'smooth'}});
            ''')
            print(f"⬇️ 滾動至 {offset}px")
            sleep(wait_second)

            innerHeight = driver.execute_script(
                'return window.document.documentElement.scrollHeight;'
            )
            print(f"📏 總高度：{innerHeight}px")

            if offset == innerHeight:
                count += 1
                print(f"⚠️ 無新內容 (count={count}/{limit})")

            if offset >= 1200:
                print("🚧 已超過 1200px，停止滾動")
                break
        print("✅ scroll() 完成")
    except Exception as e:
        print(f"❌ scroll() 階段錯誤：{e}")
        raise


def parse():
    try:
        items = driver.find_elements(
            By.CSS_SELECTOR,
            'ytd-video-renderer.style-scope.ytd-item-section-renderer'
        )
        print(f"✅ 找到 {len(items)} 支影片")
        for idx, yvd in enumerate(items, start=1):
            print("="*10, f"第 {idx}", "="*10)
            try:
                img = yvd.find_element(
                    By.CSS_SELECTOR,
                    "yt-image.style-scope.ytd-thumbnail img"
                )
                src = img.get_attribute('src')
                a = yvd.find_element(By.CSS_SELECTOR, "a#video-title")
                title = a.get_attribute('innerText').strip()
                link = a.get_attribute('href')
                if link and "v=" in link:
                    vid = link.split("v=")[1].split("&")[0]
                elif link and "/shorts/" in link:
                    vid = link.split("/shorts/")[1].split("?")[0]
                else:
                    vid = ""
                listData.append({
                    "id": vid,
                    "title": title,
                    "link": link,
                    "img": src
                })
                print("🎯", vid, title)
            except Exception as ee:
                print(f"⚠️ 第 {idx} 筆解析失敗：{ee}")
                continue
        print("✅ parse() 完成")
    except Exception as e:
        print(f"❌ parse() 階段錯誤：{e}")
        raise


def saveJson():
    try:
        path = os.path.join(folderPath, "youtube.json")
        with open(path, "w", encoding='utf-8') as fp:
            json.dump(listData, fp, ensure_ascii=False, indent=4)
        print(f"✅ 已寫入 {path}")
    except Exception as e:
        print(f"❌ saveJson() 階段錯誤：{e}")
        raise


def download():
    try:
        # 讀 JSON
        path = os.path.join(folderPath, "youtube.json")
        with open(path, "r", encoding='utf-8') as fp:
            results = json.load(fp)
        # 只示範前 4 支
        for idx, obj in enumerate(results):
            if idx > 3:
                break
            print("="*10, f"下載第 {idx+1}", "="*10)
            print("▶️", obj['link'])
            cmd = [
                './yt-dlp.exe',
                obj['link'],
                '-f', 'w[ext=mp4]',
                '-o', f'{folderPath}/%(title)s.%(ext)s'
            ]
            #check=True：告诉 Python “如果命令失败（return code ≠ 0），请帮我抛出例外”。
            try:
                res = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    check=True
                )
                raw = res.stdout or b''
                '''
                res.stdout：如果你在 subprocess.run(..., stdout=PIPE) 時有捕捉到程式的「標準輸出」（stdout），它就會是一個 bytes 物件（可能是空的 b''，也可能裡面有內容）。
                or b''：如果 res.stdout 本身是空（b''），在布林判斷時會被視為 False，這時就使用 b'' 這個「備胎」值。
                '''
                
            except subprocess.CalledProcessError as e:
                print(f"❌ yt-dlp 執行失敗 code={e.returncode}")
                raw = e.stdout or b''
            # 解碼：utf-8 → cp950 → replace
            for enc in ('utf-8', 'cp950'):
                try:
                    output = raw.decode(enc)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                output = raw.decode('utf-8', errors='replace')
                '''
                如果遇到无法用 UTF-8 规则正确解码的字节（例如不合法或不完整的多字节序列），

                不要抛出 UnicodeDecodeError，

                而是用“替代字符” �（U+FFFD）来代替那些错误的字节。
                '''
            print("📥 yt-dlp 輸出：")
            print(output)
    except Exception as e:
        print(f"❌ download() 階段錯誤：{e}")
        # 下載失敗也不 raise，結束流程即可


def close():
    try:
        driver.quit()
        print("✅ 瀏覽器已關閉")
    except Exception as e:
        print(f"⚠️ close() 階段錯誤：{e}")


if __name__ == '__main__':
    try:
        visit()
        search()
        filterFunc()
        scroll()
        parse()
        saveJson()
    except Exception as e:
        print(f"[FATAL] 主流程中斷：{e}")
    finally:
        close()
    # 最後再做下載
    download()