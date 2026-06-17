"""FinWiz Journal - Automated Finance Journal System."""

import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
import webbrowser

from modules.news_fetcher import NewsFetcher
from modules.market_data import MarketDataFetcher
from modules.database import JournalDB
from modules.journal_generator import JournalGenerator

# Page configuration
st.set_page_config(
    page_title="FinWiz Journal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
        color: #f1f5f9;
    }
    .stTabs [data-baseweb="tab-list"] button {
        background-color: #1e293b;
        color: #f1f5f9;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #7c3aed;
        color: white;
    }
    .article-card {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #7c3aed;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "db" not in st.session_state:
    st.session_state.db = JournalDB()
if "news_fetcher" not in st.session_state:
    st.session_state.news_fetcher = NewsFetcher()
if "market_fetcher" not in st.session_state:
    st.session_state.market_fetcher = MarketDataFetcher()
if "journal_generator" not in st.session_state:
    st.session_state.journal_generator = JournalGenerator()
if "selected_news" not in st.session_state:
    st.session_state.selected_news = set()
if "selected_market" not in st.session_state:
    st.session_state.selected_market = set()

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    st.markdown("---")

    # Display stats
    stats = st.session_state.db.get_stats()
    st.markdown("### 📊 Content Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("News (Pending)", stats["unapproved_news"])
        st.metric("Market (Pending)", stats["unapproved_market"])
    with col2:
        st.metric("News (Approved)", stats["approved_news"])
        st.metric("Market (Approved)", stats["approved_market"])

    st.markdown("---")

    # Configuration
    st.markdown("### 🔧 Configuration")
    auto_fetch = st.checkbox("Auto-fetch on load", value=False)
    limit_per_feed = st.slider("News items per feed", 1, 20, 10)

    st.markdown("---")

    # Help section
    st.markdown("### 📚 Help")
    st.info("""
    **Workflow:**
    1. 📥 Fetch data from news feeds and market APIs
    2. ✅ Review and approve content
    3. 📄 Generate HTML journal
    4. 📥 Download your journal

    **Tips:**
    - Fetch fresh data regularly
    - Review content before approval
    - Generate journal after approvals
    """)


# Main content
st.title("📊 FinWiz Journal")
st.markdown("*Automated Financial News & Market Data Journal System*")
st.markdown("---")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["📈 Dashboard", "📥 Fetch Data", "✅ Approve Content", "📄 Generate Journal"])

# ==================== TAB 1: DASHBOARD ====================
with tab1:
    st.header("Dashboard")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Pending News", stats["unapproved_news"], delta=None)
    with col2:
        st.metric("Approved News", stats["approved_news"], delta=None)
    with col3:
        st.metric("Pending Market Data", stats["unapproved_market"], delta=None)
    with col4:
        st.metric("Approved Market Data", stats["approved_market"], delta=None)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📰 Recent News (Last 10)")
        recent_news = st.session_state.db.get_unapproved_news(limit=10)
        if recent_news:
            for news in recent_news[:5]:
                with st.container():
                    st.markdown(f"""
                    **{news['title']}**
                    - Source: {news['source']}
                    - Category: {news['category']}
                    """)
        else:
            st.info("No pending news articles")

    with col2:
        st.subheader("📈 Recent Market Data")
        recent_market = st.session_state.db.get_unapproved_market_data()
        if recent_market:
            df = pd.DataFrame(recent_market)
            df = df[['symbol', 'price', 'change_percent']].head(10)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No pending market data")

    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 Refresh Stats", key="refresh_stats"):
            st.rerun()
    with col2:
        if st.button("🗑️ Clear All Approved", key="clear_approved"):
            st.session_state.db.clear_approved_content()
            st.success("Cleared all approved content!")
            st.rerun()

# ==================== TAB 2: FETCH DATA ====================
with tab2:
    st.header("📥 Fetch Data")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📰 Fetch News")
        if st.button("🔄 Fetch News from RSS Feeds", key="fetch_news"):
            with st.spinner("Fetching news from feeds..."):
                fetched_news = st.session_state.news_fetcher.fetch_all_news(
                    limit_per_feed=limit_per_feed
                )
                added_count = 0
                for news in fetched_news:
                    result = st.session_state.db.add_news(
                        title=news["title"],
                        description=news["description"],
                        link=news["link"],
                        source=news["source"],
                        published_date=news.get("published_date"),
                        category=news.get("category", "General"),
                    )
                    if result != -1:
                        added_count += 1

                st.success(f"✅ Added {added_count} new articles (duplicates skipped)")

        st.markdown("---")
        st.write("**Available News Sources:**")
        for source in st.session_state.news_fetcher.feeds.keys():
            st.write(f"- {source}")

    with col2:
        st.subheader("📈 Fetch Market Data")
        if st.button("🔄 Fetch Market Data", key="fetch_market"):
            with st.spinner("Fetching market data..."):
                market_data = st.session_state.market_fetcher.fetch_market_data()
                added_count = 0
                for data in market_data:
                    result = st.session_state.db.add_market_data(
                        symbol=data["symbol"],
                        price=data["price"],
                        change_percent=data["change_percent"],
                        change_value=data["change_value"],
                    )
                    if result != -1:
                        added_count += 1

                st.success(f"✅ Added {added_count} market data points")

        st.markdown("---")
        st.write("**Available Symbols:**")
        for name, symbol in st.session_state.market_fetcher.symbols.items():
            st.write(f"- {name}: {symbol}")

    st.markdown("---")

    # Preview fetched data
    st.subheader("👀 Preview Pending Data")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Pending News Articles**")
        pending_news = st.session_state.db.get_unapproved_news(limit=20)
        if pending_news:
            st.write(f"Total: {len(pending_news)} articles")
            for news in pending_news[:5]:
                with st.expander(f"📄 {news['title'][:50]}..."):
                    st.write(f"**Source:** {news['source']}")
                    st.write(f"**Category:** {news['category']}")
                    st.write(f"**Description:** {news['description'][:200]}...")
                    st.write(f"**Link:** [{news['link']}]({news['link']})")
        else:
            st.info("No pending news articles")

    with col2:
        st.write("**Pending Market Data**")
        pending_market = st.session_state.db.get_unapproved_market_data()
        if pending_market:
            df = pd.DataFrame(pending_market)
            st.dataframe(
                df[['symbol', 'price', 'change_value', 'change_percent']].head(10),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No pending market data")

# ==================== TAB 3: APPROVE CONTENT ====================
with tab3:
    st.header("✅ Approve Content")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📰 News Articles")
        pending_news = st.session_state.db.get_unapproved_news(limit=50)

        if pending_news:
            st.write(f"Total pending: {len(pending_news)} articles")

            # Bulk action buttons
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("✅ Approve All", key="approve_all_news"):
                    for news in pending_news:
                        st.session_state.db.approve_news(news["id"])
                    st.success(f"Approved {len(pending_news)} articles!")
                    st.rerun()

            with col_b:
                if st.button("❌ Reject All", key="reject_all_news"):
                    for news in pending_news:
                        st.session_state.db.reject_news(news["id"])
                    st.success(f"Rejected {len(pending_news)} articles!")
                    st.rerun()

            st.markdown("---")

            # Individual news items
            for news in pending_news:
                with st.container():
                    col_checkbox, col_content = st.columns([0.1, 0.9])

                    with col_checkbox:
                        if st.checkbox("Select", key=f"news_select_{news['id']}"):
                            st.session_state.selected_news.add(news["id"])

                    with col_content:
                        st.markdown(f"**{news['title']}**")
                        st.markdown(f"*Source: {news['source']} | Category: {news['category']}*")
                        st.write(news["description"][:200] + "...")

                        col_1, col_2, col_3 = st.columns(3)
                        with col_1:
                            if st.button("✅ Approve", key=f"approve_news_{news['id']}"):
                                st.session_state.db.approve_news(news["id"])
                                st.success("Approved!")
                                st.rerun()
                        with col_2:
                            if st.button("❌ Reject", key=f"reject_news_{news['id']}"):
                                st.session_state.db.reject_news(news["id"])
                                st.success("Rejected!")
                                st.rerun()
                        with col_3:
                            st.markdown(f"[🔗 View]({news['link']})")

                    st.markdown("---")
        else:
            st.info("✅ No pending news articles - great job!")

    with col2:
        st.subheader("📈 Market Data")
        pending_market = st.session_state.db.get_unapproved_market_data()

        if pending_market:
            st.write(f"Total pending: {len(pending_market)} data points")

            # Bulk actions
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("✅ Approve All", key="approve_all_market"):
                    for data in pending_market:
                        st.session_state.db.approve_market_data(data["id"])
                    st.success(f"Approved {len(pending_market)} data points!")
                    st.rerun()

            with col_b:
                if st.button("❌ Reject All", key="reject_all_market"):
                    for data in pending_market:
                        st.session_state.db.reject_market_data(data["id"])
                    st.success(f"Rejected {len(pending_market)} data points!")
                    st.rerun()

            st.markdown("---")

            # Individual market data
            df = pd.DataFrame(pending_market)
            for idx, row in df.iterrows():
                col_1, col_2, col_3 = st.columns([0.7, 0.15, 0.15])

                with col_1:
                    st.write(f"**{row['symbol']}** - ₹{row['price']} ({row['change_percent']:+.2f}%)")

                with col_2:
                    if st.button("✅", key=f"approve_market_{row['id']}"):
                        st.session_state.db.approve_market_data(row["id"])
                        st.rerun()

                with col_3:
                    if st.button("❌", key=f"reject_market_{row['id']}"):
                        st.session_state.db.reject_market_data(row["id"])
                        st.rerun()

        else:
            st.info("✅ No pending market data")

# ==================== TAB 4: GENERATE JOURNAL ====================
with tab4:
    st.header("📄 Generate Journal")

    st.info("📝 Journal will be generated from all approved content")

    col1, col2 = st.columns(2)

    with col1:
        approved_news = st.session_state.db.get_approved_news(limit=1000)
        st.metric("Approved News", len(approved_news))

    with col2:
        approved_market = st.session_state.db.get_approved_market_data()
        st.metric("Approved Market Data", len(approved_market))

    st.markdown("---")

    if st.button("📄 Generate HTML Journal", key="generate_journal", type="primary"):
        if approved_news or approved_market:
            with st.spinner("Generating journal..."):
                approved_news_list = [
                    {
                        "title": news["title"],
                        "description": news["description"],
                        "link": news["link"],
                        "source": news["source"],
                        "published_date": news.get("published_date", ""),
                        "category": news.get("category", "General"),
                    }
                    for news in approved_news
                ]

                approved_market_list = [
                    {
                        "symbol": data["symbol"],
                        "price": data["price"],
                        "change_value": data["change_value"],
                        "change_percent": data["change_percent"],
                        "display_name": data["symbol"].replace(".NS", ""),
                    }
                    for data in approved_market
                ]

                output_path = st.session_state.journal_generator.generate_journal(
                    approved_news_list,
                    approved_market_list
                )

                st.session_state.db.save_journal_metadata(
                    output_path,
                    len(approved_news),
                    len(approved_market)
                )

                st.success(f"✅ Journal generated successfully!")
                st.write(f"**Location:** {output_path}")

                # Read and display HTML for preview
                with open(output_path, "r", encoding="utf-8") as f:
                    html_content = f.read()

                # Download button
                st.download_button(
                    label="📥 Download HTML Journal",
                    data=html_content,
                    file_name=Path(output_path).name,
                    mime="text/html",
                )

                # Preview option
                if st.checkbox("👀 Preview Journal (in new tab)"):
                    st.markdown(f"[Open Preview]({output_path})", unsafe_allow_html=True)
                    st.info("Click the link above to preview the journal in a new tab")

                # Clear approved content after generation
                if st.checkbox("Clear approved content after generation"):
                    if st.button("🗑️ Clear"):
                        st.session_state.db.clear_approved_content()
                        st.success("Cleared all approved content!")
                        st.rerun()

        else:
            st.warning("⚠️ No approved content to generate journal. Please approve content first.")

    st.markdown("---")

    st.subheader("📊 Journal History")
    # Note: In production, you'd fetch from database
    st.info("Journal history will be displayed here once journals are generated.")

# Footer
st.markdown("---")
st.markdown("""
<center>

**FinWiz Journal** - Automated Financial News & Market Data Journal System
Built for the University Finance Club

</center>
""", unsafe_allow_html=True)
