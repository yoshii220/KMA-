#!/usr/bin/env python3
"""
初期セットアップスクリプト（Gemini版）
HuggingFace Embeddings（無料）+ Google Gemini
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.crawler import JTBCSupportCrawler
from src.vector_store_free import VectorStoreManager

def main():
    print("=" * 60)
    print("JTBCサポートデスク チャットボット - Gemini版セットアップ")
    print("=" * 60)
    print()
    print("💡 このバージョンの特徴:")
    print("   - Embeddings: HuggingFace（完全無料、無制限）")
    print("   - LLM: Google Gemini（無料枠60リクエスト/月）")
    print()
    
    # 環境変数のチェック
    from dotenv import load_dotenv
    load_dotenv()
    
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    if not gemini_api_key:
        print("❌ エラー: GEMINI_API_KEYが設定されていません")
        print()
        print("📝 Google AI StudioでAPIキーを取得してください:")
        print("   https://makersuite.google.com/app/apikey")
        print()
        print("   .envファイルに以下を追加:")
        print("   GEMINI_API_KEY=your-api-key-here")
        return False
    
    print("✅ Gemini APIキーが見つかりました")
    print()
    
    # データディレクトリを作成
    os.makedirs('data', exist_ok=True)
    print("✅ データディレクトリを作成しました")
    
    # ステップ1: サイトをクロール
    print()
    print("📡 ステップ1: サイトをクロール中...")
    print("-" * 60)
    print("   ⚠️  この処理はAPIクォータを消費しません")
    
    crawler = JTBCSupportCrawler()
    articles = crawler.crawl_all()
    
    if not articles:
        print("❌ エラー: 記事を取得できませんでした")
        return False
    
    print(f"✅ {len(articles)}件の記事を取得しました")
    
    # ステップ2: JSONに保存
    print()
    print("💾 ステップ2: データを保存中...")
    print("-" * 60)
    
    crawler.save_to_json(articles, 'data/articles.json')
    print("✅ データを保存しました")
    
    # ステップ3: ベクトルインデックスを作成
    print()
    print("🔍 ステップ3: ベクトルインデックスを作成中...")
    print("-" * 60)
    print("   初回は埋め込みモデルのダウンロードに数分かかります")
    print("   (intfloat/multilingual-e5-small: 約130MB)")
    print()
    print("   ⚠️  HuggingFaceを使用するため、APIクォータを消費しません")
    print("   ✨ 完全無料で無制限にベクトル化できます！")
    
    # HuggingFace Embeddingsを使用（無料）
    vs_manager = VectorStoreManager(use_free=True)
    vs_manager.load_or_create_vectorstore()
    vs_manager.index_articles(articles)
    
    print("✅ ベクトルインデックスを作成しました")
    
    # 完了
    print()
    print("=" * 60)
    print("🎉 セットアップが完了しました！")
    print("=" * 60)
    print()
    print("次のコマンドでアプリケーションを起動できます:")
    print("  python app_gemini.py")
    print()
    print("💰 コスト情報:")
    print("  - ベクトル化（Embeddings）: 完全無料 ✨")
    print("  - 質問回答（Gemini）: 無料枠60回/月")
    print()
    print("💡 ヒント:")
    print("  - 初期ベクトル化は無料枠を消費しません")
    print("  - チャットでの質問回答のみカウントされます")
    print("  - 1日2回の質問なら月間無料枠内で運用可能")
    print()
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  セットアップが中断されました")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
