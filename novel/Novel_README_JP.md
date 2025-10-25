# グーテンベルク中文電子書バッチダウンローダ（Requests + Selenium）

本プロジェクトは、[Project Gutenberg](https://www.gutenberg.org/browse/languages/zh) の
中文電子書を自動でダウンロードする **2 つの実装** を提供します。

1️⃣ **`novel_bs.py`** — `Requests + BeautifulSoup` を用いた静的スクレイピング版
2️⃣ **`novel_se.py`** — `Selenium WebDriver` を用いたブラウザ自動化版

どちらも以下のファイルを出力します：
- 各書籍の `.txt` ファイル
- 書誌情報の `metadata.json` または `homework_meta.json`
- 全文データを集約した `train.json`

## 🧩 処理の流れ

| ステップ | 内容 |
|-----------|------|
| 1 | グーテンベルク中文ページから書籍リストを取得 |
| 2 | 各書籍ページへのリンクを抽出 |
| 3 | 各書籍ページから **Plain Text UTF-8** リンクを検索 |
| 4 | テキストをダウンロードして整形 |
| 5 | `.txt`, `metadata.json`, `train.json` を保存 |

## ⚙️ ファイル概要

| ファイル | 方法 | 説明 |
|-----------|------|------|
| `novel_bs.py` | Requests + BeautifulSoup | 軽量な静的 HTML パーサー |
| `novel_se.py` | Selenium | ブラウザ操作による自動化版 |

## 🧠 必要環境

### `novel_bs.py` 用
```bash
pip install requests beautifulsoup4 lxml
```

### `novel_se.py` 用
```bash
pip install selenium
```

さらに以下が必要です：
- **Google Chrome**
- **ChromeDriver**（バージョンを Chrome に合わせて）
  → `./chromedriver.exe` に配置、または PATH に追加。

## 🪶 出力構成

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

## ▶️ 実行方法

### 1️⃣ 静的版（Requests + BS）
```bash
python novel_bs.py
```

### 2️⃣ ブラウザ版（Selenium）
```bash
python novel_se.py
```

出力例：
```
✅ 5 件の書籍リンクを取得
✅ Plain Text UTF-8 リンクを収集
✓ 出力：三国演義.txt (152345文字)
✅ train.json を保存
```

## ⚙️ 設定項目

| 変数 | 内容 | デフォルト値 |
|------|------|---------------|
| `GUTEN_URL` | ソースURL | https://www.gutenberg.org/browse/languages/zh |
| `MAX_MAIN` | 取得書籍数 | 5 |
| `OUTPUT_DIR` | 出力フォルダ | homework_bs / homework |
| `SLEEP_BETW` | リクエスト間隔（Requests版） | 1.0 秒 |

## ⚠️ 注意事項
- 一部の書籍は UTF-8 以外の文字コードを使用している可能性があります。
- Selenium 版は重いですが、ページ構造変更に強いです。
- アクセス頻度を控えめにし、グーテンベルクの利用規約を遵守してください。
- 本スクリプトは **学習・研究目的専用** です。

