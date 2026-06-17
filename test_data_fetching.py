"""Test script for data fetching modules."""

import sys
from pathlib import Path
from datetime import datetime

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent))

from modules.news_fetcher import NewsFetcher
from modules.market_data import MarketDataFetcher
from modules.database import JournalDB


def print_header(text: str):
    """Print formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_subheader(text: str):
    """Print formatted subheader."""
    print(f"\n📌 {text}")
    print("-" * 70)


def test_news_fetcher():
    """Test news fetching functionality."""
    print_header("TEST 1: NEWS FETCHER")

    print("\n🔄 Initializing NewsFetcher...")
    fetcher = NewsFetcher()

    print(f"📰 Configured RSS Feeds:")
    for source, url in fetcher.feeds.items():
        print(f"   • {source}: {url}")

    print_subheader("Fetching news from all sources...")
    try:
        news_articles, stats = fetcher.fetch_all_news(limit_per_feed=5)

        print(f"\n✅ Fetch Complete!")
        print(f"   Total fetched: {stats['total_fetched']} entries")
        print(f"   Unique articles: {len(news_articles)}")
        print(f"   Duplicates removed: {stats['duplicates_removed']}")
        print(f"   Feed errors: {stats['errors']}")

        if news_articles:
            print_subheader(f"Sample Articles (showing first 3 of {len(news_articles)})")
            for i, article in enumerate(news_articles[:3], 1):
                print(f"\n📰 Article {i}:")
                print(f"   Title: {article['title'][:60]}...")
                print(f"   Source: {article['source']}")
                print(f"   Category: {article['category']}")
                print(f"   Date: {article.get('published_date', 'N/A')[:10]}")
                print(f"   Link: {article['link'][:50]}...")

            return news_articles
        else:
            print("⚠️  No articles fetched!")
            return []

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return []


def test_market_fetcher():
    """Test market data fetching functionality."""
    print_header("TEST 2: MARKET DATA FETCHER")

    print("\n🔄 Initializing MarketDataFetcher...")
    fetcher = MarketDataFetcher()

    # Test index data
    print_subheader("Fetching Market Indices...")
    try:
        indices = fetcher.fetch_index_data()

        if indices:
            print(f"\n📊 Market Indices:")
            for key, data in indices.items():
                if data:
                    direction = "📈" if data["change_percent"] >= 0 else "📉"
                    print(f"   {direction} {data['name']}: {data['value']} ({data['change_percent']:+.2f}%)")
        else:
            print("⚠️  No index data fetched")

    except Exception as e:
        print(f"❌ Error fetching indices: {str(e)}")

    # Test Nifty 50 movers
    print_subheader("Fetching Nifty 50 Top Movers...")
    try:
        gainers, losers, stats = fetcher.fetch_nifty_50_movers(top_n=5)

        print(f"\n✅ Fetch Complete!")
        print(f"   Stocks fetched: {stats['fetched']}")
        print(f"   Fetch errors: {stats['errors']}")

        if gainers:
            print(f"\n📈 Top 5 Gainers:")
            for i, stock in enumerate(gainers, 1):
                print(f"   {i}. {stock['display_name']:<15} ₹{stock['price']:>8.2f} ({stock['change_percent']:>6.2f}%)")

        if losers:
            print(f"\n📉 Top 5 Losers:")
            for i, stock in enumerate(losers, 1):
                print(f"   {i}. {stock['display_name']:<15} ₹{stock['price']:>8.2f} ({stock['change_percent']:>6.2f}%)")

        return gainers + losers

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return []


def test_database(news_articles, market_data):
    """Test database operations."""
    print_header("TEST 3: DATABASE OPERATIONS")

    print("\n🔄 Initializing JournalDB...")
    db = JournalDB()

    print_subheader("Adding News Articles to Database...")
    try:
        if news_articles:
            stats = db.add_multiple_news(news_articles)
            print(f"\n✅ Articles Added:")
            print(f"   Successfully added: {stats['added']}")
            print(f"   Duplicates skipped: {stats['duplicates']}")
            print(f"   Errors: {stats['errors']}")
        else:
            print("⚠️  No news articles to add")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

    print_subheader("Adding Market Data to Database...")
    try:
        if market_data:
            stats = db.add_multiple_market_data(market_data)
            print(f"\n✅ Market Data Added:")
            print(f"   Successfully added: {stats['added']}")
            print(f"   Errors: {stats['errors']}")
        else:
            print("⚠️  No market data to add")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

    print_subheader("Database Statistics...")
    try:
        db_stats = db.get_stats()
        print(f"\n📊 Content in Database:")
        print(f"   Pending news articles: {db_stats['unapproved_news']}")
        print(f"   Approved news articles: {db_stats['approved_news']}")
        print(f"   Pending market data: {db_stats['unapproved_market']}")
        print(f"   Approved market data: {db_stats['approved_market']}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

    print_subheader("Retrieving Sample News from Database...")
    try:
        unapproved_news = db.get_unapproved_news(limit=3)

        if unapproved_news:
            print(f"\n📰 Sample Pending News (showing first 3 of {len(unapproved_news)}):")
            for i, news in enumerate(unapproved_news[:3], 1):
                print(f"\n   {i}. {news['title'][:60]}...")
                print(f"      Source: {news['source']}")
                print(f"      Status: {'Approved' if news['approved'] else 'Pending'}")
        else:
            print("ℹ️  No pending news articles")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

    print_subheader("Retrieving Sample Market Data from Database...")
    try:
        unapproved_market = db.get_unapproved_market_data()

        if unapproved_market:
            print(f"\n📈 Sample Market Data (showing first 5 of {len(unapproved_market)}):")
            for i, data in enumerate(unapproved_market[:5], 1):
                print(f"   {i}. {data['symbol']:<15} ₹{data['price']:>8.2f} ({data['change_percent']:>6.2f}%)")
        else:
            print("ℹ️  No pending market data")

    except Exception as e:
        print(f"❌ Error: {str(e)}")


def main():
    """Run all tests."""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  FinWiz Journal - Data Fetching Test Suite".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")

    start_time = datetime.now()

    try:
        # Test 1: News Fetcher
        news_articles = test_news_fetcher()

        # Test 2: Market Data Fetcher
        market_data = test_market_fetcher()

        # Test 3: Database Operations
        test_database(news_articles, market_data)

        # Summary
        print_header("SUMMARY")
        elapsed = (datetime.now() - start_time).total_seconds()
        print(f"\n✅ All tests completed successfully!")
        print(f"⏱️  Total execution time: {elapsed:.2f} seconds")

        print(f"\n📊 Final Statistics:")
        print(f"   News articles fetched: {len(news_articles)}")
        print(f"   Market data points fetched: {len(market_data)}")
        print(f"   Total items processed: {len(news_articles) + len(market_data)}")

    except KeyboardInterrupt:
        print("\n\n❌ Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()
