'''
匯入套件
'''
# 操作 browser 的 API
from selenium import webdriver

# 處理逾時例外的工具
from selenium.common.exceptions import TimeoutException

# 面對動態網頁，等待某個元素出現的工具，通常與 exptected_conditions 搭配
from selenium.webdriver.support.ui import WebDriverWait

# 搭配 WebDriverWait 使用，對元素狀態的一種期待條件，若條件發生，則等待結束，往下一行執行
from selenium.webdriver.support import expected_conditions as EC

# 期待元素出現要透過什麼方式指定，通常與 EC、WebDriverWait 一起使用
from selenium.webdriver.common.by import By

# 強制等待 (執行期間休息一下)
from time import sleep

# 整理 json 使用的工具
import json

# 執行 command 的時候用的
import os

# 子處理程序，用來取代 os.system 的功能
import subprocess

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
# my_options.add_argument("--headless")                #不開啟實體瀏覽器背景執行
my_options.add_argument("--start-maximized")         #最大化視窗
my_options.add_argument("--incognito")               #開啟無痕模式
my_options.add_argument("--disable-popup-blocking") #禁用彈出攔截
my_options.add_argument("--disable-notifications")  #取消通知
my_options.add_argument("--lang=zh-TW") #設定為正體中文

# 指定 chromedriver 檔案的路徑
driver_exec_path = './chromedriver.exe'

# 使用 Chrome 的 WebDriver
driver = webdriver.Chrome( 
    options = my_options, 
    executable_path = driver_exec_path
)

# driver.set_window_size(1200, 960) #視窗大小設定 (寬，高)
# driver.maximize_window() #視窗最大化
# driver.minimize_window() #視窗最小化

 # 建立儲存圖片、影片的資料夾
folderPath = 'youtube'
if not os.path.exists(folderPath):
    os.makedirs(folderPath)

# 放置爬取的資料
listData = []    

'''
function 名稱

'''
#走訪頁面
def visit():
    driver.get('https://www.youtube.com/')
 
#輸入關鍵字 
def search():
    #輸入名稱
    txtInput = driver.find_element(By.CSS_SELECTOR, 'input[name="search_query"]')
    txtInput.send_keys('張學友')
    
    # 等待一下
    sleep(2)
    
    #按下送出
    btnInput = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Search"]')
    
    btnInput.click()
   
    
    # 等待一下
    sleep(2)

# 篩選 (選項)
def filterFunc():
    try:
        # 等待篩選元素出現
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located( 
                (By.CSS_SELECTOR, "div#filter-button button[aria-label='搜尋篩選器']") 
            )
        )

        #按下篩選元素，使項目浮現
        driver.find_elements(
            By.CSS_SELECTOR, 
            "div#filter-button button[aria-label='搜尋篩選器']"
        )[0].click()

        # 等待一下
        sleep(2)

        # 按下選擇的項目
        driver.find_element(
            By.CSS_SELECTOR, 
            "a#endpoint div#label[title='搜尋「4 分鐘內」']"
        ).click()
        
        # 等待一下
        sleep(2)
        
    except TimeoutException:
        print("等待逾時，即將關閉瀏覽器…")
        driver.quit()    
# 滾動頁面
def scroll():
    '''
    innerHeight => 瀏覽器內部的高度
    offset => 當前捲動的量(高度)
    count => 計無效滾動次數
    limit => 最大無效滾動次數
    wait_second => 每次滾動後的強制等待時間
    '''
    innerHeight = 0
    offset = 0
    count = 0
    limit = 3
    wait_second = 3
    
    # 在捲動到沒有元素動態產生前，持續捲動
    while count <= limit:
        #offset += 600
        # 取得每次移動高度
        offset = driver.execute_script(
            'return window.document.documentElement.scrollHeight;'
        )

        '''
        或是每次只滾動一點距離，
        以免有些網站會在移動長距離後，
        將先前移動當中的元素隱藏

        例如將上方的 script 改成:
        offset += 600
        '''

        # 捲軸往下滑動
        driver.execute_script(f'''
            window.scrollTo({{
                top: {offset}, 
                behavior: 'smooth' 
            }});
        ''')
        
        # 強制等待，此時若有新元素生成，瀏覽器內部高度會自動增加
        sleep(wait_second)
        
        # 透過執行 js 語法來取得捲動後的當前總高度
        innerHeight = driver.execute_script(
            'return window.document.documentElement.scrollHeight;'
        );
        
        # 經過計算，如果滾動距離(offset)大於等於視窗內部總高度(innerHeight)，代表已經到底了
        if offset == innerHeight:
            count += 1
            
        # 為了實驗功能，捲動超過一定的距離，就結束程式
        if offset >= 1200:
            break     
# 分析頁面元素資訊
def parse():
    # 取得主要元素的集合
    ytd_video_renderers = driver.find_elements(
        By.CSS_SELECTOR, 
        'ytd-video-renderer.style-scope.ytd-item-section-renderer'
    )
    
    # 逐一檢視元素
    for ytd_video_renderer in ytd_video_renderers:
        # 印出分隔文字
        print("=" * 30)
        
        # 取得圖片連結
        img = ytd_video_renderer.find_element(
            By.CSS_SELECTOR, 
            "yt-image.style-scope.ytd-thumbnail img"
        )
        imgSrc = img.get_attribute('src')
        print(imgSrc) 
        
        # 取得資料名稱
        a = ytd_video_renderer.find_element(By.CSS_SELECTOR, "a#video-title")
        aTitle = a.get_attribute('innerText') #取內文用innertext javascript 「取得元素內部顯示文字」的方法
        print(aTitle)
        
        # 取得 YouTube 連結
        aLink = a.get_attribute('href')
        print(aLink)
        
        
        if aLink is None:
            youtube_id = ""
        elif "v=" in aLink:
            # 影片頁面（標準 Watch URL），例如 "...?v=XYZ123&ab_channel=...”
            # 先用 "v=" 分割，再用 "&" 把參數串切掉
            youtube_id = aLink.split("v=")[1].split("&")[0]
        elif "/shorts/" in aLink:
            # Shorts 頁面，URL 通常像 "/shorts/ABC789?..." 或只是 "/shorts/ABC789"
            youtube_id = aLink.split("/shorts/")[1].split("?")[0]
        else:
            # 其他情況：既沒有 v= 也不是 shorts，就當成沒抓到
            youtube_id = ""
        
        # 取得 影音 ID
        #youtube_id = aLink.split("v=")[1]
        
        # 放資料到 list 中
        listData.append({
            "id": youtube_id,
            "title": aTitle,
            "link": aLink,
            "img": imgSrc
        })
# 將 list 存成 json
def saveJson():
    with open(f"{folderPath}/youtube.json", "w", encoding='utf-8') as fp:
        fp.write( json.dumps(listData, ensure_ascii=False, indent=4) )      
# 關閉瀏覽器
def close():
    driver.quit() 
    
def download():   
    # 開啟 json 檔案
    with open(f"{folderPath}/youtube.json", "r", encoding='utf-8') as fp:
        #取得 json 字串
        strJson = fp.read()
    
    # 將 json 轉成 list (裡面是 dict 集合)
    listResult = json.loads(strJson)

    # 下載所有檔案
    for index, obj in enumerate(listResult):
        if index > 3:
            break
        
        print("=" * 50)
        print(f"正在下載連結: {obj['link']}")
        
        # 定義指令
        cmd = [
            './yt-dlp.exe', 
            obj['link'], 
            '-f', 'w[ext=mp4]', 
            '-o', f'{folderPath}/%(title)s.%(ext)s'
        ]

        # 執行指令，並取得回傳結果
        #用 Python 的 subprocess 模組，去「呼叫外部程式」並且「把它的輸出抓回來」
        #stdout=subprocess.PIPE  把該指令的「標準輸出」（stdout）導向一個暫存的管線 (PIPE)，讓你可以從 result.stdout 讀到它執行時印出來的文字（位元組）。
        #stderr=subprocess.STDOUT  表示把「標準錯誤」（stderr）也導到同一條管線裡，等於把錯誤訊息和一般輸出都混在一起，統一從 result.stdout 讀。
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        # 將回傳結果進行解碼，顯示實際執行過程的文字輸出
        #.decode('utf-8') 可以格式化
        #output = result.stdout.decode('utf-8')
        #中文 Windows 下的程序输出
        output = result.stdout.decode('Big5')
        print("下載完成，訊息如下:")
        print(output)
            
    
    
    
'''

主程式

'''

if __name__ =='__main__':
    visit() 
    search()
    filterFunc()
    scroll()
    parse()
    saveJson()
    close() 
    download()