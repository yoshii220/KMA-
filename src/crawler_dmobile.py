"""
dmobileサポートサイト専用クローラー
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import json
import time
from datetime import datetime
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DmobileSupportCrawler:
    def __init__(self, base_url: str = "https://help.dmobile.jp/hc/ja"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        })
    
    def get_article_links(self) -> List[str]:
        """記事リンクを取得"""
        try:
            response = self.session.get(self.base_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            article_urls = set()
            
            # すべてのリンクを取得
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                
                # 記事ページのURLパターン
                if '/articles/' in href:
                    full_url = href if href.startswith('http') else 'https://help.dmobile.jp' + href
                    article_urls.add(full_url)
            
            logger.info(f"Found {len(article_urls)} article URLs")
            return list(article_urls)
            
        except Exception as e:
            logger.error(f"Error fetching article links: {e}")
            return []
    
    def get_article_content(self, article_url: str) -> Dict:
        """記事の内容を取得"""
        try:
            response = self.session.get(article_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # タイトルを取得
            title = ''
            title_elem = soup.find('h1')
            if title_elem:
                title = title_elem.get_text(strip=True)
            
            # 本文を取得
            content = ''
            
            # よくあるクラス名を試す
            content_selectors = [
                'article-body',
                'article-content',
                'article',
                'content',
                'main-content'
            ]
            
            for selector in content_selectors:
                content_elem = soup.find('div', class_=selector) or soup.find('article', class_=selector)
                if content_elem:
                    content = content_elem.get_text(separator='\n', strip=True)
                    break
            
            # 見つからない場合はarticleタグを探す
            if not content:
                content_elem = soup.find('article') or soup.find('main')
                if content_elem:
                    content = content_elem.get_text(separator='\n', strip=True)
            
            if not title and not content:
                logger.warning(f"No content found for {article_url}")
                return {}
            
            return {
                'title': title,
                'content': content,
                'url': article_url,
                'category': 'dmobileサポート',
                'crawled_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error fetching article {article_url}: {e}")
            return {}
    
    def crawl_all(self) -> List[Dict]:
        """全記事をクロール"""
        logger.info("Starting dmobile support site crawl...")
        
        # 記事URLを取得
        article_urls = self.get_article_links()
        
        if not article_urls:
            logger.error("No article URLs found")
            return []
        
        articles = []
        
        for i, url in enumerate(article_urls, 1):
            logger.info(f"Crawling article {i}/{len(article_urls)}: {url}")
            
            article_data = self.get_article_content(url)
            
            if article_data and article_data.get('content'):
                articles.append(article_data)
                logger.info(f"✅ Crawled: {article_data.get('title', 'No title')}")
            
            # レート制限対策
            time.sleep(0.5)
        
        logger.info(f"Crawl completed. Total articles: {len(articles)}")
        return articles
    
    def save_to_json(self, articles: List[Dict], filepath: str = 'data/articles.json'):
        """記事データをJSONファイルに保存"""
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(articles, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved {len(articles)} articles to {filepath}")
        except Exception as e:
            logger.error(f"Error saving to JSON: {e}")


if __name__ == "__main__":
    crawler = DmobileSupportCrawler()
    articles = crawler.crawl_all()
    
    if articles:
        crawler.save_to_json(articles)
        print(f"\n✅ Successfully crawled {len(articles)} articles!")
        print(f"📁 Saved to: data/articles.json")
    else:
        print("\n❌ No articles were crawled.")
