"""
JTBCサポートサイトのクローラー
サイトから記事情報を取得し、データベースに保存します。
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import json
import time
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JTBCSupportCrawler:
    def __init__(self, base_url: str = "https://biz.help.jtbc.info/hc/ja"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def get_categories(self) -> List[Dict]:
        """カテゴリ一覧を取得"""
        try:
            response = self.session.get(self.base_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            categories = []
            # カテゴリリンクを探す
            category_links = soup.find_all('a', href=True)
            
            for link in category_links:
                href = link.get('href', '')
                if '/hc/ja/categories/' in href or '/hc/ja/sections/' in href:
                    title = link.get_text(strip=True)
                    if title:
                        categories.append({
                            'title': title,
                            'url': href if href.startswith('http') else self.base_url + href
                        })
            
            logger.info(f"Found {len(categories)} categories")
            return categories
        except Exception as e:
            logger.error(f"Error fetching categories: {e}")
            return []
    
    def get_articles_from_category(self, category_url: str) -> List[Dict]:
        """特定のカテゴリから記事一覧を取得"""
        try:
            response = self.session.get(category_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            articles = []
            article_links = soup.find_all('a', href=True)
            
            for link in article_links:
                href = link.get('href', '')
                if '/hc/ja/articles/' in href:
                    title = link.get_text(strip=True)
                    if title:
                        full_url = href if href.startswith('http') else 'https://biz.help.jtbc.info' + href
                        articles.append({
                            'title': title,
                            'url': full_url
                        })
            
            logger.info(f"Found {len(articles)} articles in category")
            return articles
        except Exception as e:
            logger.error(f"Error fetching articles from category: {e}")
            return []
    
    def get_article_content(self, article_url: str) -> Dict:
        """記事の詳細内容を取得"""
        try:
            response = self.session.get(article_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # タイトルを取得
            title_elem = soup.find('h1') or soup.find('title')
            title = title_elem.get_text(strip=True) if title_elem else ''
            
            # 本文を取得
            content_elem = soup.find('div', class_='article-body') or \
                          soup.find('article') or \
                          soup.find('main')
            
            content = ''
            if content_elem:
                # テキストを抽出
                content = content_elem.get_text(separator='\n', strip=True)
            
            return {
                'title': title,
                'content': content,
                'url': article_url,
                'crawled_at': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error fetching article content from {article_url}: {e}")
            return {}
    
    def crawl_all(self) -> List[Dict]:
        """全記事をクロール"""
        logger.info("Starting full crawl...")
        all_articles = []
        
        # カテゴリを取得
        categories = self.get_categories()
        
        for category in categories:
            logger.info(f"Crawling category: {category['title']}")
            time.sleep(1)  # レート制限対策
            
            # カテゴリ内の記事を取得
            articles = self.get_articles_from_category(category['url'])
            
            for article in articles:
                time.sleep(1)  # レート制限対策
                article_data = self.get_article_content(article['url'])
                
                if article_data:
                    article_data['category'] = category['title']
                    all_articles.append(article_data)
                    logger.info(f"Crawled: {article_data['title']}")
        
        logger.info(f"Crawl completed. Total articles: {len(all_articles)}")
        return all_articles
    
    def save_to_json(self, articles: List[Dict], filepath: str = 'data/articles.json'):
        """記事データをJSONファイルに保存"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(articles, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved {len(articles)} articles to {filepath}")
        except Exception as e:
            logger.error(f"Error saving to JSON: {e}")


if __name__ == "__main__":
    crawler = JTBCSupportCrawler()
    articles = crawler.crawl_all()
    crawler.save_to_json(articles)
