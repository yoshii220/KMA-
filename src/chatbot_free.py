"""
チャットボット - 無料版（Ollama対応）
ローカルLLMまたはOpenAIを選択可能
"""
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JTBCSupportChatbot:
    def __init__(self, vectorstore, api_key: str = None, use_local: bool = True, model: str = None):
        """
        Args:
            vectorstore: ベクトルストア
            api_key: OpenAI APIキー（use_local=Falseの場合のみ必要）
            use_local: Trueの場合はOllamaを使用、Falseの場合はOpenAIを使用
            model: 使用するモデル名
        """
        self.vectorstore = vectorstore
        self.use_local = use_local
        
        # LLMの選択
        if use_local:
            # Ollamaを使用（完全無料）
            model_name = model or "gemma2:2b"  # 軽量モデル
            logger.info(f"Using local Ollama model: {model_name}")
            self.llm = Ollama(
                model=model_name,
                temperature=0.7,
            )
        else:
            # OpenAIを使用
            if not api_key:
                raise ValueError("OpenAI使用時はapi_keyが必要です")
            model_name = model or "gpt-4o-mini"
            logger.info(f"Using OpenAI model: {model_name}")
            self.llm = ChatOpenAI(
                temperature=0.7,
                model=model_name,
                openai_api_key=api_key
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
