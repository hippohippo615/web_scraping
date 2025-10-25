# TWSE Foreign Institutional Investors CSV Downloader (Selenium)

Automate the TWSE page **外資及陸資買賣超彙總** to select a date, run the search, download the **CSV**, and save a **screenshot**.

## ✨ Features
- Launches Chrome with custom download folder (no prompts)
- Auto-passes site UI, selects **year / month / day**
- Clicks **CSV** button and waits for file to appear
- Saves a timestamped **screenshot** of the result page
- Graceful startup/shutdown with clear logs

## 🧩 How it works (flow)
1. Initialize Chrome (`requests` not used here; Selenium only).
2. Open TWSE page: `https://www.twse.com.tw/zh/page/trading/fund/TWT38U.html`
3. Select **year 2011**, **month 02**, **day index 8** (＝the 9th day) via `<select>` elements.
4. Click **Search** → wait for results.
5. Click **CSV** → file downloads into `./files/`.
6. Save screenshot to `./files/<timestamp>.png`.

> Date selectors are currently hard-coded in `set_drop_down_menu()`; adjust to your needs.

## 🛠 Requirements
- **Google Chrome** (stable)
- **ChromeDriver** that matches your Chrome version  
  (script expects `./chromedriver.exe` on Windows; adjust path for Mac/Linux)
- **Python 3.9+**
- Python packages:
  ```bash
  pip install selenium
  ```

> Optional: use `webdriver-manager` to avoid manual chromedriver:
> ```bash
> pip install webdriver-manager
> ```
> and replace the driver init with:
> ```python
> from selenium.webdriver.chrome.service import Service
> from webdriver_manager.chrome import ChromeDriverManager
> driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
> ```

## 📂 Project layout
```
your_project/
├─ chromedriver.exe
├─ twse_downloader.py
└─ files/
```

## ⚙️ Configuration
- **Download folder**: change `folderPath = 'files'`
- **Date**: edit `set_drop_down_menu()`:
  - `select_by_value('2011')`  → year
  - `select_by_visible_text('02月')` → month
  - `select_by_index(8)` → day (0-based index)
- **Headless mode** (optional):
  ```python
  options.add_argument("--headless=new")
  ```

## ▶️ Run
```bash
python twse_downloader.py
```

Console output example:
```
✅ Chrome 截圖及下載實例啟動成功
✅ 開啟主頁成功
✅ 查詢參數設定完成並執行查詢
✅ 已點擊下載 CSV 按鈕
✅ 已截圖並儲存：files/20250101XXXXXX.png
✅ 瀏覽器已關閉
```

## 🔍 Troubleshooting
- **`SessionNotCreatedException` / version mismatch** → Update ChromeDriver to match Chrome version.
- **CSV button timeout** → Update CSS selectors if the page layout changes.
- **Downloads blocked** → Ensure `"download.default_directory"` is valid.

## ⚖️ Notice
For educational and personal use. Respect TWSE site policy.
