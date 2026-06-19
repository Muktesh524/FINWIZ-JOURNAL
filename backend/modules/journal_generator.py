"""Generate HTML journal from approved content using Jinja2."""

from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import json


class JournalGenerator:
    """Generate HTML journals from approved content."""

    def __init__(self, template_dir: Optional[Path] = None):
        """Initialize Jinja2 environment."""
        if template_dir is None:
            template_dir = Path(__file__).parent.parent / "templates"

        self.template_dir = template_dir
        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape(["html", "xml"])
        )
        self.last_generated_path = None

    def generate_journal(self, news: List[Dict], market_data: List[Dict],
                        output_path: Optional[Path] = None, club_name: str = "Finance Club") -> str:
        """Generate HTML journal from news and market data."""

        if output_path is None:
            output_path = Path(__file__).parent.parent / "data" / f"journal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Prepare data for template
        context = {
            "generated_date": datetime.now().strftime("%B %d, %Y"),
            "generated_time": datetime.now().strftime("%H:%M:%S"),
            "news_articles": news,
            "market_data": market_data,
            "news_count": len(news),
            "market_count": len(market_data),
            "club_name": club_name,
        }

        # Render template
        template = self.env.get_template("journal.html")
        html_content = template.render(**context)

        # Write to file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        self.last_generated_path = str(output_path)
        return str(output_path)

    def generate_preview(self, news: List[Dict], market_data: List[Dict]) -> str:
        """Generate HTML preview without saving to file."""
        context = {
            "generated_date": datetime.now().strftime("%B %d, %Y"),
            "generated_time": datetime.now().strftime("%H:%M:%S"),
            "news_articles": news[:5],  # Preview with limited articles
            "market_data": market_data,
            "news_count": len(news),
            "market_count": len(market_data),
            "club_name": "Finance Club",
        }

        template = self.env.get_template("journal.html")
        return template.render(**context)

    def render_news_section(self, news: List[Dict]) -> str:
        """Render just the news section."""
        context = {"news_articles": news}
        template = self.env.get_template("news_section.html")
        return template.render(**context)

    def render_market_section(self, market_data: List[Dict]) -> str:
        """Render just the market data section."""
        context = {"market_data": market_data}
        template = self.env.get_template("market_section.html")
        return template.render(**context)

    def get_template_list(self) -> List[str]:
        """Get list of available templates."""
        return [f.name for f in self.template_dir.glob("*.html")]

    def generate_journal_bytes(self, news: List[Dict], market_data: List[Dict],
                              club_name: str = "Finance Club") -> bytes:
        """Generate HTML journal and return as bytes (for download)."""
        # Prepare data for template
        context = {
            "generated_date": datetime.now().strftime("%B %d, %Y"),
            "generated_time": datetime.now().strftime("%H:%M:%S"),
            "news_articles": news,
            "market_data": market_data,
            "news_count": len(news),
            "market_count": len(market_data),
            "club_name": club_name,
        }

        # Render template
        template = self.env.get_template("journal.html")
        html_content = template.render(**context)

        return html_content.encode("utf-8")

    def generate_index_page(self, stats: Dict, recent_updates: Optional[List[Dict]] = None,
                           output_path: Optional[Path] = None) -> str:
        """Generate index/dashboard page from template."""
        if output_path is None:
            output_path = Path(__file__).parent.parent / "data" / "index.html"

        output_path.parent.mkdir(parents=True, exist_ok=True)

        context = {
            "generated_date": datetime.now().strftime("%B %d, %Y"),
            "pending_news": stats.get("unapproved_news", 0),
            "approved_news": stats.get("approved_news", 0),
            "market_count": stats.get("unapproved_market", 0) + stats.get("approved_market", 0),
            "journal_count": stats.get("journal_count", 0),
            "recent_updates": recent_updates or [],
        }

        template = self.env.get_template("index.html")
        html_content = template.render(**context)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return str(output_path)

    def get_last_generated_path(self) -> Optional[str]:
        """Get the path of the last generated journal."""
        return self.last_generated_path

    def read_generated_journal(self, file_path: str) -> Optional[str]:
        """Read and return content of generated journal file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return None

    def get_generated_journals_list(self) -> List[Tuple[str, datetime]]:
        """Get list of all generated journal files with their creation dates."""
        data_dir = Path(__file__).parent.parent / "data"
        journals = []

        if not data_dir.exists():
            return journals

        for file_path in sorted(data_dir.glob("journal_*.html"), reverse=True):
            try:
                journals.append((str(file_path), file_path.stat().st_mtime))
            except (OSError, ValueError):
                continue

        return journals

    def get_journal_file_size(self, file_path: str) -> Optional[int]:
        """Get file size in bytes."""
        try:
            return Path(file_path).stat().st_size
        except FileNotFoundError:
            return None

    def get_journal_info(self, file_path: str) -> Dict:
        """Get detailed information about a generated journal file."""
        path = Path(file_path)

        if not path.exists():
            return {"error": "File not found"}

        try:
            stat = path.stat()
            return {
                "file_name": path.name,
                "file_path": str(path),
                "file_size": stat.st_size,
                "file_size_mb": round(stat.st_size / (1024 * 1024), 2),
                "created": datetime.fromtimestamp(stat.st_mtime).strftime("%B %d, %Y %H:%M:%S"),
                "created_timestamp": stat.st_mtime,
            }
        except (OSError, ValueError) as e:
            return {"error": str(e)}
