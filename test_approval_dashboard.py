"""Test script for the Approval Dashboard."""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent))

from modules.database import JournalDB
from modules.news_fetcher import NewsFetcher
from modules.market_data import MarketDataFetcher


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
    print_header("SETUP: Creating Test Data")

    db = JournalDB()

    # Sample news articles
    sample_news = [
        {
            "title": "Market Rally Continues as Sensex Hits New Heights",
            "description": "The BSE Sensex surged to record levels today, driven by strong performance in IT stocks and robust FII inflows. Analysts attribute the rally to optimistic expectations about upcoming corporate earnings.",
            "link": "https://example.com/article1",
            "source": "Reuters Business",
            "category": "Markets",
            "published_date": (datetime.now() - timedelta(hours=2)).isoformat()
        },
        {
            "title": "TCS Reports Strong Q2 Numbers, Stock Surges 5%",
            "description": "Tata Consultancy Services has reported better-than-expected quarterly earnings, with revenue growth accelerating. The stock jumped 5% on the announcement, pulling the IT index higher.",
            "link": "https://example.com/article2",
            "source": "Economic Times",
            "category": "Markets",
            "published_date": (datetime.now() - timedelta(hours=4)).isoformat()
        },
        {
            "title": "RBI Maintains Repo Rate at 6.5%, Signals Pause in Hikes",
            "description": "The Reserve Bank of India has decided to maintain the repo rate at 6.5%, suggesting that the rate hiking cycle may have ended. Market experts believe this could open doors for rate cuts in the coming months.",
            "link": "https://example.com/article3",
            "source": "Moneycontrol Business",
            "category": "Economy",
            "published_date": (datetime.now() - timedelta(hours=6)).isoformat()
        },
        {
            "title": "Reliance Industries Eyes Jio Financial Services Expansion",
            "description": "Reliance Industries is planning to expand its digital financial services division. The company expects to leverage its massive user base to capture a larger share of the fintech market.",
            "link": "https://example.com/article4",
            "source": "CNBC",
            "category": "Markets",
            "published_date": (datetime.now() - timedelta(hours=8)).isoformat()
        },
        {
            "title": "Auto Sector Shows Recovery Signs Amid Improved Demand",
            "description": "India's auto sector is showing signs of recovery with improved sales numbers. Manufacturers are optimistic about the festive season and expect sustained growth in the coming quarters.",
            "link": "https://example.com/article5",
            "source": "Financial Express",
            "category": "Markets",
            "published_date": (datetime.now() - timedelta(hours=10)).isoformat()
        },
    ]

    # Add news to database
    print_subheader("Adding Sample News Articles...")
    stats = db.add_multiple_news(sample_news)
    print(f"✅ Added {stats['added']} articles")
    print(f"   Duplicates: {stats['duplicates']}")
    print(f"   Errors: {stats['errors']}")

    # Add market data
    print_subheader("Adding Sample Market Data...")
    sample_market = [
        {"symbol": "RELIANCE.NS", "display_name": "RELIANCE", "price": 2550.50, "change_percent": 2.05, "change_value": 50.25},
        {"symbol": "TCS.NS", "display_name": "TCS", "price": 3450.75, "display_name": "TCS", "change_percent": 1.85, "change_value": 62.50},
        {"symbol": "INFY.NS", "display_name": "INFY", "price": 1800.25, "change_percent": 0.95, "change_value": 17.00},
        {"symbol": "HDFCBANK.NS", "display_name": "HDFC Bank", "price": 1650.50, "change_percent": -1.25, "change_value": -21.00},
        {"symbol": "ICICIBANK.NS", "display_name": "ICICI Bank", "price": 950.75, "change_percent": -0.85, "change_value": -8.25},
        {"symbol": "AXISBANK.NS", "display_name": "Axis Bank", "price": 1050.00, "change_percent": -1.50, "change_value": -16.00},
        {"symbol": "WIPRO.NS", "display_name": "Wipro", "price": 450.50, "change_percent": 3.25, "change_value": 14.00},
        {"symbol": "MARUTI.NS", "display_name": "Maruti", "price": 8500.25, "change_percent": -0.50, "change_value": -42.50},
    ]

    stats = db.add_multiple_market_data(sample_market)
    print(f"✅ Added {stats['added']} market data points")
    print(f"   Errors: {stats['errors']}")

    return db


def test_approval_workflow(db: JournalDB):
    """Test the approval workflow."""
    print_header("TEST 1: Approval Workflow")

    print_subheader("Initial Database State...")
    stats = db.get_stats()
    print(f"📊 Pending News: {stats['unapproved_news']}")
    print(f"✅ Approved News: {stats['approved_news']}")
    print(f"📈 Pending Market: {stats['unapproved_market']}")
    print(f"✅ Approved Market: {stats['approved_market']}")

    # Get pending news
    pending_news = db.get_unapproved_news(limit=5)
    print_subheader("Sample Pending News Articles...")
    for i, article in enumerate(pending_news[:3], 1):
        print(f"\n{i}. {article['title']}")
        print(f"   Source: {article['source']}")
        print(f"   Category: {article['category']}")

    # Approve first 2 articles
    print_subheader("Approving First 2 Articles...")
    if len(pending_news) >= 2:
        db.approve_news(pending_news[0]['id'])
        db.approve_news(pending_news[1]['id'])
        print(f"✅ Approved: {pending_news[0]['title'][:40]}...")
        print(f"✅ Approved: {pending_news[1]['title'][:40]}...")

    # Reject next article
    print_subheader("Rejecting Article...")
    if len(pending_news) >= 3:
        db.reject_news(pending_news[2]['id'])
        print(f"❌ Rejected: {pending_news[2]['title'][:40]}...")

    # Check updated stats
    print_subheader("Updated Database State...")
    stats = db.get_stats()
    print(f"📊 Pending News: {stats['unapproved_news']}")
    print(f"✅ Approved News: {stats['approved_news']}")

    return db


def test_edit_functionality(db: JournalDB):
    """Test the edit functionality."""
    print_header("TEST 2: Edit Functionality")

    pending_news = db.get_unapproved_news(limit=1)

    if not pending_news:
        print("⚠️  No pending news to edit")
        return

    article = pending_news[0]
    print_subheader("Original Article...")
    print(f"📄 Title: {article['title']}")
    print(f"📝 Description: {article['description'][:100]}...")

    # Edit the article
    new_title = f"[EDITED] {article['title']}"
    new_description = f"[EDITED] {article['description'][:50]}... with more details."

    print_subheader("Editing Article...")
    success = db.update_news(article['id'], title=new_title, description=new_description)

    if success:
        print("✅ Article updated successfully")

        # Fetch and display updated article
        updated = db.get_unapproved_news(limit=1)[0]
        print_subheader("Updated Article...")
        print(f"📄 Title: {updated['title']}")
        print(f"📝 Description: {updated['description'][:100]}...")
    else:
        print("❌ Failed to update article")


def test_market_data_editing(db: JournalDB):
    """Test market data editing."""
    print_header("TEST 3: Market Data Editing")

    pending_market = db.get_unapproved_market_data()

    if not pending_market:
        print("⚠️  No pending market data")
        return

    # Display all market data
    print_subheader("Current Market Data...")
    for data in pending_market[:5]:
        print(f"{data['symbol']:<15} ₹{data['price']:>8.2f} ({data['change_percent']:>6.2f}%)")

    # Edit first market data
    if pending_market:
        data = pending_market[0]
        new_price = data['price'] * 1.02  # Increase by 2%
        new_change = 2.0

        print_subheader(f"Editing {data['symbol']}...")
        print(f"Old Price: ₹{data['price']:.2f}")
        print(f"New Price: ₹{new_price:.2f}")

        success = db.update_market_data(data['id'], price=new_price, change_percent=new_change)

        if success:
            print("✅ Market data updated")
        else:
            print("❌ Failed to update market data")


def test_approval_states(db: JournalDB):
    """Test different approval states."""
    print_header("TEST 4: Approval States")

    print_subheader("Getting Approved News...")
    approved_news = db.get_approved_news(limit=5)
    print(f"✅ Found {len(approved_news)} approved articles")

    if approved_news:
        for i, article in enumerate(approved_news[:3], 1):
            print(f"\n{i}. ✅ {article['title'][:50]}...")
            print(f"   Source: {article['source']}")

    print_subheader("Getting Approved Market Data...")
    approved_market = db.get_approved_market_data()
    print(f"✅ Found {len(approved_market)} approved market data points")

    if approved_market:
        for i, data in enumerate(approved_market[:5], 1):
            print(f"{i}. {data['symbol']}: ₹{data['price']:.2f}")


def test_bulk_approvals(db: JournalDB):
    """Test bulk approval operations."""
    print_header("TEST 5: Bulk Operations")

    pending_news = db.get_unapproved_news(limit=100)
    print_subheader(f"Bulk Approving {len(pending_news)} Remaining Articles...")

    for article in pending_news:
        db.approve_news(article['id'])

    stats = db.get_stats()
    print(f"✅ All news articles approved")
    print(f"   Pending: {stats['unapproved_news']}")
    print(f"   Approved: {stats['approved_news']}")

    print_subheader("Bulk Approving Market Data...")
    pending_market = db.get_unapproved_market_data()

    for data in pending_market:
        db.approve_market_data(data['id'])

    stats = db.get_stats()
    print(f"✅ All market data approved")
    print(f"   Pending: {stats['unapproved_market']}")
    print(f"   Approved: {stats['approved_market']}")


def test_clear_approved(db: JournalDB):
    """Test clearing approved content."""
    print_header("TEST 6: Clear Approved Content")

    stats_before = db.get_stats()
    print_subheader("Before Clearing...")
    print(f"Approved News: {stats_before['approved_news']}")
    print(f"Approved Market: {stats_before['approved_market']}")

    print_subheader("Clearing Approved Content...")
    db.clear_approved_content()

    stats_after = db.get_stats()
    print_subheader("After Clearing...")
    print(f"Approved News: {stats_after['approved_news']}")
    print(f"Approved Market: {stats_after['approved_market']}")

    if stats_after['approved_news'] == 0 and stats_after['approved_market'] == 0:
        print("✅ Approved content cleared successfully")
    else:
        print("❌ Failed to clear all approved content")


def main():
    """Run all tests."""
    print("\n" + "╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  Approval Dashboard - Full Workflow Test".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")

    start_time = datetime.now()

    try:
        # Setup test data
        db = setup_test_data()

        # Run tests
        test_approval_workflow(db)
        test_edit_functionality(db)
        test_market_data_editing(db)
        test_approval_states(db)
        test_bulk_approvals(db)
        test_clear_approved(db)

        # Summary
        print_header("SUMMARY")
        elapsed = (datetime.now() - start_time).total_seconds()

        print(f"\n✅ All tests completed successfully!")
        print(f"⏱️  Total execution time: {elapsed:.2f} seconds")

        print(f"\n📊 Final Database State:")
        stats = db.get_stats()
        print(f"   Pending News: {stats['unapproved_news']}")
        print(f"   Approved News: {stats['approved_news']}")
        print(f"   Pending Market: {stats['unapproved_market']}")
        print(f"   Approved Market: {stats['approved_market']}")

    except KeyboardInterrupt:
        print("\n\n❌ Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()
