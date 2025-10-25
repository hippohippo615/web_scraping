# YouTube Video Crawler & Downloader (Selenium + yt-dlp)

This project includes two scripts for **automated video scraping and downloading** from YouTube.

| File | Function | Description |
|------|-----------|-------------|
| `youtube.py` | Scraper | Collects YouTube video metadata — title, thumbnail, link, video ID — and saves to `youtube.json`. |
| `youtube_download.py` | Full version | Performs scraping + downloads top videos using `yt-dlp`. |

## 🧩 Features

✅ Headless Chrome automation  
✅ Auto search by keyword (default: “張學友”)  
✅ Scroll and load dynamic results  
✅ Parse title, thumbnail, video ID, and URL  
✅ Save structured JSON output  
✅ Download videos as MP4 using `yt-dlp`  

## ⚙️ Requirements

| Library | Purpose |
|----------|----------|
| `selenium` | Web browser automation |
| `yt-dlp` | Video download |
| `json`, `os`, `subprocess` | File I/O and system commands |

Install dependencies:
```bash
pip install selenium yt-dlp
```

> Requires **Google Chrome** and a matching **ChromeDriver** (placed in the same folder or PATH).

## 🪶 Workflow

1️⃣ **Launch Chrome WebDriver**  
2️⃣ **Open YouTube and search “張學友”**  
3️⃣ **Scroll the page and collect results**  
4️⃣ **Extract title / link / image / video ID**  
5️⃣ **Save results to `youtube.json`**  
6️⃣ *(In downloader version)* — read JSON and download first 4 videos via `yt-dlp`.

## ▶️ Usage

### 1️⃣ Run the scraper only
```bash
python youtube.py
```

Output:
```
✅ ChromeDriver started
✅ Opened YouTube homepage
✅ Input keyword '張學友'
✅ Found 20 videos
✅ Saved youtube/youtube.json
```

### 2️⃣ Run scraper + downloader
```bash
python youtube_download.py
```

Example log:
```
🎯 abcd1234 張學友 - 吻別 (官方版)
📥 yt-dlp output:
[download] Downloading video 1 of 4
[download] Destination: youtube/張學友 - 吻別.mp4
[download] 100% of 5.03MiB in 00:10
```

## 📂 Output Structure

```
project_root/
├── youtube.py
├── youtube_download.py
├── chromedriver.exe
├── yt-dlp.exe
└── youtube/
    ├── youtube.json
    ├── 張學友 - 吻別.mp4
    └── ...
```

### `youtube.json` Example
```json
[
  {
    "id": "abcd1234",
    "title": "張學友 - 吻別 (官方版)",
    "link": "https://www.youtube.com/watch?v=abcd1234",
    "img": "https://i.ytimg.com/vi/abcd1234/hqdefault.jpg"
  }
]
```

## ⚠️ Notes

- Some elements may fail to load due to region or dynamic content — the script includes error handling to continue scraping.  
- `yt-dlp.exe` must be in the project directory or PATH.  
- Use only for **educational/research purposes** — follow YouTube’s terms of service.  


