# PTT Article Crawler
**Fetch article titles and full text from a PTT board using Python and BeautifulSoup**

## 🧩 Overview
This project is a **simple web crawler** for [PTT](https://www.ptt.cc/), the largest Taiwanese online forum.

It automatically:
1. Bypasses the 18+ age verification gate
2. Fetches the article list from a specific board (e.g., NBA)
3. Parses each article title and URL
4. Downloads and cleans article content by removing metadata and comments

## ⚙️ Features
✅ Maintains login session using `requests.Session()`  
✅ Automatically passes over-18 verification  
✅ Extracts all post titles and URLs from a given board  
✅ Downloads full article content (cleaned from author/time/push messages)  
✅ Uses `BeautifulSoup` (`lxml` parser) for reliable HTML parsing  

## 🧠 Requirements
| Library | Purpose |
|----------|----------|
| `requests` | Send HTTP requests |
| `beautifulsoup4` | Parse HTML |
| `lxml` | Fast HTML parser |

Install dependencies:
```bash
pip install requests beautifulsoup4 lxml
```

## 🪶 Usage
### 1️⃣ Run the crawler
```bash
python ptt_crawler.py
```
### 2️⃣ Output example
```
✅ Session initialized (passed 18+ verification)
✅ Retrieved NBA board index, status: 200
✅ Parsed 20 article links
✅ Downloaded article: “Wembanyama 30 pts Highlights”
...
```

## 📘 Project Structure
```
ptt_crawler.py
```

## 🧩 Main Functions
| Function | Description |
|-----------|-------------|
| `init_session()` | Create session and bypass 18+ page |
| `fetch_board_index(session, board)` | Fetch board index HTML |
| `parse_index(html)` | Parse titles and URLs |
| `fetch_article_content(session, url)` | Fetch and clean full article |
| `main()` | Run the whole workflow |

## ⚠️ Notes
- This script only scrapes **public PTT pages**, and should be used **for educational or research purposes** only.  
- Respect website robots.txt and fair usage policy.


