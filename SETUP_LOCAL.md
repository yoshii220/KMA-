# ローカル環境セットアップガイド

## 📋 前提条件

- Python 3.8以上
- JTBCサポートサイトのアカウント（ログイン情報）

## 🚀 セットアップ手順

### 1. リポジトリをクローン

```bash
git clone https://github.com/yoshii220/KMA-.git
cd KMA-
```

### 2. 仮想環境を作成（推奨）

```bash
# 仮想環境を作成
python -m venv venv

# 仮想環境を有効化
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. 依存関係をインストール

```bash
pip install -r requirements-gemini.txt
```

### 4. 環境変数を設定

```bash
# テンプレートをコピー
cp .env.example.gemini .env
```

`.env`ファイルを編集して以下を設定：

```env
# Google Gemini API Key
GEMINI_API_KEY=あなたのGemini APIキー

# Geminiモデル設定
GEMINI_MODEL=gemini-pro

# JTBCサポートサイトのログイン情報
JTBC_LOGIN_EMAIL=あなたのメールアドレス
JTBC_LOGIN_PASSWORD=あなたのパスワード

# サイト設定
TARGET_SITE_URL=https://biz.help.jtbc.info/hc/ja
UPDATE_INTERVAL_HOURS=24

# アプリケーション設定
FLASK_ENV=development
FLASK_PORT=5000
```

### 5. 記事をクロール

```bash
# ログイン機能付きクローラーでデータを取得
python src/crawler_with_login.py
```

成功すると `data/articles.json` にデータが保存されます。

### 6. ベクトルインデックスを作成

```bash
python -c "
from src.vector_store_free import VectorStoreManager
vs = VectorStoreManager(use_free=True)
vs.load_or_create_vectorstore()
vs.update_index('data/articles.json')
print('✅ ベクトル化完了！')
"
```

### 7. アプリケーションを起動

```bash
python app_gemini.py
```

ブラウザで `http://localhost:5000` にアクセス

## 🔧 トラブルシューティング

### ログインエラー

```
❌ Login failed. Please check your credentials.
```

**解決方法:**
1. `.env`ファイルのメールアドレスとパスワードを確認
2. JTBCサポートサイトで直接ログインできるか確認
3. パスワードに特殊文字がある場合は引用符で囲む

### クロールできない

```
No articles were crawled.
```

**解決方法:**
1. ログイン情報が正しいか確認
2. サイトの構造が変わっていないか確認
3. `src/crawler_with_login.py`のセレクタを調整

### Gemini APIエラー

```
Error: Invalid API key
```

**解決方法:**
1. https://makersuite.google.com/app/apikey で新しいキーを取得
2. `.env`のGEMINI_API_KEYを更新

## 💡 ヒント

### データの確認

```bash
# 取得した記事数を確認
python -c "
import json
with open('data/articles.json') as f:
    data = json.load(f)
print(f'記事数: {len(data)}')
"
```

### ベクトルストアの確認

```bash
# インデックスされたドキュメント数を確認
python -c "
from src.vector_store_free import VectorStoreManager
vs = VectorStoreManager(use_free=True)
vs.load_or_create_vectorstore()
print(f'✅ ベクトルストアが読み込まれました')
"
```

## 🔒 セキュリティ

- `.env`ファイルは**絶対にGitHubにプッシュしない**
- `.gitignore`で既に除外されています
- パスワードは暗号化されて保存されません（ローカルのみ）

## 📚 参考

- [README-GEMINI.md](README-GEMINI.md) - Gemini版の詳細
- [README-FREE.md](README-FREE.md) - 完全無料版（Ollama）
- [README.md](README.md) - OpenAI版
