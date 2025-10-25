# Zeczec クラウドファンディング スクレイパー（Selenium + BeautifulSoup）

台湾のクラウドファンディングサイト
**[嘖嘖（Zeczec）](https://www.zeczec.com/)** から
プロジェクトデータを自動収集するための **3 つの Python スクリプト** を提供します。

## 🧩 概要

| ファイル名 | 機能 | 説明 |
|-------------|------|------|
| `scrape_funding_title_image_link.py` | ステップ1 | 各プロジェクトの **タイトル・画像URL・リンク** を取得し、`data.json` に保存。 |
| `scrape_funding_goal_backers_days.py` | ステップ2 | `data.json` を読み込み、**目標金額・集資金額・支援者数・残り日数・期間** を追加。 |
| `scrape_crowdfunding_all_details.py` | ステップ3 | 上記 2 つの処理を自動実行し、完全なデータセットを生成。 |

## ⚙️ 特徴

✅ **ヘッドレス Chrome** による自動化  
✅ **CAPTCHA** 検知＆スクリーンショット保存  
✅ **BeautifulSoup** による HTML 構造解析  
✅ **JSON 出力** によるデータ再利用  
✅ リクエスト間隔を調整可能 (`SLEEP_BETWEEN`)

## 🪶 処理の流れ

1️⃣ **プロジェクト概要の取得**  
- カテゴリーページを巡回し、`title`、`cover image`、`link` を収集  

2️⃣ **詳細情報の追加**  
- 各プロジェクトページにアクセスして以下を抽出：  
  - 目標金額・集資金額  
  - 支援者数  
  - 残り日数  
  - 開始／終了日時  

3️⃣ **データ保存**  
- 出力ファイル：`data.json`

## 🧠 必要環境

| ライブラリ | 用途 |
|-------------|------|
| `selenium` | ブラウザ自動操作 |
| `beautifulsoup4` | HTML 解析 |
| `lxml` | 高速 HTML パーサー |
| `json`, `re`, `time`, `random` | 標準ライブラリ |

インストール：
```bash
pip install selenium beautifulsoup4 lxml
```

> **Google Chrome** と **ChromeDriver**（バージョン一致）を用意してください。

## ▶️ 実行方法

### 手動ステップ実行
```bash
python scrape_funding_title_image_link.py
python scrape_funding_goal_backers_days.py
```

### 一括自動実行
```bash
python scrape_crowdfunding_all_details.py
```

出力例：
```
✅ 40 件のプロジェクトを取得
✅ 各プロジェクトの詳細情報を追加
✅ data.json に保存しました
```

## 📂 出力例 (`data.json`)

```json
[
  {
    "title": "エコバッグプロジェクト",
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

## ⚠️ 注意事項
- CAPTCHA（認証ページ）が表示された場合、`debug_block_*.png` にスクリーンショットを保存します。  
- `SLEEP_BETWEEN` 変数を調整してアクセス頻度をコントロール可能です。  
- 本スクリプトは **学習・研究目的専用** です。Zeczec の利用規約を遵守してください。  

