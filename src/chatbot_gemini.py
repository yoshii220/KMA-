"""
チャットボット - Gemini版
HuggingFace Embeddings（無料）+ Google Gemini（無料枠60/月）
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import logging
import os

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
        
        logger.info(f"Using Google Gemini model: {model}")
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=gemini_api_key,
            temperature=0.7,
            convert_system_message_to_human=True  # Gemini用の設定
        )
        
        # プロンプトテンプレートの設定
        self.prompt_template = """あなたはJTBCのサポートデスクのアシスタントです。
以下の情報を基に、ユーザーの質問に親切に、わかりやすく日本語で回答してください。

参考情報:
{context}

質問: {question}

回答: 情報を基に、丁寧に説明してください。参考情報に関連する内容が見つからない場合は、
「申し訳ございませんが、その情報は現在のサポートページには見つかりませんでした。
詳しくは公式サポートページをご確認いただくか、直接お問い合わせください。」と回答してください。"""

        self.prompt = PromptTemplate(
            template=self.prompt_template,
            input_variables=["context", "question"]
        )
        
        # QAチェーンの作成
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 4}
            ),
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt}
        )
    
    def ask(self, question: str) -> dict:
        """質問に対する回答を生成"""
        try:
            logger.info(f"Processing question: {question}")
            
            result = self.qa_chain.invoke({"query": question})
            
            response = {
                "answer": result["result"],
                "sources": []
            }
            
            # ソース情報を追加
            for doc in result.get("source_documents", []):
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
