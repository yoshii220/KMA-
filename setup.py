#!/usr/bin/env python3
"""
初期セットアップスクリプト
初回起動時にデータをクロールしてインデックスを作成します。
"""
import os
import sys
from dotenv import load_dotenv

# プロジェクトのルートディレクトリをPythonパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.crawler import JTBCSupportCrawler
from src.vector_store import VectorStoreManager

def main():
    print("=" * 60)
    print("JTBCサポートデスク チャットボット - 初期セットアップ")
    print("=" * 60)
    print()
    
    # 環境変数を読み込む
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ エラー: OPENAI_API_KEYが設定されていません")
        print("   .envファイルを作成し、OpenAI APIキーを設定してください")
        return False
    
    print("✅ OpenAI APIキーが見つかりました")
    print()
    
    # データディレクトリを作成
    os.makedirs('data', exist_ok=True)
    print("✅ データディレクトリを作成しました")
    
    # ステップ1: サイトをクロール
    print()
    print("📡 ステップ1: サイトをクロール中...")
    print("-" * 60)
    
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
    print("   (この処理には数分かかる場合があります)")
    
    vs_manager = VectorStoreManager(api_key)
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
    print("  python app.py")
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
