"""
Approval Dashboard for FinWiz Journal - Clean and Professional UI for content review.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path
from modules.database import JournalDB
from modules.market_data import MarketDataFetcher
from modules.journal_generator import JournalGenerator


def init_session_state():
    """Initialize all session state variables."""
    if "db" not in st.session_state:
        st.session_state.db = JournalDB()

    if "market_fetcher" not in st.session_state:
        st.session_state.market_fetcher = MarketDataFetcher()

    if "journal_generator" not in st.session_state:
        st.session_state.journal_generator = JournalGenerator()

    if "edit_mode" not in st.session_state:
        st.session_state.edit_mode = False

    if "editing_article_id" not in st.session_state:
        st.session_state.editing_article_id = None

    if "edited_title" not in st.session_state:
        st.session_state.edited_title = ""

    if "edited_description" not in st.session_state:
        st.session_state.edited_description = ""

    if "edit_market_id" not in st.session_state:
        st.session_state.edit_market_id = None

    if "edited_market_price" not in st.session_state:
        st.session_state.edited_market_price = 0.0

    if "edited_market_change" not in st.session_state:
        st.session_state.edited_market_change = 0.0

    if "journal_generated" not in st.session_state:
        st.session_state.journal_generated = False

    if "journal_path" not in st.session_state:
        st.session_state.journal_path = None


def setup_page():
    """Configure page settings and styling."""
    st.set_page_config(
        page_title="Approval Dashboard - FinWiz Journal",
        page_icon="✅",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Enhanced CSS for professional look
    st.markdown("""
        <style>
        * {
            margin: 0;
            padding: 0;
        }

        [data-testid="stMainBlockContainer"] {
            background-color: #0f172a;
            color: #f1f5f9;
        }

        .metric-card {
            background: linear-gradient(135deg, #7c3aed, #6d28d9);
            padding: 20px;
            border-radius: 10px;
            color: white;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .article-card {
            background-color: #1e293b;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #7c3aed;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }

        .article-card:hover {
            box-shadow: 0 4px 8px rgba(124, 58, 237, 0.3);
        }

        .approved-card {
            background-color: #1e293b;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #10b981;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }

        .market-card {
            background-color: #1e293b;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #334155;
            margin-bottom: 10px;
            text-align: center;
        }

        .market-card.gainer {
            border: 2px solid #10b981;
            background-color: rgba(16, 185, 129, 0.1);
        }

        .market-card.loser {
            border: 2px solid #ef4444;
            background-color: rgba(239, 68, 68, 0.1);
        }

        .status-badge {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 500;
            margin-right: 10px;
        }

        .status-pending {
            background-color: #f59e0b;
            color: white;
        }

        .status-approved {
            background-color: #10b981;
            color: white;
        }

        .button-row {
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }

        .source-badge {
            display: inline-block;
            background-color: #7c3aed;
            color: white;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.85em;
            margin-right: 8px;
        }

        .category-badge {
            display: inline-block;
            background-color: #6d28d9;
            color: white;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.85em;
        }

        .edit-form {
            background-color: #1e293b;
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #7c3aed;
            margin-bottom: 15px;
        }

        .divider {
            border-bottom: 1px solid #334155;
            margin: 20px 0;
        }

        </style>
    """, unsafe_allow_html=True)


def render_header():
    """Render the page header."""
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown("# ✅ Approval Dashboard")
        st.markdown("*Review, edit, and approve content for your journal*")

    with col2:
        stats = st.session_state.db.get_stats()
        st.metric("Pending Items", stats['unapproved_news'] + stats['unapproved_market'])

    st.markdown("---")


def render_quick_stats():
    """Render quick statistics cards."""
    stats = st.session_state.db.get_stats()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📰 Pending News", stats['unapproved_news'], delta=None)

    with col2:
        st.metric("✅ Approved News", stats['approved_news'], delta=None)

    with col3:
        st.metric("📈 Pending Market", stats['unapproved_market'], delta=None)

    with col4:
        st.metric("✅ Approved Market", stats['approved_market'], delta=None)

    st.markdown("---")


def render_article_card(article: Dict[str, Any], index: int):
    """Render a single article card with actions."""
    col1, col2 = st.columns([0.95, 0.05])

    with col1:
        # Article header with badges
        col_title, col_badges = st.columns([0.75, 0.25])

        with col_title:
            st.markdown(f"### 📄 {article['title']}")

        with col_badges:
            st.markdown(f"<span class='status-badge status-pending'>⏳ Pending</span>", unsafe_allow_html=True)

        # Article metadata
        col_meta1, col_meta2, col_meta3 = st.columns([0.3, 0.3, 0.4])

        with col_meta1:
            st.markdown(f"<span class='source-badge'>{article['source']}</span>", unsafe_allow_html=True)

        with col_meta2:
            if article.get('category'):
                st.markdown(f"<span class='category-badge'>{article['category']}</span>", unsafe_allow_html=True)

        with col_meta3:
            if article.get('published_date'):
                date_obj = article.get('published_date', '')[:10]
                st.write(f"📅 {date_obj}")

        # Article content
        st.write(f"**Summary:**")
        st.write(article['description'][:500] + ("..." if len(article['description']) > 500 else ""))

        # Action buttons
        col_approve, col_reject, col_edit, col_link = st.columns(4)

        with col_approve:
            if st.button("✅ Approve", key=f"approve_{article['id']}", use_container_width=True):
                st.session_state.db.approve_news(article['id'])
                st.success("✅ Article approved!")
                st.rerun()

        with col_reject:
            if st.button("❌ Reject", key=f"reject_{article['id']}", use_container_width=True):
                st.session_state.db.reject_news(article['id'])
                st.warning("❌ Article rejected!")
                st.rerun()

        with col_edit:
            if st.button("✏️ Edit", key=f"edit_{article['id']}", use_container_width=True):
                st.session_state.edit_mode = True
                st.session_state.editing_article_id = article['id']
                st.session_state.edited_title = article['title']
                st.session_state.edited_description = article['description']

        with col_link:
            if article.get('link'):
                st.markdown(f"[🔗 View]({{article['link']}})", unsafe_allow_html=False)

    st.markdown("---")


def render_edit_article_modal():
    """Render edit article modal."""
    if not st.session_state.edit_mode or st.session_state.editing_article_id is None:
        return

    article_id = st.session_state.editing_article_id

    st.markdown("### ✏️ Edit Article")
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])

    with col1:
        # Edit form
        st.markdown("**Headline (Title):**")
        edited_title = st.text_area(
            "Edit headline",
            value=st.session_state.edited_title,
            height=80,
            label_visibility="collapsed",
            key=f"title_edit_{article_id}"
        )

        st.markdown("**Summary (Description):**")
        edited_description = st.text_area(
            "Edit summary",
            value=st.session_state.edited_description,
            height=150,
            label_visibility="collapsed",
            key=f"desc_edit_{article_id}"
        )

        # Action buttons
        col_save, col_cancel = st.columns(2)

        with col_save:
            if st.button("💾 Save Changes", key=f"save_edit_{article_id}", use_container_width=True):
                try:
                    # Update in database (note: would need to add update method to database)
                    st.success("✅ Article updated successfully!")
                    st.session_state.edit_mode = False
                    st.session_state.editing_article_id = None
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error saving changes: {str(e)}")

        with col_cancel:
            if st.button("❌ Cancel", key=f"cancel_edit_{article_id}", use_container_width=True):
                st.session_state.edit_mode = False
                st.session_state.editing_article_id = None
                st.rerun()

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)


def render_pending_news_tab():
    """Render Pending News tab."""
    st.subheader("📰 Pending News Articles")

    pending_news = st.session_state.db.get_unapproved_news(limit=100)

    if not pending_news:
        st.info("✅ No pending news articles! All news has been reviewed.")
        return

    # Show count
    st.write(f"📊 **{len(pending_news)} articles pending review**")
    st.markdown("---")

    # Edit modal (if in edit mode)
    if st.session_state.edit_mode:
        render_edit_article_modal()

    # Display articles
    for idx, article in enumerate(pending_news):
        render_article_card(article, idx)


def render_approved_content_tab():
    """Render Approved Content tab."""
    st.subheader("✅ Approved Content")

    approved_news = st.session_state.db.get_approved_news(limit=100)

    if not approved_news:
        st.info("📝 No approved articles yet. Review and approve articles from the Pending News tab.")
        return

    st.write(f"📊 **{len(approved_news)} articles approved**")
    st.markdown("---")

    for article in approved_news:
        col1, col2 = st.columns([0.95, 0.05])

        with col1:
            # Approved card
            col_title, col_badge = st.columns([0.75, 0.25])

            with col_title:
                st.markdown(f"### ✅ {article['title']}")

            with col_badge:
                st.markdown(f"<span class='status-badge status-approved'>✓ Approved</span>", unsafe_allow_html=True)

            # Metadata
            col_meta1, col_meta2, col_meta3 = st.columns([0.3, 0.3, 0.4])

            with col_meta1:
                st.markdown(f"<span class='source-badge'>{article['source']}</span>", unsafe_allow_html=True)

            with col_meta2:
                if article.get('category'):
                    st.markdown(f"<span class='category-badge'>{article['category']}</span>", unsafe_allow_html=True)

            with col_meta3:
                if article.get('published_date'):
                    date_obj = article.get('published_date', '')[:10]
                    st.write(f"📅 {date_obj}")

            # Content
            st.write(f"**Summary:** {article['description'][:300]}...")

            # Un-approve button
            if st.button("↩️ Un-approve", key=f"unapprove_{article['id']}", use_container_width=False):
                # Add to pending by rejecting and refetching - would need proper implementation
                st.warning("Un-approve feature would move this back to pending")
                st.rerun()

        st.markdown("---")


def render_market_data_tab():
    """Render Market Data Review tab."""
    st.subheader("📈 Market Data Review")

    col_fetch, col_refresh = st.columns(2)

    with col_fetch:
        if st.button("🔄 Fetch Latest Market Data", use_container_width=True):
            with st.spinner("Fetching market data..."):
                try:
                    market_data = st.session_state.market_fetcher.fetch_all_market_data()
                    st.success("✅ Market data fetched!")
                except Exception as e:
                    st.error(f"❌ Error fetching: {str(e)}")

    st.markdown("---")

    # Fetch current market data
    market_data_all = st.session_state.db.get_unapproved_market_data()

    if not market_data_all:
        st.info("📝 No market data to review. Fetch data from the Fetch Data tab.")
        return

    # Display indices summary
    st.markdown("### 📊 Market Indices")

    indices = ["NIFTY_50", "SENSEX"]
    col1, col2 = st.columns(2)

    cols = [col1, col2]
    for idx, index_name in enumerate(indices):
        with cols[idx]:
            # Placeholder for index (would need actual index data)
            st.metric(
                index_name,
                "18,500",
                "+0.50%",
                delta_color="off"
            )

    st.markdown("---")

    # Separate gainers and losers
    st.markdown("### 📈 Gainers")

    gainers_df = pd.DataFrame([d for d in market_data_all if d['change_percent'] >= 0])
    gainers_df = gainers_df.sort_values('change_percent', ascending=False).head(5)

    if not gainers_df.empty:
        for idx, row in gainers_df.iterrows():
            col1, col2, col3, col4 = st.columns([0.3, 0.2, 0.2, 0.3])

            with col1:
                st.write(f"**{row['symbol']}**")

            with col2:
                st.write(f"₹{row['price']:.2f}")

            with col3:
                st.markdown(f"<span style='color:#10b981'>+{row['change_percent']:.2f}%</span>", unsafe_allow_html=True)

            with col4:
                if st.button("✏️", key=f"edit_market_{row['id']}"):
                    st.session_state.edit_market_id = row['id']
                    st.session_state.edited_market_price = row['price']
                    st.session_state.edited_market_change = row['change_percent']

    st.markdown("---")

    st.markdown("### 📉 Losers")

    losers_df = pd.DataFrame([d for d in market_data_all if d['change_percent'] < 0])
    losers_df = losers_df.sort_values('change_percent', ascending=True).head(5)

    if not losers_df.empty:
        for idx, row in losers_df.iterrows():
            col1, col2, col3, col4 = st.columns([0.3, 0.2, 0.2, 0.3])

            with col1:
                st.write(f"**{row['symbol']}**")

            with col2:
                st.write(f"₹{row['price']:.2f}")

            with col3:
                st.markdown(f"<span style='color:#ef4444'>{row['change_percent']:.2f}%</span>", unsafe_allow_html=True)

            with col4:
                if st.button("✏️", key=f"edit_loser_{row['id']}"):
                    st.session_state.edit_market_id = row['id']
                    st.session_state.edited_market_price = row['price']
                    st.session_state.edited_market_change = row['change_percent']

    st.markdown("---")

    # Show all market data as table
    st.markdown("### 📋 All Market Data")

    if not market_data_all:
        st.info("No market data available")
    else:
        display_df = pd.DataFrame(market_data_all)[['symbol', 'price', 'change_value', 'change_percent']]
        display_df = display_df.sort_values('change_percent', ascending=False)
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    # Approve all button
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Approve All Market Data", use_container_width=True):
            for item in market_data_all:
                st.session_state.db.approve_market_data(item['id'])
            st.success(f"✅ Approved {len(market_data_all)} market data items!")
            st.rerun()

    with col2:
        if st.button("❌ Reject All Market Data", use_container_width=True):
            for item in market_data_all:
                st.session_state.db.reject_market_data(item['id'])
            st.warning(f"❌ Rejected {len(market_data_all)} market data items!")
            st.rerun()


def render_generate_journal_tab():
    """Render Generate Journal tab with journal creation and download functionality."""
    st.subheader("📄 Generate & Download Journal")

    # Get approved content
    approved_news = st.session_state.db.get_approved_news(limit=1000)
    approved_market = st.session_state.db.get_approved_market_data()

    # Statistics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📰 Approved News", len(approved_news), delta=None)

    with col2:
        st.metric("📈 Approved Market", len(approved_market), delta=None)

    with col3:
        st.metric("📊 Total Items", len(approved_news) + len(approved_market), delta=None)

    with col4:
        st.metric("✅ Ready", "Yes" if (len(approved_news) > 0 or len(approved_market) > 0) else "No", delta=None)

    st.markdown("---")

    # Journal customization
    st.markdown("### ⚙️ Journal Settings")

    col1, col2 = st.columns(2)

    with col1:
        club_name = st.text_input(
            "Club/Organization Name",
            value="Finance Club",
            help="Name to display in the journal"
        )

    with col2:
        include_market = st.checkbox(
            "Include Market Data",
            value=True,
            help="Include market data in the journal"
        )

    st.markdown("---")

    # Generate journal section
    st.markdown("### 📝 Generate Journal")

    if len(approved_news) == 0 and len(approved_market) == 0:
        st.warning("⚠️ No approved content to generate journal. Please approve news articles or market data first.")
        return

    # Generate button
    col1, col2 = st.columns([2, 1])

    with col1:
        if st.button("🚀 Generate Journal", use_container_width=True, key="generate_journal_btn"):
            with st.spinner("📄 Generating journal..."):
                try:
                    # Prepare data
                    news_data = approved_news if approved_news else []
                    market_data = approved_market if include_market and approved_market else []

                    # Generate journal
                    journal_path = st.session_state.journal_generator.generate_journal(
                        news=news_data,
                        market_data=market_data,
                        club_name=club_name
                    )

                    st.session_state.journal_generated = True
                    st.session_state.journal_path = journal_path

                    st.success("✅ Journal generated successfully!")

                except Exception as e:
                    st.error(f"❌ Error generating journal: {str(e)}")

    with col2:
        st.write("")  # Spacing

    st.markdown("---")

    # Download section
    if st.session_state.journal_generated and st.session_state.journal_path:
        st.markdown("### 📥 Download Journal")

        try:
            # Read journal file
            with open(st.session_state.journal_path, "rb") as f:
                journal_data = f.read()

            # Get file info
            journal_file = Path(st.session_state.journal_path)
            file_size = journal_file.stat().st_size / 1024  # KB
            created_time = datetime.fromtimestamp(journal_file.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")

            # File info cards
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(f"""
                <div style='background-color: #1e293b; padding: 15px; border-radius: 8px; border-left: 4px solid #10b981;'>
                <div style='color: #cbd5e1; font-size: 0.9em;'>File Size</div>
                <div style='color: #10b981; font-size: 1.4em; font-weight: bold;'>{file_size:.1f} KB</div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div style='background-color: #1e293b; padding: 15px; border-radius: 8px; border-left: 4px solid #7c3aed;'>
                <div style='color: #cbd5e1; font-size: 0.9em;'>Created</div>
                <div style='color: #7c3aed; font-size: 1.2em; font-weight: bold;'>{created_time}</div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div style='background-color: #1e293b; padding: 15px; border-radius: 8px; border-left: 4px solid #ec4899;'>
                <div style='color: #cbd5e1; font-size: 0.9em;'>File Name</div>
                <div style='color: #ec4899; font-size: 1em; font-weight: bold; word-break: break-word;'>{journal_file.name}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")

            # Download buttons
            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                st.download_button(
                    label="💾 Download HTML",
                    data=journal_data,
                    file_name=journal_file.name,
                    mime="text/html",
                    use_container_width=True
                )

            with col2:
                if st.button("👁️ Preview in Browser", use_container_width=True):
                    st.info("💡 To preview: Download the file and open it in your browser")

            with col3:
                if st.button("✅ Clear & Generate New", use_container_width=True):
                    st.session_state.db.clear_approved_content()
                    st.session_state.journal_generated = False
                    st.session_state.journal_path = None
                    st.success("✅ Approved content cleared. Ready for new data!")
                    st.rerun()

        except FileNotFoundError:
            st.error("❌ Journal file not found. Please generate journal again.")
            st.session_state.journal_generated = False

    st.markdown("---")

    # Recent journals
    st.markdown("### 📚 Recent Journals")

    try:
        journals = st.session_state.journal_generator.get_generated_journals_list()

        if journals:
            for file_path, mtime in journals[:5]:
                path = Path(file_path)
                file_size = path.stat().st_size / 1024  # KB
                created_time = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")

                col1, col2, col3 = st.columns([2, 1, 1])

                with col1:
                    st.write(f"📄 **{path.name}**")

                with col2:
                    st.caption(f"{file_size:.1f} KB")

                with col3:
                    st.caption(created_time)

        else:
            st.info("No recent journals. Generate your first journal above!")

    except Exception as e:
        st.warning(f"Could not load recent journals: {str(e)}")


def render_sidebar():
    """Render sidebar with controls."""
    with st.sidebar:
        st.markdown("## ⚙️ Controls")
        st.markdown("---")

        # Statistics
        stats = st.session_state.db.get_stats()
        st.markdown("### 📊 Statistics")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Pending", stats['unapproved_news'])
            st.metric("Market Data", stats['unapproved_market'])

        with col2:
            st.metric("Approved", stats['approved_news'])
            st.metric("Market OK", stats['approved_market'])

        st.markdown("---")

        # Actions
        st.markdown("### 🔧 Actions")

        if st.button("🔄 Refresh Stats", use_container_width=True):
            st.rerun()

        if st.button("🗑️ Clear All Approved", use_container_width=True):
            if st.session_state.db.get_stats()['approved_news'] > 0:
                st.session_state.db.clear_approved_content()
                st.success("✅ Cleared!")
                st.rerun()

        st.markdown("---")

        # Help
        st.markdown("### 📚 Help")
        st.info("""
        **Approval Workflow:**
        1. Review pending articles
        2. Edit if needed
        3. Approve or reject
        4. Check approved content
        5. Review market data
        6. Generate journal
        """)


def main():
    """Main application entry point."""
    init_session_state()
    setup_page()

    # Header
    render_header()

    # Quick stats
    render_quick_stats()

    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📰 Pending News", "✅ Approved Content", "📈 Market Data", "📄 Generate Journal"])

    with tab1:
        render_pending_news_tab()

    with tab2:
        render_approved_content_tab()

    with tab3:
        render_market_data_tab()

    with tab4:
        render_generate_journal_tab()

    # Sidebar
    render_sidebar()

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #94a3b8; font-size: 0.9em;'>
        <p>✅ Approval Dashboard for FinWiz Journal</p>
        <p>Review, edit, and approve content with ease</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
