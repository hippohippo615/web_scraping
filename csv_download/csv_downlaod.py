'''
臺灣證券交易所
外資及陸資買賣超彙總表
https://www.twse.com.tw/zh/page/trading/fund/TWT38U.html
'''

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

# 處理下拉式選單的工具
from selenium.webdriver.support.ui import Select

# 取得系統時間的工具
from datetime import datetime

# 強制等待 (執行期間休息一下)
from time import sleep

# 整理 json 使用的工具
import json

# 執行 command 的時候用的
import os

'''
[1] Selenium with Python 中文翻譯文檔
參考網頁：https://selenium-python-zh.readthedocs.io/en/latest/index.html
[2] selenium 啓動 Chrome 的進階配置參數
參考網址：https://stackoverflow.max-everyday.com/2019/12/selenium-chrome-options/
[3] Mouse Hover Action in Selenium
參考網址：https://www.toolsqa.com/selenium-webdriver/mouse-hover-action/
[4] How to select a drop-down menu value with Selenium using Python?
參考網址：https://stackoverflow.com/questions/7867537/how-to-select-a-drop-down-menu-value-with-selenium-using-python
'''

# 啟動瀏覽器工具的選項
options = webdriver.ChromeOptions()
# options.add_argument("--headless")                #不開啟實體瀏覽器背景執行
options.add_argument("--start-maximized")         #最大化視窗
options.add_argument("--incognito")               #開啟無痕模式
options.add_argument("--disable-popup-blocking") #禁用彈出攔截
options.add_argument("--disable-notifications")   #取消通知

# 建立儲存圖片的資料夾，不存在就新增
folderPath = 'files'
if not os.path.exists(folderPath):
    os.makedirs(folderPath)

# 下載路徑 (請先在專案目錄下，建立一個新資料夾 files)
download_path = 'C:\\Users\\Liu\\python爬蟲\\cases\\files'

#預設下載路徑
options.add_experimental_option("prefs", {
  "download.default_directory": download_path 
})

# 指定 chromedriver 檔案的路徑
executable_path = './chromedriver.exe'

# 使用 Chrome 的 WebDriver (options 以及 executable_path)
driver = webdriver.Chrome( 
    options = options, 
    executable_path = executable_path
)

# 走訪頁面
def visit():
    driver.get('https://www.twse.com.tw/zh/page/trading/fund/TWT38U.html');

# 選取下拉式選單的項目
def setDropDownMenu():
    # 強制停止
    sleep(1)
    
    # 選擇 select[name="YY"] 元素，並依 option 的 innerText 來進行選取
    selectYY = Select(driver.find_element(By.CSS_SELECTOR, 'div#d1 > select[name="yy"]'))
    selectYY.select_by_visible_text('民國 100 年')
    
    # 強制停止
    sleep(1)
    
    # 選擇 select[name="MM"] 元素，並依 option 的 value 來進行選取
    selectMM = Select(driver.find_element(By.CSS_SELECTOR, 'div#d1 > select[name="mm"]'))
    selectMM.select_by_value('2')
    
    # 強制停止
    sleep(1)
    
    # 選擇 select[name="DD"] 元素，並依 option 的 index 來進行選取
    selectDD = Select(driver.find_element(By.CSS_SELECTOR, 'div#d1 > select[name="dd"]'))
    selectDD.select_by_index(8)
    
    # 強制停止
    sleep(1)
    
    # 按下查詢
    driver.find_element(By.CSS_SELECTOR, 'a.button.search').click()
    
    # 強制停止
    sleep(2)
    
# 下載檔案
def download():
    try:
        # 等待篩選元素出現
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located( 
                (By.CSS_SELECTOR, "div.tools > a.csv") 
            )
        )
        
        # 下載
        driver.find_element(By.CSS_SELECTOR, "div.tools > a.csv").click()
        
        # 強制停止
        sleep(2)
        
        # 找出現在時間 (年月日時分秒)
        strDataTime = datetime.today().strftime("%Y%m%d%H%M%S")
        
        # 擷圖
        driver.save_screenshot(f"./files/{strDataTime}.png");
        
        # 強制停止
        sleep(2)
    except TimeoutException:
        print("等待逾時，即將關閉瀏覽器…")
        sleep(3)
        driver.quit()

# 關閉瀏覽器
def close():
    driver.quit()

# 主程式
if __name__ == '__main__':
    visit()
    setDropDownMenu()
    download()
    close()