"""
ベクトルストア - 無料版（Sentence Transformers対応）
OpenAIのEmbeddings不要
"""
import json
from typing import List, Dict
import logging
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorStoreManager:
    def __init__(self, use_free: bool = True, openai_api_key: str = None, persist_directory: str = "./chroma_db"):
        """
        Args:
            use_free: Trueの場合は無料のHuggingFace Embeddingsを使用
            openai_api_key: OpenAI APIキー（use_free=Falseの場合のみ必要）
            persist_directory: ベクトルストアの保存先
        """
        self.persist_directory = persist_directory
        self.use_free = use_free
        
        if use_free:
            # 無料のHuggingFace Embeddingsを使用（日本語対応）
            logger.info("Using free HuggingFace Embeddings")
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",  # 超軽量モデル
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
        else:
            # OpenAI Embeddingsを使用
            if not openai_api_key:
                raise ValueError("OpenAI使用時はapi_keyが必要です")
            from langchain_openai import OpenAIEmbeddings
            logger.info("Using OpenAI Embeddings")
            self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        
        self.vectorstore = None
        
    def load_or_create_vectorstore(self):
        """ベクトルストアをロードまたは作成"""
        if os.path.exists(self.persist_directory):
            logger.info("Loading existing vector store...")
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
        else:
            logger.info("Creating new vector store...")
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
        return self.vectorstore
    
    def load_articles_from_json(self, filepath: str = 'data/articles.json') -> List[Dict]:
        """JSONファイルから記事を読み込む"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                articles = json.load(f)
            logger.info(f"Loaded {len(articles)} articles from {filepath}")
            return articles
        except Exception as e:
            logger.error(f"Error loading articles: {e}")
            return []
    
    def prepare_documents(self, articles: List[Dict]) -> List[Document]:
        """記事をLangChainのDocumentオブジェクトに変換"""
        documents = []
        
        for article in articles:
            if article.get('content'):
                doc = Document(
                    page_content=article['content'],
                    metadata={
                        'title': article.get('title', ''),
                        'url': article.get('url', ''),
                        'category': article.get('category', ''),
                        'crawled_at': article.get('crawled_at', '')
                    }
                )
                documents.append(doc)
        
        logger.info(f"Prepared {len(documents)} documents")
        return documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """ドキュメントを小さなチャンクに分割"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        splits = text_splitter.split_documents(documents)
        logger.info(f"Split into {len(splits)} chunks")
        return splits
    
    def index_articles(self, articles: List[Dict]):
        """記事をインデックス化してベクトルストアに保存"""
        logger.info("Starting indexing process...")
        
        # ドキュメント準備
        documents = self.prepare_documents(articles)
        
        if not documents:
            logger.warning("No documents to index")
            return
        
        # チャンク分割
        splits = self.split_documents(documents)
        
        # ベクトルストアに追加
        if self.vectorstore is None:
            self.vectorstore = Chroma.from_documents(
                documents=splits,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
        else:
            self.vectorstore.add_documents(splits)
        
        logger.info("Indexing completed")
    
    def search(self, query: str, k: int = 4) -> List[Document]:
        """類似度検索を実行"""
        if self.vectorstore is None:
            logger.error("Vector store not initialized")
            return []
        
        results = self.vectorstore.similarity_search(query, k=k)
        logger.info(f"Found {len(results)} results for query: {query}")
        return results
    
    def update_index(self, articles_filepath: str = 'data/articles.json'):
        """インデックスを更新（新しい記事を追加）"""
        logger.info("Updating index...")
        
        # 既存のベクトルストアをロード
        self.load_or_create_vectorstore()
        
        # 新しい記事を読み込み
        articles = self.load_articles_from_json(articles_filepath)
        
        if articles:
            # インデックス化
            self.index_articles(articles)
            logger.info("Index update completed")
        else:
            logger.warning("No articles to update")
