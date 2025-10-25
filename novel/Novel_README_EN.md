# Gutenberg Chinese eBook Batch Downloader (Requests + Selenium)

This project provides **two implementations** to batch download Chinese eBooks from
[Project Gutenberg](https://www.gutenberg.org/browse/languages/zh):

1️⃣ **`novel_bs.py`** — Static scraper using `Requests + BeautifulSoup`
2️⃣ **`novel_se.py`** — Browser automation using `Selenium WebDriver`

Both scripts fetch book metadata and plain-text content (“Plain Text UTF-8”) and save:
- `.txt` files (each book)
- `metadata.json` or `homework_meta.json` (book info)
- `train.json` (aggregated text corpus)

## 🧩 Workflow Summary

| Step | Description |
|------|--------------|
| 1 | Fetch main list from the Chinese section of Project Gutenberg |
| 2 | Extract links to each book |
| 3 | Find the **Plain Text UTF-8** link for each book |
| 4 | Download and clean text content |
| 5 | Save outputs (`.txt`, `metadata.json`, `train.json`) |

## ⚙️ File Overview

| File | Method | Description |
|------|---------|-------------|
| `novel_bs.py` | Requests + BeautifulSoup | Lightweight static HTML parsing |
| `novel_se.py` | Selenium | Full browser automation, handles dynamic pages |

## 🧠 Requirements

### For `novel_bs.py`
```bash
pip install requests beautifulsoup4 lxml
```

### For `novel_se.py`
```bash
pip install selenium
```

You also need:
- **Google Chrome**
- **ChromeDriver** (matching version)
  placed as `./chromedriver.exe` or added to PATH.

## 🪶 Output Structure

```
project_root/
├── novel_bs.py
├── novel_se.py
├── homework_bs/
│   ├── metadata.json
│   ├── *.txt
│   └── train.json
└── homework/
    ├── homework_meta.json
    ├── *.txt
    └── train.json
```

## ▶️ Usage

### 1️⃣ Static version (Requests + BS)
```bash
python novel_bs.py
```

### 2️⃣ Browser version (Selenium)
```bash
python novel_se.py
```

Each script will log progress:
```
✅ Fetched 5 book links
✅ Collected Plain Text UTF-8 links
✓ Saved: 三國演義.txt (152345 chars)
✅ train.json written
```

## ⚙️ Configuration

| Variable | Description | Default |
|-----------|-------------|----------|
| `GUTEN_URL` | Source URL | https://www.gutenberg.org/browse/languages/zh |
| `MAX_MAIN` | Number of books to fetch | 5 |
| `OUTPUT_DIR` | Output directory | homework_bs / homework |
| `SLEEP_BETW` | Delay between requests (Requests ver.) | 1.0 sec |

## ⚠️ Notes
- Some Gutenberg pages may have non-UTF8 text; handle encoding if needed.
- Selenium version is heavier but can handle layout changes.
- Use responsibly; avoid sending too many requests in a short time.
- All scripts are for **educational/research purposes** only.


