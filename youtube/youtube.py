'''
匯入套件
'''
# 操作 browser 的 API
from selenium import webdriver

# 處理逾時例外的工具
from selenium.common.exceptions import TimeoutException, WebDriverException

# 面對動態網頁，等待某個元素出現的工具，通常與 expected_conditions 搭配
from selenium.webdriver.support.ui import WebDriverWait

# 搭配 WebDriverWait 使用，對元素狀態的一種期待條件，若條件發生，則等待結束，往下一行執行
from selenium.webdriver.support import expected_conditions as EC

# 期待元素出現要透過什麼方式指定，通常與 EC、WebDriverWait 一起使用
from selenium.webdriver.common.by import By

# 強制等待 (執行期間休息一下)
from time import sleep

# 整理 json 使用的工具
import json

# 檢查、建立資料夾或刪檔案
import os

# 子處理程序，用來取代 os.system 的功能
import subprocess
# 收集youtube影片資料

'''
Selenium with Python 中文翻譯文檔
參考網頁：https://selenium-python-zh.readthedocs.io/en/latest/index.html
selenium 啓動 Chrome 的進階配置參數
參考網址：https://stackoverflow.max-everyday.com/2019/12/selenium-chrome-options/
Mouse Hover Action in Selenium
參考網址：https://www.toolsqa.com/selenium-webdriver/mouse-hover-action/
yt-dlp 下載影音的好工具
參考網址：https://github.com/yt-dlp/yt-dlp
'''

# 啟動瀏覽器工具的選項
my_options = webdriver.ChromeOptions()
# my_options.add_argument("--headless")                # 不開啟實體瀏覽器背景執行
my_options.add_argument("--start-maximized")           # 最大化視窗
my_options.add_argument("--incognito")                 # 開啟無痕模式
my_options.add_argument("--disable-popup-blocking")    # 禁用彈出攔截
my_options.add_argument("--disable-notifications")     # 取消通知
my_options.add_argument("--lang=zh-TW")                # 設定為正體中文

# 指定 chromedriver 檔案的路徑
driver_exec_path = './chromedriver.exe'

# 使用 Chrome 的 WebDriver
try:
    driver = webdriver.Chrome(
        options=my_options,
        executable_path=driver_exec_path
    )
    print("✅ ChromeDriver 啟動成功")
except WebDriverException as e:
    print(f"❌ 無法啟動 ChromeDriver：{e}")
    raise SystemExit("無法啟動瀏覽器，程式結束。")

# 建立儲存圖片、影片的資料夾
folderPath = 'youtube'
if not os.path.exists(folderPath):
    try:
        os.makedirs(folderPath)
        print(f"✅ 資料夾 '{folderPath}' 建立完成")
    except Exception as e:
        print(f"❌ 建立資料夾失敗：{e}")
        raise SystemExit("請確認檔案權限或資料夾路徑是否正確，程式結束。")

# 放置爬取的資料
listData = []    


'''
走訪頁面
'''
def visit():
    try:
        driver.get('https://www.youtube.com/')
        print("✅ 開啟 YouTube 首頁")
    except Exception as e:
        print(f"❌ 無法開啟 YouTube 首頁：{e}")
        raise

'''
輸入關鍵字
'''
def search():
    try:
        # 定位搜尋框，輸入名稱
        txtInput = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="search_query"]'))
        )
        txtInput.send_keys('張學友')
        print("✅ 已在搜尋框內輸入關鍵字 '張學友'")
        
        # 等待一下
        sleep(2)
        
        # 按下送出
        btnInput = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Search"]')
        btnInput.click()
        print("✅ 已點擊搜尋按鈕")
        
        # 等待一下
        sleep(2)
    except Exception as e:
        print(f"❌ 搜尋階段發生錯誤：{e}")
        raise

'''
篩選 (選項)
'''
def filterFunc():
    try:
        # 等待篩選元素出現
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div#filter-button button[aria-label='搜尋篩選器']")
            )
        )

        # 按下篩選元素，使項目浮現
        driver.find_elements(
            By.CSS_SELECTOR,
            "div#filter-button button[aria-label='搜尋篩選器']"
        )[0].click()
        print("✅ 已點擊篩選按鈕")
        sleep(2)

        # 按下選擇的項目 (4 分鐘內)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a#endpoint div#label[title='搜尋「4 分鐘內」']"))
        ).click()
        print("✅ 已選擇『4 分鐘內』篩選")
        sleep(2)
        
    except TimeoutException:
        print("⚠️ 等待篩選按鈕超時，略過篩選步驟")
    except Exception as e:
        print(f"❌ 篩選階段發生錯誤：{e}")
        raise

'''
滾動頁面
'''
def scroll():
    '''
    innerHeight => 瀏覽器內部的高度
    offset      => 當前捲動的量(高度)
    count       => 計無效滾動次數
    limit       => 最大無效滾動次數
    wait_second => 每次滾動後的強制等待時間
    '''
    innerHeight = 0
    offset = 0
    count = 0
    limit = 3
    wait_second = 3
    
    try:
        # 在捲動到沒有元素動態產生前，持續捲動
        while count <= limit:
            #offset += 600
            # 取得每次移動高度
            offset = driver.execute_script(
                'return window.document.documentElement.scrollHeight;'
            )

            # 捲軸往下滑動到 offset（文件底部）
            driver.execute_script(f'''
                window.scrollTo({{
                    top: {offset}, 
                    behavior: 'smooth' 
                }});
            ''')
            print(f"⬇️ 滾動至 {offset}px")
            
            # 強制等待，若有新元素生成，會自動增加 scrollHeight
            sleep(wait_second)
            
            # 取得滾動後的最新總高度
            innerHeight = driver.execute_script(
                'return window.document.documentElement.scrollHeight;'
            )
            print(f"📏 滾動後總高度：{innerHeight}px")
            
            # 如果這次滾動前後高度相同，代表已經到底
            if offset == innerHeight:
                count += 1
                print(f"⚠️ 無新內容載入 (count={count}/{limit})")
            
            # 為了實驗功能， 若 offset 超過 1200，就結束滾動
            if offset >= 1200:
                print("🚧 已滾動超過 1200px，停止滾動")
                break
        
        print("✅ 滾動結束")
    except Exception as e:
        print(f"❌ 滾動階段發生錯誤：{e}")
        raise

'''
分析頁面元素資訊
'''
def parse():
    try:
        # 取得主要元素的集合
        ytd_video_renderers = driver.find_elements(
            By.CSS_SELECTOR, 
            'ytd-video-renderer.style-scope.ytd-item-section-renderer'
        )
        print(f"✅ 找到 {len(ytd_video_renderers)} 個影片項目")
        
        # 逐一檢視、擷取資訊
        for idx, yvd in enumerate(ytd_video_renderers, start=1):
            print("=" * 30, f"第 {idx} 筆", "=" * 30)
            try:
                # 取得圖片連結
                img = yvd.find_element(
                    By.CSS_SELECTOR, 
                    "yt-image.style-scope.ytd-thumbnail img"
                )
                imgSrc = img.get_attribute('src')
                print("🖼 圖片連結:", imgSrc)
                
                # 取得影片標題（使用 innerText）
                a = yvd.find_element(By.CSS_SELECTOR, "a#video-title")
                aTitle = a.get_attribute('innerText').strip()
                print("📌 影片標題:", aTitle)
                
                # 取得 YouTube 連結
                aLink = a.get_attribute('href')
                print("🔗 影片連結:", aLink)
                
                # 解析 影片 ID (支援 watch 與 shorts 格式)
                if aLink and "v=" in aLink:
                    youtube_id = aLink.split("v=")[1].split("&")[0]
                elif aLink and "/shorts/" in aLink:
                    youtube_id = aLink.split("/shorts/")[1].split("?")[0]
                else:
                    youtube_id = ""
                print("🎯 影片 ID:", youtube_id)
                
                # 將資料放進 listData
                listData.append({
                    "id": youtube_id,
                    "title": aTitle,
                    "link": aLink,
                    "img": imgSrc
                })
            except Exception as element_error:
                print(f"⚠️ 第 {idx} 筆影片解析失敗：{element_error}")
                # 繼續處理下一筆，不讓一筆錯誤中斷所有
                continue
        
        print("✅ parse() 完成，所有影片資料已擷取")
    except Exception as e:
        print(f"❌ parse() 階段發生錯誤：{e}")
        raise

'''
將 list 存成 json
'''
def saveJson():
    try:
        file_path = os.path.join(folderPath, "youtube.json")
        with open(file_path, "w", encoding='utf-8') as fp:
            json.dump(listData, fp, ensure_ascii=False, indent=4)
        print(f"✅ 已將結果寫入 {file_path}")
    except Exception as e:
        print(f"❌ 寫入 JSON 檔案失敗：{e}")
        raise

'''
關閉瀏覽器
'''
def close():
    try:
        driver.quit()
        print("✅ 瀏覽器已關閉")
    except Exception as e:
        print(f"⚠️ 關閉瀏覽器時發生錯誤：{e}")


'''
主程式
'''
if __name__ == '__main__':
    try:
        visit()
    except Exception:
        print("[FATAL] visit() 階段失敗，程式中止")
        close()
        raise SystemExit

    try:
        search()
    except Exception:
        print("[FATAL] search() 階段失敗，程式中止")
        close()
        raise SystemExit

    try:
        filterFunc()
    except Exception:
        print("[WARN] filterFunc() 階段失敗，但程式繼續")
        # 不把例外往上 raise，僅記警告，繼續後續步驟

    try:
        scroll()
    except Exception:
        print("[FATAL] scroll() 階段失敗，程式中止")
        close()
        raise SystemExit

    try:
        parse()
    except Exception:
        print("[WARN] parse() 階段發生錯誤，但儘量寫出已擷取部分")
        # 不把例外往上 raise，讓 saveJson() 仍可執行

    try:
        saveJson()
    except Exception:
        print("[WARN] saveJson() 階段失敗，可能未寫入檔案")

    close()