"""Fetch financial news from RSS feeds."""

import feedparser
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urlparse


class NewsFetcher:
    """Fetch news from RSS feeds."""

    # Configure RSS feeds for financial news
    RSS_FEEDS = {
        "Financial Express": "https://www.financialexpress.com/feed/",
        "Moneycontrol": "https://feeds.moneycontrol.com/news/business/",
        "Economic Times": "https://economictimes.indiatimes.com/feed/",
        "Yahoo Finance": "https://feeds.finance.yahoo.com/rss/2.0/headline",
    }

    def __init__(self, feeds: Optional[Dict[str, str]] = None):
        """Initialize with custom feeds or use defaults."""
        self.feeds = feeds or self.RSS_FEEDS

    def fetch_all_news(self, limit_per_feed: int = 10) -> List[Dict]:
        """Fetch news from all configured feeds."""
        all_news = []

        for source_name, feed_url in self.feeds.items():
            try:
                news = self.fetch_from_feed(feed_url, source_name, limit_per_feed)
                all_news.extend(news)
            except Exception as e:
                print(f"Error fetching from {source_name}: {str(e)}")

        return all_news

    def fetch_from_feed(self, feed_url: str, source_name: str, limit: int = 10) -> List[Dict]:
        """Fetch news from a single RSS feed."""
        try:
            feed = feedparser.parse(feed_url)
            news_list = []

            for entry in feed.entries[:limit]:
                news_item = {
                    "title": entry.get("title", ""),
                    "description": entry.get("summary", ""),
                    "link": entry.get("link", ""),
                    "source": source_name,
                    "published_date": self._parse_date(entry.get("published", "")),
                    "category": self._extract_category(entry, source_name),
                }

                if news_item["title"] and news_item["link"]:
                    news_list.append(news_item)

            return news_list
        except Exception as e:
            print(f"Error parsing feed {feed_url}: {str(e)}")
            return []

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
        # Try to get category from entry
        if "tags" in entry and entry["tags"]:
            return entry["tags"][0].get("term", "General")

        # Default categories per source
        category_map = {
            "Financial Express": "Markets",
            "Moneycontrol": "Markets",
            "Economic Times": "Economy",
            "Yahoo Finance": "Markets",
        }

        return category_map.get(source, "General")


if __name__ == "__main__":
    fetcher = NewsFetcher()
    news = fetcher.fetch_all_news(limit_per_feed=5)
    for item in news[:3]:
        print(f"\n{item['source']} - {item['title']}")
        print(f"Link: {item['link']}")
