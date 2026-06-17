# FinWiz Journal - Data Fetching Test Guide

## 🧪 Running the Test Suite

This guide will help you run the comprehensive test script for all data fetching modules.

---

## 📋 What Gets Tested

The test script (`test_data_fetching.py`) validates:

### Test 1: News Fetcher
- ✅ Connects to 4 RSS feeds (Reuters, Economic Times, Moneycontrol, CNBC)
- ✅ Parses feed entries correctly
- ✅ Extracts title, summary, link, source, category
- ✅ Removes HTML tags and cleans text
- ✅ Detects and removes duplicate articles
- ✅ Handles errors gracefully

### Test 2: Market Data Fetcher
- ✅ Fetches Nifty 50 index data
- ✅ Fetches Sensex index data
- ✅ Fetches prices for 20 major stocks
- ✅ Calculates price changes and percentages
- ✅ Identifies top 5 gainers
- ✅ Identifies top 5 losers
- ✅ Handles errors gracefully

### Test 3: Database Operations
- ✅ Creates tables automatically
- ✅ Stores news articles with metadata
- ✅ Stores market data with timestamps
- ✅ Handles duplicate detection
- ✅ Retrieves articles and data correctly
- ✅ Manages approval status
- ✅ Generates statistics

---

## 🚀 How to Run the Test

### Prerequisites
1. Virtual environment should be activated
2. Dependencies should be installed
3. Internet connection required

### Step 1: Navigate to Project
```bash
cd C:\Users\pulig\OneDrive\Documents\Mase cap\finwizjournal
```

### Step 2: Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Step 3: Run the Test Script
```bash
python test_data_fetching.py
```

### Expected Output

```
======================================================================
  FinWiz Journal - Data Fetching Test Suite
======================================================================

======================================================================
  TEST 1: NEWS FETCHER
======================================================================

🔄 Initializing NewsFetcher...
📰 Configured RSS Feeds:
   • Reuters Business: https://feeds.reuters.com/reuters/businessNews
   • Economic Times: https://economictimes.indiatimes.com/feed/
   • Moneycontrol Business: https://feeds.moneycontrol.com/news/business/
   • CNBC: https://feeds.cnbc.com/id/100003114/rss.html

──────────────────────────────────────────────────────────────────────

📌 Fetching news from all sources...
──────────────────────────────────────────────────────────────────────

✅ Fetch Complete!
   Total fetched: ~20 entries
   Unique articles: ~18-20
   Duplicates removed: 0-2
   Feed errors: 0

📌 Sample Articles (showing first 3 of X)
──────────────────────────────────────────────────────────────────────

📰 Article 1:
   Title: Sample Article Title...
   Source: Reuters Business
   Category: Markets
   Date: 2024-06-17
   Link: https://example.com/article1...

[... continues for Articles 2 and 3 ...]

======================================================================
  TEST 2: MARKET DATA FETCHER
======================================================================

🔄 Initializing MarketDataFetcher...

📌 Fetching Market Indices...
──────────────────────────────────────────────────────────────────────

📊 Market Indices:
   📈 Nifty 50: 18500.00 (+0.50%)
   📉 Sensex: 61500.00 (-0.25%)

📌 Fetching Nifty 50 Top Movers...
──────────────────────────────────────────────────────────────────────

✅ Fetch Complete!
   Stocks fetched: 20
   Fetch errors: 0

📈 Top 5 Gainers:
   1. RELIANCE        ₹2550.00 (+2.50%)
   2. TCS             ₹3450.00 (+1.80%)
   3. INFY            ₹1800.00 (+1.25%)
   [... continues ...]

📉 Top 5 Losers:
   1. MARUTI          ₹8500.00 (-1.50%)
   2. BAJAJ AUTO      ₹3200.00 (-0.80%)
   [... continues ...]

======================================================================
  TEST 3: DATABASE OPERATIONS
======================================================================

🔄 Initializing JournalDB...

📌 Adding News Articles to Database...
──────────────────────────────────────────────────────────────────────

✅ Articles Added:
   Successfully added: 18
   Duplicates skipped: 2
   Errors: 0

📌 Adding Market Data to Database...
──────────────────────────────────────────────────────────────────────

✅ Market Data Added:
   Successfully added: 10
   Errors: 0

📌 Database Statistics...
──────────────────────────────────────────────────────────────────────

📊 Content in Database:
   Pending news articles: 18
   Approved news articles: 0
   Pending market data: 10
   Approved market data: 0

[... continues with sample retrievals ...]

======================================================================
  SUMMARY
======================================================================

✅ All tests completed successfully!
⏱️  Total execution time: 15.23 seconds

📊 Final Statistics:
   News articles fetched: 18
   Market data points fetched: 10
   Total items processed: 28
```

---

## 📊 Understanding Test Results

### News Fetcher Results

| Metric | Expected | Notes |
|--------|----------|-------|
| Feeds Configured | 4 | Reuters, Economic Times, Moneycontrol, CNBC |
| Total Entries | 15-20 | 5 per feed × 4 feeds |
| Unique Articles | 13-20 | Some duplicates possible |
| Duplicates | 0-2 | Detected via MD5 hash |
| Errors | 0 | Feeds may be temporarily unavailable |

### Market Data Results

| Metric | Expected | Notes |
|--------|----------|-------|
| Indices | 2 | Nifty 50 + Sensex |
| Stocks Fetched | 20 | Nifty 50 constituents |
| Top Gainers | 5 | With highest % gain |
| Top Losers | 5 | With lowest % gain |
| Errors | 0-1 | May vary by network |

### Database Results

| Metric | Expected | Notes |
|--------|----------|-------|
| News Added | 13-20 | Excluding duplicates |
| Market Added | 10 | All stocks + indices |
| Duplicates | 0-2 | Handled automatically |
| Approval Status | pending | Initially all pending |

---

## 🛠️ Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'feedparser'"

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "No articles fetched"

**Causes:**
- Internet connection down
- RSS feed URLs are unreachable
- Feed format changed

**Solutions:**
1. Check internet: `ping google.com`
2. Check URL manually in browser
3. Try again in 5 minutes (feeds may be updating)

### Issue: "No market data fetched"

**Causes:**
- yfinance rate limiting
- Market may be closed
- Symbol errors

**Solutions:**
1. Wait 5 minutes before retrying
2. Check if market is open (NSE trading hours)
3. Verify internet connection

### Issue: "Database error: table news_articles already exists"

**Solution:**
Delete the old database and restart:
```bash
rm data/finwiz.db
python test_data_fetching.py
```

### Issue: "Execution takes very long (> 30 seconds)"

**Causes:**
- Slow internet
- RSS feeds not responding
- yfinance timeout

**Solutions:**
1. Check internet speed
2. Try again later
3. Increase timeout in code if needed

---

## 📝 Test Output Files

### Console Output
The test script prints detailed output to console showing:
- Fetch statistics
- Sample articles
- Market data details
- Database contents
- Execution time

### Database File
- Location: `data/finwiz.db`
- Size: ~1-5 MB (increases with each run)
- Contains: news_articles, market_data, generated_journals tables

---

## ✅ Verification Checklist

After running the test, verify:

- [ ] Test completes without errors
- [ ] News articles are fetched (≥ 10)
- [ ] Market data is fetched (≥ 10)
- [ ] Database file exists: `data/finwiz.db`
- [ ] Tables created: `news_articles`, `market_data`
- [ ] Articles have proper fields: title, link, source
- [ ] Market data has proper fields: symbol, price, change_percent
- [ ] Execution time is reasonable (< 60 seconds)

---

## 🔄 Running Tests Regularly

### Daily Test
```bash
# Quick test to verify system is working
python test_data_fetching.py
```

### After Making Changes
```bash
# Test any modifications you made
python test_data_fetching.py
```

### Before Deployment
```bash
# Full validation before going live
python test_data_fetching.py
```

---

## 📊 Next Steps After Testing

1. **If tests pass:**
   - Start the Streamlit app: `streamlit run app.py`
   - Try "Fetch Latest Data" button
   - Approve content
   - Generate journal

2. **If tests fail:**
   - Check troubleshooting section above
   - Verify internet connection
   - Check RSS feed URLs
   - Review error messages

---

## 📚 Related Files

- **News Fetcher:** `modules/news_fetcher.py`
- **Market Data:** `modules/market_data.py`
- **Database:** `modules/database.py`
- **Streamlit App:** `app.py`
- **Requirements:** `requirements.txt`

---

## 💡 Tips

1. **First time run:** May take 15-30 seconds due to data fetching
2. **RSS feeds:** May be slow on first request
3. **Market data:** Fastest during NSE trading hours (9:15 AM - 3:30 PM IST)
4. **Run before bedtime:** Takes time but doesn't need interaction
5. **Check logs:** Monitor test output for any warnings

---

## 🚀 Performance Benchmarks

Typical execution times on a good internet connection:

| Component | Time | Notes |
|-----------|------|-------|
| News fetching | 5-10s | Depends on feed responsiveness |
| Market data | 3-8s | Depends on yfinance |
| Database ops | 1-2s | Local SQLite |
| **Total** | **15-25s** | Typical full run |

---

## 📞 Getting Help

If you encounter issues:

1. **Check SETUP.md** - General setup issues
2. **Review error message** - Often shows the root cause
3. **Test internet connection** - Most issues are network-related
4. **Try again later** - Feeds may be temporarily unavailable
5. **Check requirements.txt** - Ensure all packages installed

---

**Last Updated:** 2026-06-17
**Test Script Version:** 1.0
**Status:** ✅ Production Ready
