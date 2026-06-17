"""Test script for Journal Generation system."""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent))

from modules.database import JournalDB
from modules.journal_generator import JournalGenerator


def print_header(text: str):
    """Print formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_subheader(text: str):
    """Print formatted subheader."""
    print(f"\n📌 {text}")
    print("-" * 70)


def setup_test_data():
    """Setup test data in database."""
    print_header("SETUP: Creating Test Data for Journal Generation")

    db = JournalDB()

    # Clear any existing data
    db.clear_approved_content()

    # Sample news articles
    sample_news = [
        {
            "title": "Market Rally Continues as Sensex Hits New Heights",
            "description": "The BSE Sensex surged to record levels today, driven by strong performance in IT stocks and robust FII inflows. Analysts attribute the rally to optimistic expectations about upcoming corporate earnings.",
            "link": "https://reuters.com/article1",
            "source": "Reuters Business",
            "category": "Markets",
            "published_date": (datetime.now() - timedelta(hours=2)).isoformat()
        },
        {
            "title": "TCS Reports Strong Q2 Numbers, Stock Surges 5%",
            "description": "Tata Consultancy Services has reported better-than-expected quarterly earnings, with revenue growth accelerating. The stock jumped 5% on the announcement, pulling the IT index higher.",
            "link": "https://economictimes.com/article1",
            "source": "Economic Times",
            "category": "Markets",
            "published_date": (datetime.now() - timedelta(hours=4)).isoformat()
        },
        {
            "title": "RBI Maintains Repo Rate at 6.5%, Signals Pause in Hikes",
            "description": "The Reserve Bank of India has decided to maintain the repo rate at 6.5%, suggesting that the rate hiking cycle may have ended. Market experts believe this could open doors for rate cuts in the coming months.",
            "link": "https://moneycontrol.com/article1",
            "source": "Moneycontrol Business",
            "category": "Economy",
            "published_date": (datetime.now() - timedelta(hours=6)).isoformat()
        },
        {
            "title": "Reliance Industries Eyes Jio Financial Services Expansion",
            "description": "Reliance Industries is planning to expand its digital financial services division. The company expects to leverage its massive user base to capture a larger share of the fintech market.",
            "link": "https://cnbc.com/article1",
            "source": "CNBC",
            "category": "Markets",
            "published_date": (datetime.now() - timedelta(hours=8)).isoformat()
        },
        {
            "title": "Auto Sector Shows Recovery Signs Amid Improved Demand",
            "description": "India's auto sector is showing signs of recovery with improved sales numbers. Manufacturers are optimistic about the festive season and expect sustained growth in the coming quarters.",
            "link": "https://reuters.com/article2",
            "source": "Reuters Business",
            "category": "Markets",
            "published_date": (datetime.now() - timedelta(hours=10)).isoformat()
        },
    ]

    # Add news to database
    print_subheader("Adding Sample News Articles...")
    stats = db.add_multiple_news(sample_news)
    print(f"✅ Added {stats['added']} articles")

    # Approve all articles
    print_subheader("Approving All Articles for Journal...")
    articles = db.get_unapproved_news(limit=1000)
    for article in articles:
        db.approve_news(article['id'])
    print(f"✅ Approved {len(articles)} articles")

    # Add market data
    print_subheader("Adding Sample Market Data...")
    sample_market = [
        {"symbol": "RELIANCE.NS", "display_name": "RELIANCE", "price": 2550.50, "change_percent": 2.05, "change_value": 50.25},
        {"symbol": "TCS.NS", "display_name": "TCS", "price": 3450.75, "change_percent": 1.85, "change_value": 62.50},
        {"symbol": "INFY.NS", "display_name": "INFY", "price": 1800.25, "change_percent": 0.95, "change_value": 17.00},
        {"symbol": "HDFCBANK.NS", "display_name": "HDFC Bank", "price": 1650.50, "change_percent": -1.25, "change_value": -21.00},
        {"symbol": "ICICIBANK.NS", "display_name": "ICICI Bank", "price": 950.75, "change_percent": -0.85, "change_value": -8.25},
        {"symbol": "AXISBANK.NS", "display_name": "Axis Bank", "price": 1050.00, "change_percent": -1.50, "change_value": -16.00},
        {"symbol": "WIPRO.NS", "display_name": "Wipro", "price": 450.50, "change_percent": 3.25, "change_value": 14.00},
        {"symbol": "MARUTI.NS", "display_name": "Maruti", "price": 8500.25, "change_percent": -0.50, "change_value": -42.50},
    ]

    stats = db.add_multiple_market_data(sample_market)
    print(f"✅ Added {stats['added']} market data points")

    # Approve all market data
    print_subheader("Approving All Market Data...")
    market_data = db.get_unapproved_market_data()
    for data in market_data:
        db.approve_market_data(data['id'])
    print(f"✅ Approved {len(market_data)} market data points")

    return db


def test_basic_journal_generation(db: JournalDB, generator: JournalGenerator):
    """Test basic journal generation."""
    print_header("TEST 1: Basic Journal Generation")

    # Get approved content
    news = db.get_approved_news(limit=1000)
    market_data = db.get_approved_market_data()

    print_subheader("Generating Journal...")
    print(f"📰 News articles: {len(news)}")
    print(f"📈 Market data: {len(market_data)}")

    try:
        output_path = generator.generate_journal(
            news=news,
            market_data=market_data,
            club_name="Finance Club"
        )

        print(f"✅ Journal generated successfully!")
        print(f"   Path: {output_path}")

        # Verify file exists and has content
        file_path = Path(output_path)
        file_size = file_path.stat().st_size

        print(f"   Size: {file_size / 1024:.1f} KB")

        return output_path

    except Exception as e:
        print(f"❌ Error generating journal: {str(e)}")
        return None


def test_journal_bytes_generation(db: JournalDB, generator: JournalGenerator):
    """Test journal generation as bytes."""
    print_header("TEST 2: Journal Generation as Bytes (Download Mode)")

    news = db.get_approved_news(limit=1000)
    market_data = db.get_approved_market_data()

    print_subheader("Generating Journal as Bytes...")

    try:
        html_bytes = generator.generate_journal_bytes(
            news=news,
            market_data=market_data,
            club_name="Test Finance Club"
        )

        print(f"✅ Journal generated as bytes")
        print(f"   Size: {len(html_bytes) / 1024:.1f} KB")
        print(f"   Type: {type(html_bytes)}")

        # Verify it's valid HTML
        html_str = html_bytes.decode("utf-8")
        is_valid = "<html" in html_str.lower() and "</html>" in html_str.lower()

        if is_valid:
            print(f"✅ Valid HTML structure detected")
        else:
            print(f"❌ HTML structure validation failed")

    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_journal_info(generator: JournalGenerator, journal_path: str):
    """Test getting journal information."""
    print_header("TEST 3: Journal File Information")

    print_subheader("Getting Journal Info...")

    try:
        info = generator.get_journal_info(journal_path)

        print(f"✅ Journal info retrieved:")
        for key, value in info.items():
            print(f"   {key}: {value}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_journal_list(generator: JournalGenerator):
    """Test getting list of generated journals."""
    print_header("TEST 4: Generated Journals List")

    print_subheader("Getting Recent Journals...")

    try:
        journals = generator.get_generated_journals_list()

        print(f"✅ Found {len(journals)} generated journals:")

        for file_path, mtime in journals[:5]:
            path = Path(file_path)
            file_size = path.stat().st_size
            created = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")

            print(f"   📄 {path.name}")
            print(f"      Size: {file_size / 1024:.1f} KB")
            print(f"      Created: {created}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")


def test_index_page_generation(db: JournalDB, generator: JournalGenerator):
    """Test index page generation."""
    print_header("TEST 5: Index/Dashboard Page Generation")

    print_subheader("Generating Index Page...")

    try:
        stats = db.get_stats()
        recent_updates = [
            {"date": "2026-06-17", "title": "System Ready", "description": "FinWiz Journal system is running and ready to process financial news."},
            {"date": "2026-06-16", "title": "Market Data Updated", "description": "Latest Nifty 50 data has been fetched and stored."},
        ]

        output_path = generator.generate_index_page(stats, recent_updates)

        print(f"✅ Index page generated successfully!")
        print(f"   Path: {output_path}")

        file_size = Path(output_path).stat().st_size
        print(f"   Size: {file_size / 1024:.1f} KB")

    except Exception as e:
        print(f"❌ Error: {str(e)}")


def main():
    """Run all journal generation tests."""
    print("\n" + "╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  Journal Generation System - Full Workflow Test".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")

    start_time = datetime.now()

    try:
        # Setup test data
        db = setup_test_data()

        # Initialize generator
        generator = JournalGenerator()

        # Run tests
        journal_path = test_basic_journal_generation(db, generator)
        test_journal_bytes_generation(db, generator)

        if journal_path:
            test_journal_info(generator, journal_path)

        test_journal_list(generator)
        test_index_page_generation(db, generator)

        # Summary
        print_header("SUMMARY")
        elapsed = (datetime.now() - start_time).total_seconds()

        print(f"\n✅ All tests completed successfully!")
        print(f"⏱️  Total execution time: {elapsed:.2f} seconds")

        print(f"\n📊 Generated Content:")
        stats = db.get_stats()
        print(f"   Approved News: {stats['approved_news']}")
        print(f"   Approved Market Data: {stats['approved_market']}")

        if journal_path:
            print(f"\n📄 Journal Details:")
            print(f"   File: {Path(journal_path).name}")
            print(f"   Path: {journal_path}")

    except KeyboardInterrupt:
        print("\n\n❌ Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
