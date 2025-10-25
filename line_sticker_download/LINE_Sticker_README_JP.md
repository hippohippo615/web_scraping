# LINE スタンプ自動ダウンローダ（Python + BeautifulSoup）

本プロジェクトは、[LINE ストア](https://store.line.me/stickershop/product/17555/zh-Hant) から
スタンプ画像を自動でダウンロードする **2 種類の方法** を提供します。

1️⃣ **cURL コマンド方式** — `os.system("curl ...")` を利用  
2️⃣ **requests + with open() 方式** — Python 標準ライブラリのみで実装

---

## 🧩 概要
両方のスクリプトで行う流れは同じです：

1. フォルダ `line_stickers` を作成  
2. LINE ストアの HTML ページを取得  
3. `<li data-preview="...">` 要素を解析  
4. 各スタンプの `id` と `staticUrl`（画像 URL）を抽出  
5. `.png` 画像をローカルに保存  

---

## ⚙️ ファイル構成
| スクリプト名 | 方式 | 説明 |
|---------------|------|------|
| `line_sticker_curl.py` | cURL コマンド | OS コマンドとして cURL を呼び出してダウンロード |
| `line_sticker_open.py` | requests + open | Python 標準でストリーム保存 |

---

## 🪶 使用方法
```bash
# どちらかを実行
python line_sticker_open.py
# または
python line_sticker_curl.py
```

出力例：
```
✅ フォルダ line_stickers 準備完了
✅ ページ取得成功 (status 200)
✅ 40 件のスタンプを検出
✅ ダウンロード完了: line_stickers/123456789.png
...
```

---

## 🧠 必要ライブラリ
| ライブラリ | 用途 |
|-------------|------|
| `requests` | HTTP 通信 |
| `beautifulsoup4` | HTML 解析 |
| `lxml` | 高速 HTML パーサー |

インストール：
```bash
pip install requests beautifulsoup4 lxml
```

---

## ⚙️ 設定
- **対象 URL**
  ```python
  URL = 'https://store.line.me/stickershop/product/17555/zh-Hant'
  ```
  `17555` を他のスタンプセット ID に変更できます。

- **出力フォルダ**
  デフォルト：`./line_stickers`（自動作成）

---

## ⚠️ 注意事項
- cURL 方式を使う場合、OS に `curl` コマンドがインストールされている必要があります。  
- requests 方式は OS に依存せず動作します。  
- 本スクリプトは **学習・研究目的** に限り使用してください。LINE の著作権ポリシーに従ってください。

---

