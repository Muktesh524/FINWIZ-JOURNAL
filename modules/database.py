"""SQLite database operations for FinWiz Journal."""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

DB_PATH = Path(__file__).parent.parent / "data" / "finwiz.db"


class JournalDB:
    """Handle all database operations for FinWiz Journal."""

    def __init__(self, db_path: str = str(DB_PATH)):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize database tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # News articles table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS news_articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    link TEXT UNIQUE,
                    source TEXT,
                    published_date TIMESTAMP,
                    fetched_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    approved INTEGER DEFAULT 0,
                    category TEXT,
                    content_json TEXT
                )
            """)

            # Market data table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS market_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    price REAL,
                    change_percent REAL,
                    change_value REAL,
                    fetched_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    approved INTEGER DEFAULT 0,
                    data_json TEXT
                )
            """)

            # Generated journals table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS generated_journals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    file_path TEXT,
                    news_count INTEGER,
                    market_data_count INTEGER,
                    metadata_json TEXT
                )
            """)

            conn.commit()

    def add_news(self, title: str, description: str, link: str, source: str,
                 published_date: Optional[str] = None, category: str = "General") -> tuple:
        """Add a news article. Returns (id, success, message)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO news_articles (title, description, link, source, published_date, category)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (title, description, link, source, published_date, category))
                conn.commit()
                return cursor.lastrowid, True, "Article added successfully"
            except sqlite3.IntegrityError:
                return -1, False, "Article already exists (duplicate link)"
            except Exception as e:
                return -1, False, f"Error: {str(e)}"

    def add_market_data(self, symbol: str, price: float, change_percent: float,
                       change_value: float, data_type: str = "stock", data_json: Optional[str] = None) -> tuple:
        """Add market data. Returns (id, success, message)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO market_data (symbol, price, change_percent, change_value, data_json)
                    VALUES (?, ?, ?, ?, ?)
                """, (symbol, price, change_percent, change_value, data_json))
                conn.commit()
                return cursor.lastrowid, True, "Market data added successfully"
            except Exception as e:
                return -1, False, f"Error: {str(e)}"

    def add_multiple_news(self, articles: List[Dict]) -> Dict[str, Any]:
        """Add multiple news articles. Returns stats dict."""
        stats = {"added": 0, "duplicates": 0, "errors": 0}

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for article in articles:
                try:
                    cursor.execute("""
                        INSERT INTO news_articles (title, description, link, source, published_date, category)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        article.get("title", ""),
                        article.get("description", ""),
                        article.get("link", ""),
                        article.get("source", ""),
                        article.get("published_date"),
                        article.get("category", "General"),
                    ))
                    stats["added"] += 1
                except sqlite3.IntegrityError:
                    stats["duplicates"] += 1
                except Exception as e:
                    stats["errors"] += 1

            conn.commit()

        return stats

    def add_multiple_market_data(self, market_data_list: List[Dict]) -> Dict[str, Any]:
        """Add multiple market data entries. Returns stats dict."""
        stats = {"added": 0, "errors": 0}

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for data in market_data_list:
                try:
                    cursor.execute("""
                        INSERT INTO market_data (symbol, price, change_percent, change_value, data_json)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        data.get("symbol") or data.get("display_name"),
                        data.get("price", 0),
                        data.get("change_percent", 0),
                        data.get("change_value", 0),
                        json.dumps(data),
                    ))
                    stats["added"] += 1
                except Exception as e:
                    stats["errors"] += 1

            conn.commit()

        return stats

    def get_unapproved_news(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get all unapproved news articles."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM news_articles
                WHERE approved = 0
                ORDER BY fetched_date DESC
                LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]

    def get_approved_news(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get all approved news articles."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM news_articles
                WHERE approved = 1
                ORDER BY published_date DESC
                LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]

    def get_unapproved_market_data(self) -> List[Dict[str, Any]]:
        """Get all unapproved market data."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM market_data
                WHERE approved = 0
                ORDER BY fetched_date DESC
            """)
            return [dict(row) for row in cursor.fetchall()]

    def get_approved_market_data(self) -> List[Dict[str, Any]]:
        """Get all approved market data."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM market_data
                WHERE approved = 1
                ORDER BY fetched_date DESC
            """)
            return [dict(row) for row in cursor.fetchall()]

    def approve_news(self, news_id: int) -> bool:
        """Approve a news article."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE news_articles SET approved = 1 WHERE id = ?", (news_id,))
            conn.commit()
            return cursor.rowcount > 0

    def approve_market_data(self, data_id: int) -> bool:
        """Approve market data."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE market_data SET approved = 1 WHERE id = ?", (data_id,))
            conn.commit()
            return cursor.rowcount > 0

    def reject_news(self, news_id: int) -> bool:
        """Delete a news article."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM news_articles WHERE id = ?", (news_id,))
            conn.commit()
            return cursor.rowcount > 0

    def reject_market_data(self, data_id: int) -> bool:
        """Delete market data."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM market_data WHERE id = ?", (data_id,))
            conn.commit()
            return cursor.rowcount > 0

    def update_news(self, news_id: int, title: Optional[str] = None,
                   description: Optional[str] = None) -> bool:
        """Update a news article's title and/or description."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            updates = []
            params = []

            if title is not None:
                updates.append("title = ?")
                params.append(title)

            if description is not None:
                updates.append("description = ?")
                params.append(description)

            if not updates:
                return False

            params.append(news_id)
            query = f"UPDATE news_articles SET {', '.join(updates)} WHERE id = ?"

            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0

    def update_market_data(self, data_id: int, price: Optional[float] = None,
                          change_percent: Optional[float] = None,
                          change_value: Optional[float] = None) -> bool:
        """Update market data price and changes."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            updates = []
            params = []

            if price is not None:
                updates.append("price = ?")
                params.append(price)

            if change_percent is not None:
                updates.append("change_percent = ?")
                params.append(change_percent)

            if change_value is not None:
                updates.append("change_value = ?")
                params.append(change_value)

            if not updates:
                return False

            params.append(data_id)
            query = f"UPDATE market_data SET {', '.join(updates)} WHERE id = ?"

            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0

    def get_stats(self) -> Dict[str, int]:
        """Get database statistics."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM news_articles WHERE approved = 0")
            unapproved_news = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM news_articles WHERE approved = 1")
            approved_news = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM market_data WHERE approved = 0")
            unapproved_market = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM market_data WHERE approved = 1")
            approved_market = cursor.fetchone()[0]

            return {
                "unapproved_news": unapproved_news,
                "approved_news": approved_news,
                "unapproved_market": unapproved_market,
                "approved_market": approved_market,
            }

    def clear_approved_content(self):
        """Clear all approved content after journal generation."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM news_articles WHERE approved = 1")
            cursor.execute("DELETE FROM market_data WHERE approved = 1")
            conn.commit()

    def save_journal_metadata(self, file_path: str, news_count: int,
                            market_data_count: int, metadata: Optional[Dict] = None):
        """Save journal generation metadata."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            metadata_json = json.dumps(metadata or {})
            cursor.execute("""
                INSERT INTO generated_journals (file_path, news_count, market_data_count, metadata_json)
                VALUES (?, ?, ?, ?)
            """, (file_path, news_count, market_data_count, metadata_json))
            conn.commit()
