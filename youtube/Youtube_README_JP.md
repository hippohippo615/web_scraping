# YouTube 動画クローラー＆ダウンローダ（Selenium + yt-dlp）

本プロジェクトは **YouTube から自動的に動画情報を取得・ダウンロード** する  
2 つの Python スクリプトを含みます。

| ファイル名 | 役割 | 説明 |
|-------------|------|------|
| `youtube.py` | クローラー | YouTube 検索結果から **タイトル・サムネイル・リンク・動画ID** を取得し、`youtube.json` に保存。 |
| `youtube_download.py` | 完全版 | 上記のスクレイピング後、自動で上位数件の動画を `yt-dlp` で MP4 形式にダウンロード。 |

## 🧩 特徴

✅ Chrome（ヘッドレス対応）で自動操作  
✅ キーワード検索（デフォルト：「張學友」）  
✅ 動的スクロールで動画を読み込み  
✅ JSON 形式でデータ保存  
✅ `yt-dlp` による自動ダウンロード  

## ⚙️ 必要環境

| ライブラリ | 用途 |
|-------------|------|
| `selenium` | ブラウザ自動操作 |
| `yt-dlp` | 動画ダウンロード |
| `json`, `os`, `subprocess` | ファイル操作・システム実行 |

インストール：
```bash
pip install selenium yt-dlp
```

> **Google Chrome** と **ChromeDriver**（同じバージョン）を事前に準備してください。

## 🪶 処理の流れ

1️⃣ ChromeDriver を起動  
2️⃣ YouTube を開き「張學友」で検索  
3️⃣ ページをスクロールして動画情報を収集  
4️⃣ タイトル／リンク／サムネイル／動画IDを抽出  
5️⃣ `youtube.json` に保存  
6️⃣ （ダウンローダ版）`yt-dlp` で動画を MP4 として保存  

## ▶️ 実行方法

### クローラーのみ実行
```bash
python youtube.py
```

出力例：
```
✅ ChromeDriver 起動成功
✅ YouTube ホームページを開きました
✅ キーワード「張學友」を入力
✅ 20 本の動画を検出
✅ youtube/youtube.json に保存
```

### クローラー＋ダウンローダ実行
```bash
python youtube_download.py
```

出力例：
```
🎯 abcd1234 張學友 - 吻別 (官方版)
📥 yt-dlp 出力：
[download] Downloading video 1 of 4
[download] Destination: youtube/張學友 - 吻別.mp4
[download] 100% of 5.03MiB in 00:10
```

## 📂 出力構成

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

### `youtube.json` の例
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

## ⚠️ 注意事項
- 地域や動的要素によって、一部の要素が読み込めない場合があります（スクリプトには例外処理を実装済み）。  
- `yt-dlp.exe` はプロジェクトフォルダ内または PATH に配置してください。  
- 本スクリプトは **学習・研究目的限定** です。YouTube の利用規約を遵守してください。  

