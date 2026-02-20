# JTBCサポートデスク チャットボット

JTBCのサポートサイト（https://biz.help.jtbc.info/hc/ja）の情報を活用したAIチャットボットです。

## 特徴

🤖 **自然な対話**: OpenAI GPTを使用した自然言語での回答  
🔄 **自動更新**: サイトの情報を定期的に自動取得  
📚 **情報源表示**: 回答のソースとなった記事を表示  
💻 **使いやすいUI**: モダンでレスポンシブなWebインターフェース  

## 技術スタック

### バックエンド
- **Python 3.8+**
- **Flask**: Webフレームワーク
- **LangChain**: RAG（Retrieval-Augmented Generation）実装
- **ChromaDB**: ベクトルデータベース
- **BeautifulSoup4**: Webスクレイピング
- **APScheduler**: 定期実行スケジューラー

### フロントエンド
- **HTML5/CSS3**
- **Vanilla JavaScript**
- **レスポンシブデザイン**

## セットアップ手順

### 1. 依存関係のインストール

```bash
# Python 3.8以上が必要です
python --version

# 依存パッケージをインストール
pip install -r requirements.txt
```

### 2. 環境変数の設定

`.env.example`をコピーして`.env`ファイルを作成します：

```bash
cp .env.example .env
```

`.env`ファイルを編集し、OpenAI APIキーを設定します：

```env
OPENAI_API_KEY=sk-your-api-key-here
TARGET_SITE_URL=https://biz.help.jtbc.info/hc/ja
UPDATE_INTERVAL_HOURS=24
FLASK_ENV=development
FLASK_PORT=5000
```

### 3. 初期データの取得

初回起動時に以下のコマンドを実行して、サイトのデータをクロールします：

```bash
python setup.py
```

このスクリプトは以下を実行します：
- JTBCサポートサイトから記事を取得
- データをJSONファイルに保存
- ベクトルインデックスを作成

### 4. アプリケーションの起動

```bash
python app.py
```

ブラウザで `http://localhost:5000` にアクセスしてください。

## 使い方

### チャットボット

1. Webインターフェースで質問を入力
2. 送信ボタンをクリック
3. AIが関連情報を検索して回答
4. 参考情報のリンクも表示されます

### サジェスト質問

よくある質問がボタンとして表示されます。クリックすると自動的に質問が入力されます。

### データの更新

- **自動更新**: デフォルトで24時間ごとに自動更新
- **手動更新**: フッターの「データを更新」ボタンをクリック

## プロジェクト構造

```
.
├── app.py                 # Flaskアプリケーション
├── setup.py              # 初期セットアップスクリプト
├── requirements.txt      # Python依存パッケージ
├── .env.example         # 環境変数のテンプレート
├── .gitignore           # Git除外設定
├── README.md            # このファイル
├── src/
│   ├── __init__.py
│   ├── crawler.py       # Webクローラー
│   ├── vector_store.py  # ベクトルストア管理
│   ├── chatbot.py       # チャットボットロジック
│   └── scheduler.py     # 定期更新スケジューラー
├── templates/
│   └── index.html       # HTMLテンプレート
├── static/
│   ├── css/
│   │   └── style.css    # スタイルシート
│   └── js/
│       └── app.js       # クライアントサイドJS
└── data/
    └── articles.json    # クロールされた記事データ
```

## API エンドポイント

### POST `/api/chat`
チャットメッセージを送信して回答を取得

**リクエスト:**
```json
{
  "question": "総務省への届出について教えてください"
}
```

**レスポンス:**
```json
{
  "answer": "回答テキスト...",
  "sources": [
    {
      "title": "記事タイトル",
      "url": "記事URL",
      "category": "カテゴリ名",
      "excerpt": "抜粋..."
    }
  ]
}
```

### GET `/api/suggestions`
サジェスト質問を取得

### GET `/api/status`
システムステータスを取得

### POST `/api/update`
データ更新を手動でトリガー

## カスタマイズ

### 更新頻度の変更

`.env`ファイルで更新間隔を変更できます：

```env
UPDATE_INTERVAL_HOURS=12  # 12時間ごとに更新
```

### AIモデルの変更

`src/chatbot.py`の`JTBCSupportChatbot`クラスでモデルを変更できます：

```python
self.llm = ChatOpenAI(
    temperature=0.7,
    model="gpt-4",  # または "gpt-3.5-turbo"
    openai_api_key=openai_api_key
)
```

### プロンプトのカスタマイズ

`src/chatbot.py`の`prompt_template`を編集して、チャットボットの応答スタイルを変更できます。

## トラブルシューティング

### OpenAI APIキーエラー
```
Error: OPENAI_API_KEY not found
```
→ `.env`ファイルにAPIキーを正しく設定してください

### クロールエラー
```
Error fetching articles
```
→ インターネット接続を確認してください  
→ サイトがアクセス可能か確認してください

### ベクトルストアエラー
```
Error initializing vector store
```
→ `chroma_db`ディレクトリを削除して再度`setup.py`を実行してください

## 開発

### 開発モードでの起動

```bash
export FLASK_ENV=development
python app.py
```

### テストの実行

各モジュールを個別にテストできます：

```bash
# クローラーのテスト
python src/crawler.py

# ベクトルストアのテスト
python src/vector_store.py

# チャットボットのテスト
python src/chatbot.py
```

## ライセンス

このプロジェクトは個人使用のために作成されています。

## 作成者

yoshii220

## 注意事項

- このチャットボットはJTBCサポートサイトの情報を基に回答しますが、100%の正確性を保証するものではありません
- 重要な決定を行う前に、公式サイトで最新情報を確認してください
- OpenAI APIの使用には料金が発生します
- Webスクレイピングは利用規約に従って行ってください
