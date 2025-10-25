# TWSE 外資買越・売越 CSV 自動ダウンローダ（Selenium）

TWSE のページ **「外資及び大陸資の売買超集計」** を自動操作して、日付を選択 → 検索 → **CSV をダウンロード** → **スクリーンショット保存** まで行います。

## ✨ 特長
- ダウンロードフォルダを自動設定（ダイアログなし）
- 年／月／日を自動選択して検索実行
- **CSV** ボタンをクリックして保存
- 結果ページをタイムスタンプ付きで **PNG** 保存
- 起動・終了時にログ出力

## 🧩 処理の流れ
1. Chrome を Selenium で起動  
2. `https://www.twse.com.tw/zh/page/trading/fund/TWT38U.html` を開く  
3. 年（2011）、月（02月）、日（index 8＝9日）を `<select>` から選択  
4. **検索** をクリックして結果を待機  
5. **CSV** をクリック → `./files/` に保存  
6. スクリーンショットを `./files/<timestamp>.png` に保存  

> 日付は `set_drop_down_menu()` 内でハードコーディングされています。必要に応じて変更してください。

## 🛠 必要環境
- **Google Chrome**
- **ChromeDriver**（Chrome バージョンと一致）  
  （Windows は `./chromedriver.exe`、Mac/Linux は PATH に設定）
- **Python 3.9+**
- 必要パッケージ：
  ```bash
  pip install selenium
  ```

> webdriver-manager を使うと自動ダウンロード可能：
> ```bash
> pip install webdriver-manager
> ```
> 初期化を次のように変更：
> ```python
> from selenium.webdriver.chrome.service import Service
> from webdriver_manager.chrome import ChromeDriverManager
> driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
> ```

## 📂 構成
```
your_project/
├─ chromedriver.exe
├─ twse_downloader.py
└─ files/
```

## ⚙️ 設定
- **保存フォルダ**：`folderPath = 'files'` を変更可能  
- **日付選択**：`set_drop_down_menu()` を編集  
  - `select_by_value('2011')`（年）  
  - `select_by_visible_text('02月')`（月）  
  - `select_by_index(8)`（日・0始まり）  
- **ヘッドレス実行**（任意）：
  ```python
  options.add_argument("--headless=new")
  ```

## ▶️ 実行
```bash
python twse_downloader.py
```

出力例：
```
✅ Chrome 起動成功
✅ ページを開きました
✅ 年月日を選択して検索実行
✅ CSV ボタンをクリック
✅ スクリーンショット保存：files/20250101XXXXXX.png
✅ ブラウザを閉じました
```

## 🔍 トラブルシューティング
- **`SessionNotCreatedException` / バージョン不一致** → ChromeDriver を更新
- **CSV ボタンが見つからない** → CSS セレクタ変更を確認
- **ダウンロード不可** → `"download.default_directory"` を確認

## ⚖️ 注意事項
学習・個人利用を想定。TWSE の利用規約を遵守してください。
