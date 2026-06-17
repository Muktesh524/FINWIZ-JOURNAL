# FinWiz Journal - Automated Finance Journal System

An automated system that fetches news and market data, allows user review/approval through a clean Streamlit interface, and generates a professional multi-page HTML journal.

## 📋 Project Overview

FinWiz Journal automates the creation of finance club journals by:
1. Fetching financial news from multiple RSS feeds
2. Pulling market data (stock prices, indices)
3. Providing a review/approval interface
4. Generating a professional HTML journal with Jinja2 templates

## 🏗️ Project Structure

```
finwizjournal/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── modules/
│   ├── __init__.py
│   ├── news_fetcher.py       # RSS feed parsing & news fetching
│   ├── market_data.py        # yfinance data fetching
│   ├── database.py           # SQLite database operations
│   └── journal_generator.py  # HTML journal generation
├── templates/                # Jinja2 HTML templates
│   ├── base.html             # Base template
│   ├── journal.html          # Main journal template
│   ├── news_section.html     # News section component
│   └── market_section.html   # Market data section component
└── data/                     # Data storage
    └── .gitkeep
```

## 🚀 Quick Start

### 1. Create Virtual Environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📱 Features

### Dashboard Tab
- Overview of the system
- Recent activity logs
- Quick statistics

### Fetch Data Tab
- Fetch news from configured RSS feeds
- Fetch market data (Nifty movers, stock prices)
- Preview fetched data before approval

### Approve Content Tab
- Review fetched news articles
- Review market data
- Approve/reject individual items
- Bulk approve/reject

### Generate Journal Tab
- Generate HTML journal from approved content
- Preview journal
- Download generated journal

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Data Fetching**: feedparser (RSS), yfinance (market data)
- **Templating**: Jinja2
- **Database**: SQLite
- **Language**: Python 3.8+

## 📊 Supported Data Sources

### News Sources
- Financial Express
- Moneycontrol
- Economic Times
- Yahoo Finance

### Market Data
- Nifty 50 index
- Stock prices
- Market movers

## 🔄 Workflow

1. **Fetch**: Automatically fetch news and market data
2. **Review**: User reviews fetched content in Streamlit UI
3. **Approve**: Select content to include in the journal
4. **Generate**: System creates HTML journal with approved content
5. **Download**: User downloads the generated journal

## 📝 Phase 1 (Current)
- News fetching (RSS feeds)
- Market data fetching (yfinance)
- Basic Streamlit UI
- SQLite storage
- HTML journal generation with Jinja2

## 📋 Phase 2 (Future)
- Gmail integration (send journal via email)
- Zerodha integration (fetch live portfolio data)
- Advanced filtering and search
- Scheduled automatic generation
- Template customization

## 🤝 Contributing

This project is for the university finance club. For questions or suggestions, contact the club.

## 📄 License

Internal use only.
