"""
Flaskアプリケーション - Gemini版
HuggingFace Embeddings（無料）+ Google Gemini（無料枠60/月）
"""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import logging

from src.vector_store_free import VectorStoreManager
from src.chatbot_gemini import JTBCSupportChatbot
# from src.scheduler import UpdateScheduler  # スケジューラーは一時的に無効化

# 環境変数のロード
load_dotenv()

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flaskアプリケーション作成
app = Flask(__name__)
CORS(app)

# グローバル変数
chatbot = None
scheduler = None

def initialize_app():
    """アプリケーションの初期化"""
    global chatbot, scheduler
    
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    if not gemini_api_key:
        logger.error("GEMINI_API_KEY not found in environment variables")
        return False
    
    try:
        # ベクトルストアの初期化（HuggingFace Embeddings - 完全無料）
        logger.info("Initializing vector store with HuggingFace Embeddings (FREE)...")
        vs_manager = VectorStoreManager(use_free=True)
        vectorstore = vs_manager.load_or_create_vectorstore()
        
        # チャットボットの初期化（Google Gemini）
        logger.info("Initializing chatbot with Google Gemini...")
        model = os.getenv('GEMINI_MODEL', 'gemini-pro')
        chatbot = JTBCSupportChatbot(
            vectorstore=vectorstore,
            gemini_api_key=gemini_api_key,
            model=model
        )
        
        # スケジューラーの開始（必要に応じて）
        # スケジューラーは一時的に無効化
        scheduler = None
        # update_interval = int(os.getenv('UPDATE_INTERVAL_HOURS', 24))
        # logger.info(f"Starting scheduler (interval: {update_interval} hours)...")
        # scheduler = UpdateScheduler(interval_hours=update_interval)
        
        logger.info("Application initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error initializing application: {e}")
        import traceback
        traceback.print_exc()
        return False


@app.route('/')
def index():
    """ホームページ"""
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """チャットエンドポイント"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        if chatbot is None:
            return jsonify({'error': 'Chatbot not initialized'}), 500
        
        # 回答を生成
        response = chatbot.ask(question)
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/suggestions', methods=['GET'])
def suggestions():
    """サジェスト質問を取得"""
    try:
        if chatbot is None:
            return jsonify({'error': 'Chatbot not initialized'}), 500
        
        suggested = chatbot.get_suggested_questions()
        return jsonify({'suggestions': suggested})
        
    except Exception as e:
        logger.error(f"Error in suggestions endpoint: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/status', methods=['GET'])
def status():
    """システムステータスを取得"""
    return jsonify({
        'status': 'running',
        'chatbot_ready': chatbot is not None,
        'scheduler_running': scheduler is not None,
        'mode': 'gemini',
        'embeddings': 'HuggingFace (FREE)',
        'llm': os.getenv('GEMINI_MODEL', 'gemini-pro'),
        'cost': '無料枠60リクエスト/月'
    })


@app.route('/api/update', methods=['POST'])
def trigger_update():
    """手動でデータ更新をトリガー"""
    try:
        if scheduler is None:
            return jsonify({'error': 'Scheduler not initialized'}), 500
        
        # 更新を実行
        scheduler.update_data()
        
        return jsonify({'message': 'Update triggered successfully'})
        
    except Exception as e:
        logger.error(f"Error triggering update: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # アプリケーション初期化
    if initialize_app():
        # サーバー起動
        port = int(os.getenv('FLASK_PORT', 5000))
        print()
        print("=" * 60)
        print("🚀 JTBCサポートデスク チャットボット - Gemini版")
        print("=" * 60)
        print(f"🌐 URL: http://localhost:{port}")
        print()
        print("💰 コスト構成:")
        print("   - Embeddings: HuggingFace（完全無料・無制限）✨")
        print("   - LLM: Google Gemini（無料枠60リクエスト/月）")
        print()
        print("📊 使用状況:")
        print("   - ベクトル化: 無料枠を消費しません")
        print("   - チャット回答: 1回につき1リクエスト消費")
        print()
        
        app.run(
            host='0.0.0.0',
            port=port,
            debug=os.getenv('FLASK_ENV') == 'development'
        )
    else:
        logger.error("Failed to initialize application")
