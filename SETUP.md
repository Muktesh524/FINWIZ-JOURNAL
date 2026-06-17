# FinWiz Journal - Setup & Installation Guide

## 📋 Prerequisites

- **Python 3.8+** (Download from python.org)
- **pip** (comes with Python)
- **Git** (optional, for version control)

## 🚀 Quick Start (5 minutes)

### Step 1: Open Terminal/Command Prompt

Navigate to the project directory:
```bash
cd "C:\Users\pulig\OneDrive\Documents\Mase cap\finwizjournal"
```

### Step 2: Create Virtual Environment

#### On Windows (Command Prompt):
```bash
python -m venv venv
venv\Scripts\activate
```

#### On Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- streamlit (UI framework)
- pandas (data handling)
- yfinance (market data)
- feedparser (RSS feeds)
- jinja2 (HTML templating)
- python-dateutil (date parsing)

### Step 4: Run the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 📁 Project Structure Explained

```
finwizjournal/
├── app.py                           # Main Streamlit application (entry point)
├── requirements.txt                 # Python dependencies
├── README.md                        # Project overview
├── SETUP.md                         # This file
│
├── modules/                         # Core Python modules
│   ├── __init__.py
│   ├── news_fetcher.py             # Fetch news from RSS feeds
│   ├── market_data.py              # Fetch market data from yfinance
│   ├── database.py                 # SQLite database operations
│   └── journal_generator.py        # Generate HTML journals from data
│
├── templates/                       # Jinja2 HTML templates
│   ├── base.html                   # Base template (dark theme, styling)
│   ├── journal.html                # Main journal layout
│   ├── news_section.html           # News articles section
│   └── market_section.html         # Market data section
│
└── data/                           # Data storage directory
    ├── .gitkeep                    # Empty file to track directory
    └── finwiz.db                   # SQLite database (created on first run)
```

---

## 🎯 How to Use the Application

### 1️⃣ Dashboard Tab
- **Overview of the system**
- View pending and approved content counts
- See recent news and market data
- Quick access to refresh stats

### 2️⃣ Fetch Data Tab
- **📰 Fetch News**: Download articles from RSS feeds (Financial Express, Moneycontrol, Economic Times, Yahoo Finance)
- **📈 Fetch Market Data**: Get current prices for Nifty 50 and major stocks
- **Preview pending data** before approval

### 3️⃣ Approve Content Tab
- **Review news articles**: Read titles, descriptions, and sources
- **Review market data**: Check stock prices and changes
- **Individual approval**: Approve/reject items one by one
- **Bulk operations**: Approve/reject all items at once
- **Selection**: Mark items for bulk processing

### 4️⃣ Generate Journal Tab
- **Generate HTML**: Create a professional journal from approved content
- **Preview**: View journal in browser before downloading
- **Download**: Save journal as HTML file
- **Auto-clear**: Clear approved content after generation (optional)

---

## 📊 Database Schema

### news_articles table
```sql
- id: Unique identifier
- title: Article title
- description: Article summary
- link: URL to article
- source: News source (Financial Express, Moneycontrol, etc.)
- published_date: Article publication date
- fetched_date: When article was fetched
- approved: 0 (pending) or 1 (approved)
- category: Article category (Markets, Economy, General, etc.)
```

### market_data table
```sql
- id: Unique identifier
- symbol: Stock symbol (e.g., RELIANCE.NS)
- price: Current price
- change_percent: Percentage change
- change_value: Absolute price change
- fetched_date: When data was fetched
- approved: 0 (pending) or 1 (approved)
```

### generated_journals table
```sql
- id: Unique identifier
- created_date: When journal was generated
- file_path: Path to generated HTML file
- news_count: Number of articles in journal
- market_data_count: Number of market data points
- metadata_json: Additional metadata
```

---

## 🔧 Configuration

### Modify News Sources

Edit `modules/news_fetcher.py`:
```python
RSS_FEEDS = {
    "Financial Express": "https://www.financialexpress.com/feed/",
    "Moneycontrol": "https://feeds.moneycontrol.com/news/business/",
    "Economic Times": "https://economictimes.indiatimes.com/feed/",
    "Yahoo Finance": "https://feeds.finance.yahoo.com/rss/2.0/headline",
    # Add more feeds here
}
```

### Modify Stock Symbols

Edit `modules/market_data.py`:
```python
DEFAULT_SYMBOLS = {
    "NIFTY_50": "^NSEI",
    "RELIANCE": "RELIANCE.NS",
    "TCS": "TCS.NS",
    # Add or modify symbols here
}
```

### Customize HTML Template

Edit `templates/journal.html` for styling and layout changes.

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'streamlit'"

**Solution:** Make sure virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: "No module named 'modules'"

**Solution:** Make sure you're running the app from the project root directory:
```bash
cd C:\Users\pulig\OneDrive\Documents\Mase cap\finwizjournal
streamlit run app.py
```

### Issue: RSS feed not working

**Solution:** 
1. Check internet connection
2. Verify feed URL is correct
3. Some feeds may require user-agent headers (we handle this with feedparser)

### Issue: yfinance not fetching data

**Solution:**
1. Check internet connection
2. Verify stock symbols are correct (e.g., RELIANCE.NS, not just RELIANCE)
3. Some symbols may not have data available

### Issue: Database file not created

**Solution:** The database is created automatically on first run. If it doesn't appear:
1. Check that `data/` directory exists
2. Check file permissions on the directory
3. Try deleting `data/finwiz.db` and running again

---

## 📈 Workflow Example

### Generate a Journal in 5 Steps:

1. **Fetch News**
   - Go to "Fetch Data" tab
   - Click "Fetch News from RSS Feeds"
   - Wait for completion

2. **Fetch Market Data**
   - Click "Fetch Market Data"
   - Wait for completion
   - Data appears in preview

3. **Review & Approve**
   - Go to "Approve Content" tab
   - Review news articles (click to expand)
   - Approve individual items or use "Approve All"
   - Review and approve market data

4. **Generate Journal**
   - Go to "Generate Journal" tab
   - Verify approved content counts
   - Click "Generate HTML Journal"
   - Wait for generation

5. **Download**
   - Click "Download HTML Journal" button
   - Save the file to your computer
   - Open in any web browser

---

## 🔐 Security Notes

- **Database**: SQLite database is stored locally in `data/` directory
- **No sensitive data**: System doesn't store credentials or personal information
- **RSS feeds**: Public feeds from news websites only
- **yfinance**: Public market data from Yahoo Finance

---

## 📱 Browser Compatibility

The generated journal works on:
- ✅ Chrome/Chromium
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Mobile browsers

The journal is responsive and works on mobile devices.

---

## 🚀 Performance Tips

1. **Limit articles per feed**: Reduce "News items per feed" in sidebar to fetch faster
2. **Batch approvals**: Use "Approve All" to process large amounts quickly
3. **Clear old data**: Use "Clear All Approved" to keep database size small
4. **Browser caching**: Journal files can be large; browser caching helps

---

## 📦 Dependencies Explained

| Package | Purpose | Version |
|---------|---------|---------|
| streamlit | Web framework for the UI | 1.28.1 |
| pandas | Data manipulation | 2.0.3 |
| yfinance | Market data fetching | 0.2.32 |
| feedparser | RSS feed parsing | 6.0.10 |
| jinja2 | HTML templating | 3.1.2 |
| python-dateutil | Date parsing | 2.8.2 |
| requests | HTTP requests | 2.31.0 |

---

## 🎓 Learning Resources

- **Streamlit Docs**: https://docs.streamlit.io/
- **Jinja2 Docs**: https://jinja.palletsprojects.com/
- **yfinance Docs**: https://yfinance.readthedocs.io/
- **feedparser Docs**: https://feedparser.readthedocs.io/

---

## ❓ FAQ

**Q: Can I customize the HTML template?**
A: Yes! Edit `templates/journal.html` and change styling in `templates/base.html`.

**Q: Can I add more news sources?**
A: Yes! Add RSS feed URLs to `DEFAULT_SYMBOLS` in `modules/news_fetcher.py`.

**Q: Can I add different stock symbols?**
A: Yes! Modify `DEFAULT_SYMBOLS` in `modules/market_data.py`.

**Q: How often should I fetch data?**
A: Depends on your needs. Daily fetching is common for finance journals.

**Q: Can I export to PDF?**
A: Generated HTML can be printed to PDF using browser's print function (Ctrl+P).

**Q: Is there a way to schedule automatic generation?**
A: This is planned for Phase 2. Currently, generation is manual.

---

## 📞 Support

For issues or suggestions, create an issue in the project repository or contact the Finance Club.

---

## 🔄 Next Steps (Phase 2)

- Email integration (send journal via Gmail)
- Zerodha integration (fetch portfolio data)
- Scheduled automatic generation
- Template customization UI
- Advanced filtering and search
- Analytics dashboard

---

## 📄 License

Internal use only - University Finance Club

**Last Updated:** 2026-06-17
