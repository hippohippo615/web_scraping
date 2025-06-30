import os
from datetime import datetime
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# --------------------
# 全局設定
# --------------------
# 下載資料夾
#可以讓程式在資料夾已存在時不會拋出錯誤，而是直接跳過建立步驟，提升容錯能力。
folderPath = 'files'
if not os.path.exists(folderPath):
    os.makedirs(folderPath, exist_ok=True)
# 轉成絕對路徑
download_path = os.path.abspath(folderPath)

# Selenium Options
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--incognito")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-notifications")
options.add_argument("--lang=zh-TW")
# 設置 prefs
prefs = {
    "download.prompt_for_download": False,
    "profile.default_content_settings.popups": 0,
    "download.default_directory": download_path,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True,
}
options.add_experimental_option("prefs", prefs)

# 啟動 WebDriver
try:
    from selenium.webdriver.chrome.service import Service
    service = Service(executable_path='./chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    # 強制使用 CDP 指定下載行為
    driver.execute_cdp_cmd(
        "Page.setDownloadBehavior", {
            "behavior": "allow",
            "downloadPath": download_path
        }
    )
    print("✅ Chrome 截圖及下載實例啟動成功")
except WebDriverException as e:
    print(f"❌ 無法啟動 ChromeDriver：{e}")
    raise SystemExit("程式終止")

# --------------------
# 功能函式
# --------------------
def visit():
    """開啟 TWSE 外資買賣超頁面"""
    try:
        driver.get('https://www.twse.com.tw/zh/page/trading/fund/TWT38U.html')
        print("✅ 開啟主頁成功")
    except Exception as e:
        print(f"❌ visit() 階段錯誤：{e}")
        raise


def set_drop_down_menu():
    """選擇年月日並執行查詢"""
    try:
        sleep(1)
        # 年
        sel_yy = Select(WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.panel.label5 select#label0'))
        ))
        sel_yy.select_by_value('2011')
        sleep(1)
        # 月
        sel_mm = Select(driver.find_element(By.CSS_SELECTOR, 'div.panel.label5 select[name="mm"]'))
        sel_mm.select_by_visible_text('02月')
        sleep(1)
        # 日
        sel_dd = Select(driver.find_element(By.CSS_SELECTOR, 'div.panel.label5 select[name="dd"]'))
        sel_dd.select_by_index(8)
        sleep(1)
        # 查詢
        driver.find_element(By.CSS_SELECTOR, 'div.submit button.search').click()
        print("✅ 查詢參數設定完成並執行查詢")
        sleep(2)
    except (NoSuchElementException, TimeoutException) as e:
        print(f"❌ set_drop_down_menu() 階段錯誤：{e}")
        raise


def download_csv():
    """等待 CSV 按鈕出現後點擊下載並截圖"""
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.rwd-tools button.csv'))
        )
        driver.find_element(By.CSS_SELECTOR, 'div.rwd-tools button.csv').click()
        print("✅ 已點擊下載 CSV 按鈕")
        sleep(2)

        # 擷取畫面
        ts = datetime.today().strftime('%Y%m%d%H%M%S')
        shot_path = os.path.join(folderPath, f'{ts}.png')
        driver.save_screenshot(shot_path)
        print(f"✅ 已截圖並儲存：{shot_path}")
    except TimeoutException:
        print("⚠️ download_csv() 等待超時：未找到 CSV 按鈕")
    except Exception as e:
        print(f"❌ download_csv() 階段錯誤：{e}")


def close():
    """關閉瀏覽器"""
    try:
        driver.quit()
        print("✅ 瀏覽器已關閉")
    except Exception as e:
        print(f"⚠️ close() 階段錯誤：{e}")


# --------------------
# 主程式
# --------------------
if __name__ == '__main__':
    try:
        visit()
        set_drop_down_menu()
        download_csv()
    except Exception:
        print("[FATAL] 主流程異常，程式中止")
    finally:
        close()