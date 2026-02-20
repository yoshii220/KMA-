# 完全無料版 JTBCサポートデスク チャットボット

このバージョンは**完全無料**で動作します！OpenAI APIキー不要です。

## 💰 コスト比較

| 項目 | OpenAI版 | 無料版（このバージョン） |
|------|----------|------------------------|
| LLM | GPT-4o-mini ($0.15/1M tokens) | Ollama (完全無料) |
| Embeddings | OpenAI Embeddings ($0.02/1M tokens) | HuggingFace (完全無料) |
| 月間コスト | $5-50 | **$0** |

## 🚀 クイックスタート

### 1. Ollamaのインストール

#### macOS / Linux:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### Windows:
https://ollama.com/download からインストーラーをダウンロード

### 2. 日本語対応モデルをダウンロード

```bash
# 軽量モデル（推奨、2GB RAM）
ollama pull gemma2:2b

# または高品質モデル（8GB RAM）
ollama pull gemma2:9b
```

### 3. 依存関係のインストール

```bash
pip install -r requirements-free.txt
```

### 4. セットアップ実行

```bash
python setup_free.py
```

### 5. アプリケーション起動

```bash
python app_free.py
```

ブラウザで `http://localhost:5000` を開く

## 📝 .env 設定（無料版）

```env
# AI設定
USE_LOCAL_LLM=true
LOCAL_LLM_MODEL=gemma2:2b

# サイト設定
TARGET_SITE_URL=https://biz.help.jtbc.info/hc/ja
UPDATE_INTERVAL_HOURS=24

# アプリケーション設定
FLASK_ENV=development
FLASK_PORT=5000
```

## 🎯 推奨モデル

### 軽量版（2-4GB RAM）
- `gemma2:2b` - 高速、低メモリ
- `phi3:mini` - Microsoft製、バランス型

### 高品質版（8GB+ RAM）
- `gemma2:9b` - 高品質な回答
- `llama3.1:8b` - Meta製、汎用性高い

## 💡 使い方

OpenAI版と全く同じUI/機能ですが、全て無料です！

### モデルの切り替え

`.env`ファイルで簡単に切り替え可能：

```env
# 軽量高速モデル
LOCAL_LLM_MODEL=gemma2:2b

# 高品質モデル
LOCAL_LLM_MODEL=gemma2:9b
```

## ⚙️ ハイブリッド構成

必要に応じてOpenAIと切り替え可能：

```env
# ローカルLLMを使用
USE_LOCAL_LLM=true

# OpenAIを使用（APIキーが必要）
USE_LOCAL_LLM=false
OPENAI_API_KEY=sk-your-key-here
```

## 🔧 トラブルシューティング

### Ollamaが起動しない
```bash
# Ollamaを手動起動
ollama serve
```

### メモリ不足
より軽量なモデルを使用：
```bash
ollama pull phi3:mini
```

### 日本語の品質が低い
より大きなモデルを試してください：
```bash
ollama pull gemma2:9b
```

## 📊 パフォーマンス比較

| モデル | メモリ | 速度 | 品質 | 日本語 |
|--------|--------|------|------|--------|
| gemma2:2b | 2GB | ⚡⚡⚡ | ⭐⭐⭐ | ⭐⭐⭐ |
| gemma2:9b | 8GB | ⚡⚡ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| GPT-4o-mini | N/A | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 🎉 メリット

- ✅ **完全無料** - APIキー不要
- ✅ **プライバシー** - データが外部に送信されない
- ✅ **オフライン** - インターネット不要（クロール後）
- ✅ **カスタマイズ** - モデルを自由に選択
- ✅ **コスト予測可能** - 使用量による追加料金なし

## ⚠️ 注意点

- 初回モデルダウンロードに数分かかります
- OpenAI版より回答品質が若干低い場合があります
- PCのスペックに応じてモデルを選択してください
