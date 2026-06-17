"""Fetch market data using yfinance."""

import yfinance as yf
import json
from typing import List, Dict, Optional
from datetime import datetime


class MarketDataFetcher:
    """Fetch market data from Yahoo Finance."""

    # Default Indian stock market symbols
    DEFAULT_SYMBOLS = {
        "NIFTY_50": "^NSEI",
        "SENSEX": "^BSESN",
        "BANK_NIFTY": "^NSEBANK",
        "RELIANCE": "RELIANCE.NS",
        "TCS": "TCS.NS",
        "INFY": "INFY.NS",
        "ICICI_BANK": "ICICIBANK.NS",
        "HDFC_BANK": "HDFCBANK.NS",
    }

    def __init__(self, symbols: Optional[Dict[str, str]] = None):
        """Initialize with custom symbols or use defaults."""
        self.symbols = symbols or self.DEFAULT_SYMBOLS

    def fetch_market_data(self) -> List[Dict]:
        """Fetch current market data for all symbols."""
        market_data = []

        for name, symbol in self.symbols.items():
            try:
                data = self.fetch_single_symbol(symbol)
                if data:
                    data["display_name"] = name
                    market_data.append(data)
            except Exception as e:
                print(f"Error fetching {symbol}: {str(e)}")

        return market_data

    def fetch_single_symbol(self, symbol: str) -> Optional[Dict]:
        """Fetch data for a single symbol."""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d")

            if hist.empty:
                return None

            current_price = hist["Close"].iloc[-1]

            # Fetch previous close for comparison
            hist_2d = ticker.history(period="2d")
            if len(hist_2d) >= 2:
                previous_price = hist_2d["Close"].iloc[-2]
                change_value = current_price - previous_price
                change_percent = (change_value / previous_price * 100) if previous_price != 0 else 0
            else:
                previous_price = current_price
                change_value = 0
                change_percent = 0

            return {
                "symbol": symbol,
                "price": round(current_price, 2),
                "change_value": round(change_value, 2),
                "change_percent": round(change_percent, 2),
                "currency": "INR",
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            print(f"Error fetching {symbol}: {str(e)}")
            return None

    def get_nifty_movers(self, top_n: int = 5) -> Dict[str, List[Dict]]:
        """Get top gainers and losers for the day."""
        movers = {"gainers": [], "losers": []}

        symbols_to_check = [
            ("RELIANCE", "RELIANCE.NS"),
            ("TCS", "TCS.NS"),
            ("INFY", "INFY.NS"),
            ("ICICI_BANK", "ICICIBANK.NS"),
            ("HDFC_BANK", "HDFCBANK.NS"),
            ("WIPRO", "WIPRO.NS"),
            ("AXIS_BANK", "AXISBANK.NS"),
            ("LT", "LT.NS"),
            ("MARUTI", "MARUTI.NS"),
            ("BAJAJ_AUTO", "BAJAJAUT0.NS"),
        ]

        data = []
        for name, symbol in symbols_to_check:
            try:
                stock_data = self.fetch_single_symbol(symbol)
                if stock_data:
                    stock_data["display_name"] = name
                    data.append(stock_data)
            except:
                pass

        # Sort by change percent
        data.sort(key=lambda x: x["change_percent"], reverse=True)

        # Top gainers and losers
        movers["gainers"] = data[:top_n]
        movers["losers"] = data[-top_n:][::-1]  # Reverse to show worst first

        return movers

    def get_sector_performance(self) -> Dict[str, float]:
        """Get sector-wise performance data."""
        sectors = {
            "IT": "^CNXIT",
            "Banking": "^CNXBANK",
            "Auto": "^CNXAUTO",
            "Pharma": "^CNXPHARMA",
            "FMCG": "^CNXFMCG",
        }

        performance = {}
        for sector_name, sector_index in sectors.items():
            try:
                ticker = yf.Ticker(sector_index)
                hist = ticker.history(period="2d")

                if not hist.empty and len(hist) >= 2:
                    current = hist["Close"].iloc[-1]
                    previous = hist["Close"].iloc[-2]
                    change_percent = ((current - previous) / previous * 100) if previous != 0 else 0
                    performance[sector_name] = round(change_percent, 2)
            except:
                pass

        return performance


if __name__ == "__main__":
    fetcher = MarketDataFetcher()
    data = fetcher.fetch_market_data()
    print("Market Data:")
    for item in data[:3]:
        print(f"{item['display_name']}: {item['price']} ({item['change_percent']}%)")

    print("\nNifty Movers:")
    movers = fetcher.get_nifty_movers()
    print("Top Gainers:", movers["gainers"][:2])
    print("Top Losers:", movers["losers"][:2])
