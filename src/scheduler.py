"""
定期更新スケジューラー
指定された間隔でサイトをクロールし、データベースを更新します。
"""
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import logging
import os
from dotenv import load_dotenv

from crawler import JTBCSupportCrawler
from vector_store import VectorStoreManager

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UpdateScheduler:
    def __init__(self, interval_hours: int = 24):
        self.interval_hours = interval_hours
        self.scheduler = BackgroundScheduler()
        self.crawler = JTBCSupportCrawler()
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
    def update_data(self):
        """データ更新処理"""
        try:
            logger.info(f"Starting scheduled update at {datetime.now()}")
            
            # サイトをクロール
            articles = self.crawler.crawl_all()
            
            if not articles:
                logger.warning("No articles crawled")
                return
            
            # JSONに保存
            self.crawler.save_to_json(articles)
            
            # ベクトルストアを更新
            if self.openai_api_key:
                vs_manager = VectorStoreManager(self.openai_api_key)
                vs_manager.update_index()
                logger.info("Vector store updated successfully")
            else:
                logger.error("OpenAI API key not found")
            
            logger.info(f"Update completed at {datetime.now()}")
            
        except Exception as e:
            logger.error(f"Error during scheduled update: {e}")
    
    def start(self):
        """スケジューラーを開始"""
        # 初回実行
        logger.info("Running initial data update...")
        self.update_data()
        
        # 定期実行をスケジュール
        self.scheduler.add_job(
            self.update_data,
            'interval',
            hours=self.interval_hours,
            id='update_job',
            name='Update JTBC support data',
            replace_existing=True
        )
        
        self.scheduler.start()
        logger.info(f"Scheduler started. Will update every {self.interval_hours} hours")
    
    def stop(self):
        """スケジューラーを停止"""
        self.scheduler.shutdown()
        logger.info("Scheduler stopped")


if __name__ == "__main__":
    scheduler = UpdateScheduler(interval_hours=24)
    scheduler.start()
    
    # Keep the script running
    try:
        import time
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.stop()
