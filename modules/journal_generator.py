"""Generate HTML journal from approved content using Jinja2."""

from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
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

    def generate_journal(self, news: List[Dict], market_data: List[Dict],
                        output_path: Optional[Path] = None) -> str:
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
            "club_name": "Finance Club",
        }

        # Render template
        template = self.env.get_template("journal.html")
        html_content = template.render(**context)

        # Write to file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

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
