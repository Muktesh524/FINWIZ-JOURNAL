"""Fetch financial news from RSS feeds."""

import feedparser
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from urllib.parse import urlparse


class NewsFetcher:
    """Fetch news from RSS feeds."""

    # Configure RSS feeds for financial news
    RSS_FEEDS = {
        "Reuters Business": "https://feeds.reuters.com/reuters/businessNews",
        "Economic Times": "https://economictimes.indiatimes.com/feed/",
        "Moneycontrol Business": "https://feeds.moneycontrol.com/news/business/",
        "CNBC": "https://feeds.cnbc.com/id/100003114/rss.html",
    }

    def __init__(self, feeds: Optional[Dict[str, str]] = None):
        """Initialize with custom feeds or use defaults."""
        self.feeds = feeds or self.RSS_FEEDS

    def fetch_all_news(self, limit_per_feed: int = 10) -> Tuple[List[Dict], Dict[str, int]]:
        """Fetch news from all configured feeds. Returns (articles, stats)."""
        all_news = []
        stats = {"total_fetched": 0, "duplicates_removed": 0, "errors": 0}
        seen_hashes = set()

        for source_name, feed_url in self.feeds.items():
            try:
                news, feed_stats = self.fetch_from_feed(feed_url, source_name, limit_per_feed)

                # Remove duplicates
                for item in news:
                    item_hash = self._hash_article(item)
                    if item_hash not in seen_hashes:
                        all_news.append(item)
                        seen_hashes.add(item_hash)
                    else:
                        stats["duplicates_removed"] += 1

                stats["total_fetched"] += feed_stats["fetched"]
            except Exception as e:
                stats["errors"] += 1
                print(f"Error fetching from {source_name}: {str(e)}")

        return all_news, stats

    def fetch_from_feed(self, feed_url: str, source_name: str, limit: int = 10) -> Tuple[List[Dict], Dict]:
        """Fetch news from a single RSS feed. Returns (articles, stats)."""
        stats = {"fetched": 0, "valid": 0}
        try:
            feed = feedparser.parse(feed_url)
            news_list = []

            if not feed.entries:
                print(f"No entries found in {source_name} feed")
                return news_list, stats

            for entry in feed.entries[:limit]:
                stats["fetched"] += 1
                news_item = {
                    "title": self._clean_text(entry.get("title", "")),
                    "description": self._clean_text(entry.get("summary", "")),
                    "link": entry.get("link", ""),
                    "source": source_name,
                    "published_date": self._parse_date(entry.get("published", "")),
                    "category": self._extract_category(entry, source_name),
                    "fetched_at": datetime.now().isoformat(),
                }

                if news_item["title"] and news_item["link"]:
                    news_list.append(news_item)
                    stats["valid"] += 1

            return news_list, stats
        except Exception as e:
            print(f"Error parsing feed {feed_url}: {str(e)}")
            return [], stats

    @staticmethod
    def _parse_date(date_str: str) -> Optional[str]:
        """Parse publication date from feed."""
        if not date_str:
            return None
        try:
            # Try parsing common date formats
            from dateutil import parser
            parsed_date = parser.parse(date_str)
            return parsed_date.isoformat()
        except:
            return None

    @staticmethod
    def _extract_category(entry: Dict, source: str) -> str:
        """Extract or infer category from feed entry."""
        if "tags" in entry and entry["tags"]:
            return entry["tags"][0].get("term", "General")

        category_map = {
            "Reuters Business": "Markets",
            "Moneycontrol Business": "Markets",
            "Economic Times": "Economy",
            "CNBC": "Markets",
        }
        return category_map.get(source, "General")

    @staticmethod
    def _clean_text(text: str) -> str:
        """Clean text by removing HTML tags and extra whitespace."""
        if not text:
            return ""
        import re
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text

    @staticmethod
    def _hash_article(article: Dict) -> str:
        """Generate hash for duplicate detection."""
        content = f"{article['title']}|{article['link']}"
        return hashlib.md5(content.encode()).hexdigest()


if __name__ == "__main__":
    fetcher = NewsFetcher()
    news = fetcher.fetch_all_news(limit_per_feed=5)
    for item in news[:3]:
        print(f"\n{item['source']} - {item['title']}")
        print(f"Link: {item['link']}")
