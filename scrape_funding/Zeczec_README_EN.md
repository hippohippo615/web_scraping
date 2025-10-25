# Zeczec Crowdfunding Scraper (Selenium + BeautifulSoup)

This project automates data scraping from the Taiwanese crowdfunding site
**[Zeczec](https://www.zeczec.com/)**.
It provides **three complementary scripts** that together form a complete data pipeline.

## 🧩 Overview

| File | Function | Description |
|------|-----------|-------------|
| `scrape_funding_title_image_link.py` | Step 1 | Fetches **project title**, **image URL**, and **project link** from the homepage. Saves to `data.json`. |
| `scrape_funding_goal_backers_days.py` | Step 2 | Loads `data.json` and adds **funding goal, raised amount, backer count, remaining days, and project duration**. |
| `scrape_crowdfunding_all_details.py` | Step 3 | Full automation — performs both steps at once, outputting a complete dataset. |

## ⚙️ Features

✅ Uses **headless Chrome** with anti-bot evasion  
✅ Extracts structured data (titles, links, metrics)  
✅ Saves JSON output for further analysis  
✅ Detects CAPTCHA / verification pages and saves debug screenshots  
✅ Adjustable sleep delays for rate control  

## 🪶 Workflow Summary

1️⃣ **Collect project overview**  
   - Visit category pages  
   - Extract `title`, `cover image`, `project link`

2️⃣ **Collect project details**  
   - Open each project link  
   - Extract:
     - Funding goal & raised amount  
     - Backers count  
     - Remaining days  
     - Start–end date range  

3️⃣ **Save results**  
   - Output: `data.json`

## 🧠 Requirements

| Library | Purpose |
|----------|----------|
| `selenium` | Headless browser automation |
| `beautifulsoup4` | HTML parsing |
| `lxml` | Fast HTML parser |
| `json`, `re`, `time`, `random` | Built-in utilities |

Install dependencies:
```bash
pip install selenium beautifulsoup4 lxml
```

> Make sure you have **Google Chrome** and a matching **ChromeDriver** installed.

## ▶️ Usage

### Option 1 — Step-by-step
```bash
python scrape_funding_title_image_link.py
python scrape_funding_goal_backers_days.py
```

### Option 2 — All-in-one
```bash
python scrape_crowdfunding_all_details.py
```

Example output:
```
✅ Collected 40 projects
✅ Updated each project with funding details
✅ Saved data.json (40 records)
```

## 📂 Output Example (`data.json`)

```json
[
  {
    "title": "New Eco Bag Project",
    "cover": "https://assets.zeczec.com/asset_12345_image_big.jpg",
    "link": "https://www.zeczec.com/projects/eco-bag",
    "TargetPrice": 500000,
    "PastPrice": 650000,
    "Backers": 320,
    "TimeLeftDays": 5,
    "Duration": {
      "begin": "2024/10/01 12:00",
      "end": "2024/11/15 23:59"
    }
  }
]
```

## ⚠️ Notes
- Some projects may trigger CAPTCHA; debug screenshots are saved as `debug_block_*.png`.  
- Adjust `SLEEP_BETWEEN` or `PAGES` constants to control request rate.  
- For research or educational use only — respect Zeczec’s site policy.  

