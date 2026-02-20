#!/usr/bin/env python3
"""
初期セットアップスクリプト（無料版）
Ollama + HuggingFace Embeddingsを使用
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.crawler import JTBCSupportCrawler
from src.vector_store_free import VectorStoreManager

def check_ollama():
    """Ollamaが起動しているか確認"""
    import subprocess
    try:
        result = subprocess.run(['ollama', 'list'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        return result.returncode == 0
    except:
        return False

def main():
    print("=" * 60)
    print("JTBCサポートデスク チャットボット - 無料版セットアップ")
    print("=" * 60)
    print()
    
    # Ollamaのチェック
    print("🔍 Ollamaの確認中...")
    if not check_ollama():
        print("❌ エラー: Ollamaが見つかりません")
        print()
        print("📥 Ollamaをインストールしてください:")
        print("   macOS/Linux: curl -fsSL https://ollama.com/install.sh | sh")
        print("   Windows: https://ollama.com/download")
        print()
        print("インストール後、以下を実行してください:")
        print("   ollama pull gemma2:2b")
        return False
    
    print("✅ Ollamaが見つかりました")
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
    print("   初回は埋め込みモデルのダウンロードに数分かかります")
    print("   (intfloat/multilingual-e5-small: 約130MB)")
    
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
    print("  python app_free.py")
    print()
    print("💡 ヒント:")
    print("  - 完全無料で動作します（APIキー不要）")
    print("  - モデルは .env で変更可能")
    print("  - より高品質な回答が必要な場合: ollama pull gemma2:9b")
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
