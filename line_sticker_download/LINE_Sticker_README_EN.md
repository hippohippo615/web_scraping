# LINE Sticker Downloader (Python + BeautifulSoup)

This project provides **two methods** to download LINE sticker images automatically from the [LINE Store](https://store.line.me/stickershop/product/17555/zh-Hant):

1️⃣ **Using cURL command** — via `os.system("curl ...")`  
2️⃣ **Using requests + with open()** — pure Python download

---

## 🧩 Overview
Each script performs the same sequence:

1. Create a local folder `line_stickers`  
2. Fetch the LINE Store HTML page  
3. Parse all `<li>` elements containing sticker metadata (`data-preview`)  
4. Extract sticker `id` and `staticUrl` (image URL)  
5. Download each `.png` image to the local folder

---

## ⚙️ Files
| Script | Method | Description |
|---------|---------|-------------|
| `line_sticker_curl.py` | System `curl` | Calls OS-level `curl` command for each image |
| `line_sticker_open.py` | Python `requests` | Streams image bytes and writes via `with open()` |

---

## 🪶 Example Workflow
```bash
# Run either script
python line_sticker_open.py
# or
python line_sticker_curl.py
```

Output example:
```
✅ Folder line_stickers ready
✅ Page fetched successfully (status 200)
✅ Found 40 stickers
✅ Downloaded: line_stickers/123456789.png
...
```

---

## 🧠 Requirements
| Library | Purpose |
|----------|----------|
| `requests` | HTTP GET requests |
| `beautifulsoup4` | HTML parsing |
| `lxml` | Fast parser for BeautifulSoup |

Install dependencies:
```bash
pip install requests beautifulsoup4 lxml
```

---

## ⚙️ Configuration
- **Target URL**
  ```python
  URL = 'https://store.line.me/stickershop/product/17555/zh-Hant'
  ```
  You can change `17555` to any sticker set ID.

- **Output Folder**
  Defaults to `./line_stickers`, auto-created.

---

## ⚠️ Notes
- `curl` version requires that your OS has `curl` installed.  
- `requests` version works cross-platform (Windows / macOS / Linux).  
- For educational purposes only — respect LINE’s copyright policy.

---

