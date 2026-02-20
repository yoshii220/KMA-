"""
チャットボットのメインロジック
ユーザーの質問に対してRAGベースで回答を生成します。
"""
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JTBCSupportChatbot:
    def __init__(self, vectorstore, openai_api_key: str, model: str = "gpt-4o-mini"):
        self.vectorstore = vectorstore
        self.llm = ChatOpenAI(
            temperature=0.7,
            model=model,
            openai_api_key=openai_api_key
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


if __name__ == "__main__":
    # テスト用
    import os
    from dotenv import load_dotenv
    from vector_store import VectorStoreManager
    
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    
    if api_key:
        # ベクトルストアをロード
        vs_manager = VectorStoreManager(api_key)
        vectorstore = vs_manager.load_or_create_vectorstore()
        
        # チャットボット作成
        chatbot = JTBCSupportChatbot(vectorstore, api_key)
        
        # テスト質問
        test_questions = [
            "総務省への届出について教えてください",
            "JTBC一次代理店とは？"
        ]
        
        for question in test_questions:
            print(f"\n質問: {question}")
            response = chatbot.ask(question)
            print(f"回答: {response['answer']}")
            print(f"ソース数: {len(response['sources'])}")
