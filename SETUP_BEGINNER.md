# 超初心者向けセットアップガイド

## 📱 Step 1: Pythonをインストール

### Windows の場合

1. https://www.python.org/downloads/ にアクセス
2. 黄色い「Download Python」ボタンをクリック
3. ダウンロードしたファイルをダブルクリック
4. **重要**: 「Add Python to PATH」に✓を入れる
5. 「Install Now」をクリック

### Mac の場合

1. https://www.python.org/downloads/ にアクセス
2. 「Download Python」ボタンをクリック
3. ダウンロードした.pkgファイルをダブルクリック
4. 指示に従ってインストール

---

## 📱 Step 2: コードをダウンロード

### 方法A: GitHubからZIPでダウンロード（簡単！）

1. https://github.com/yoshii220/KMA- にアクセス
2. 緑色の「Code」ボタンをクリック
3. 「Download ZIP」をクリック
4. ダウンロードしたZIPファイルを解凍
5. 解凍したフォルダ「KMA--main」を開く

### 方法B: Git経由（少し難しい）

```bash
# ターミナル/コマンドプロンプトで実行
git clone https://github.com/yoshii220/KMA-.git
cd KMA-
```

---

## 📱 Step 3: 必要なプログラムをインストール

### Windows の場合

1. ダウンロードしたフォルダを開く
2. フォルダ内で「Shift + 右クリック」
3. 「PowerShellウィンドウをここで開く」または「コマンドウィンドウをここで開く」を選択
4. 以下をコピー＆ペーストしてEnter:

```bash
pip install -r requirements-gemini.txt
```

### Mac の場合

1. ダウンロードしたフォルダを見つける
2. ターミナルで以下を実行:

```bash
cd /Users/あなたのユーザー名/Downloads/KMA--main
pip3 install -r requirements-gemini.txt
```

---

## 📱 Step 4: 設定ファイルを作る

### Windows の場合

1. フォルダ内の「.env.example.gemini」を探す
2. 右クリック → 「名前を変更」
3. 「.env」に変更（拡張子表示がない場合は設定から有効化）
4. メモ帳で開く
5. 以下を編集:

```
GEMINI_API_KEY=ここにあなたのGemini APIキーを貼り付け
JTBC_LOGIN_EMAIL=あなたのメールアドレス
JTBC_LOGIN_PASSWORD=あなたのパスワード
```

### Mac の場合

ターミナルで:

```bash
cp .env.example.gemini .env
nano .env
```

編集して保存（Ctrl+X → Y → Enter）

---

## 📱 Step 5: サイトから記事を取得

ターミナル/コマンドプロンプトで:

```bash
python src/crawler_with_login.py
```

成功すると「✅ Successfully crawled XX articles!」と表示されます。

---

## 📱 Step 6: チャットボットを起動

```bash
python app_gemini.py
```

ブラウザで http://localhost:5000 を開く

---

## 🆘 困ったら

### エラーが出る場合

#### 「python: command not found」

→ Pythonがインストールされていません。Step 1へ

#### 「pip: command not found」

→ 以下を試してください:

```bash
python -m pip install -r requirements-gemini.txt
```

#### 「Permission denied」(Mac/Linux)

→ 先頭に `sudo` を付ける:

```bash
sudo pip3 install -r requirements-gemini.txt
```

### ファイルが見つからない

フォルダの場所を確認:

**Windows:**
```bash
cd C:\Users\あなたの名前\Downloads\KMA--main
```

**Mac:**
```bash
cd ~/Downloads/KMA--main
```

---

## 🎥 スクリーンショット付き手順（Windows例）

### 1. フォルダを開く
[ダウンロードフォルダ] → [KMA--main]

### 2. PowerShellを開く
フォルダ内で Shift + 右クリック → "PowerShellウィンドウをここで開く"

### 3. コマンドを実行
```powershell
pip install -r requirements-gemini.txt
```

### 4. .envファイルを作成
.env.example.gemini を .env にリネーム

### 5. メモ帳で編集
APIキーとログイン情報を入力

### 6. 実行
```powershell
python src\crawler_with_login.py
python app_gemini.py
```

---

## 💡 もっと簡単な方法が必要ですか？

スクリーンショットを送っていただければ、具体的にアドバイスできます！
