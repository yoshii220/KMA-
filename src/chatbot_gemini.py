"""
チャットボット - Gemini版（シンプル版）
HuggingFace Embeddings（無料）+ Google Gemini（無料枠60/月）
"""
import logging
from langchain_google_genai import ChatGoogleGenerativeAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JTBCSupportChatbot:
    def __init__(self, vectorstore, gemini_api_key: str, model: str = "gemini-pro"):
        """
        Args:
            vectorstore: ベクトルストア（HuggingFace Embeddingsを使用）
            gemini_api_key: Google Gemini APIキー
            model: 使用するGeminiモデル名
        """
        self.vectorstore = vectorstore
        self.retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
        
        logger.info(f"Using Google Gemini model: {model}")
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=gemini_api_key,
            temperature=0.7,
        )
    
    def ask(self, question: str) -> dict:
        """質問に対する回答を生成"""
        try:
            logger.info(f"Processing question: {question}")
            
            # 関連ドキュメントを検索
            docs = self.retriever.get_relevant_documents(question)
            
            # コンテキストを作成
            context = "\n\n".join([doc.page_content for doc in docs])
            
            # プロンプトを作成
            prompt = f"""あなたはJTBCのサポートデスクのアシスタントです。
以下の情報を基に、ユーザーの質問に親切に、わかりやすく日本語で回答してください。

参考情報:
{context}

質問: {question}

回答: 情報を基に、丁寧に説明してください。参考情報に関連する内容が見つからない場合は、
「申し訳ございませんが、その情報は現在のサポートページには見つかりませんでした。
詳しくは公式サポートページをご確認いただくか、直接お問い合わせください。」と回答してください。"""
            
            # Geminiで回答生成
            response_text = self.llm.invoke(prompt).content
            
            response = {
                "answer": response_text,
                "sources": []
            }
            
            # ソース情報を追加
            for doc in docs:
                response["sources"].append({
                    "title": doc.metadata.get("title", ""),
                    "url": doc.metadata.get("url", ""),
                    "category": doc.metadata.get("category", ""),
                    "excerpt": doc.page_content[:200] + "..."
                })
            
            logger.info("Response generated successfully")
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            import traceback
            traceback.print_exc()
            return {
                "answer": "申し訳ございません。回答の生成中にエラーが発生しました。もう一度お試しください。",
                "sources": []
            }
    
    def get_suggested_questions(self) -> list:
        """よくある質問のサジェスト"""
        return [
            "総務省への届出について教えてください",
            "JTBC一次代理店とは何ですか？",
            "活動準備で必要なことを教えてください",
            "よくある質問を教えてください"
        ]
