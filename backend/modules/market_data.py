"""Fetch market data using yfinance - Focused on Nifty 50."""

import yfinance as yf
from typing import List, Dict, Optional, Tuple
from datetime import datetime


class MarketDataFetcher:
    """Fetch market data from Yahoo Finance (India NSE)."""

    # Nifty 50 constituent stocks (top companies)
    NIFTY_50_SYMBOLS = [
        ("RELIANCE", "RELIANCE.NS"),
        ("TCS", "TCS.NS"),
        ("INFY", "INFY.NS"),
        ("HDFC Bank", "HDFCBANK.NS"),
        ("ICICI Bank", "ICICIBANK.NS"),
        ("Axis Bank", "AXISBANK.NS"),
        ("Kotak Bank", "KOTAKBANK.NS"),
        ("HDFC", "HDFC.NS"),
        ("Wipro", "WIPRO.NS"),
        ("HCL Tech", "HCLTECH.NS"),
        ("LT", "LT.NS"),
        ("Maruti", "MARUTI.NS"),
        ("Bharti Airtel", "BHARTIARTL.NS"),
        ("ITC", "ITC.NS"),
        ("NTPC", "NTPC.NS"),
        ("Power Grid", "POWERGRID.NS"),
        ("SBI", "SBIN.NS"),
        ("Sun Pharma", "SUNPHARMA.NS"),
        ("Bajaj Auto", "BAJAJAUT0.NS"),
        ("Nestlé India", "NESTLEIND.NS"),
    ]

    def __init__(self):
        """Initialize market data fetcher."""
        self.nifty_index = "^NSEI"
        self.sensex_index = "^BSESN"

    def fetch_nifty_50_movers(self, top_n: int = 5) -> Tuple[List[Dict], List[Dict], Dict]:
        """
        Fetch Nifty 50 stocks and return top gainers and losers.
        Returns (gainers, losers, stats)
        """
        all_data = []
        stats = {"fetched": 0, "errors": 0}

        for display_name, symbol in self.NIFTY_50_SYMBOLS:
            try:
                stock_data = self._fetch_single_stock(symbol, display_name)
                if stock_data:
                    all_data.append(stock_data)
                    stats["fetched"] += 1
            except Exception as e:
                stats["errors"] += 1
                print(f"Error fetching {symbol}: {str(e)}")

        # Sort by change percent
        all_data.sort(key=lambda x: x["change_percent"], reverse=True)

        # Top gainers and losers
        gainers = all_data[:top_n]
        losers = all_data[-top_n:][::-1]  # Reverse to show worst first

        return gainers, losers, stats

    def _fetch_single_stock(self, symbol: str, display_name: str) -> Optional[Dict]:
        """Fetch current price data for a single stock."""
        try:
            ticker = yf.Ticker(symbol)

            # Get 2 days of history for previous close
            hist = ticker.history(period="5d")

            if hist.empty or len(hist) < 1:
                return None

            current_price = hist["Close"].iloc[-1]

            # Get previous close (yesterday)
            if len(hist) >= 2:
                previous_price = hist["Close"].iloc[-2]
            else:
                previous_price = current_price

            change_value = current_price - previous_price
            change_percent = (change_value / previous_price * 100) if previous_price != 0 else 0

            return {
                "symbol": symbol,
                "display_name": display_name,
                "price": round(float(current_price), 2),
                "change_value": round(float(change_value), 2),
                "change_percent": round(float(change_percent), 2),
                "currency": "INR",
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            print(f"Error fetching {symbol}: {str(e)}")
            return None

    def fetch_index_data(self) -> Dict[str, Dict]:
        """Fetch Nifty 50 and Sensex index data."""
        indices = {}

        # Fetch Nifty 50
        try:
            nifty_data = self._fetch_index(self.nifty_index, "Nifty 50")
            if nifty_data:
                indices["nifty_50"] = nifty_data
        except Exception as e:
            print(f"Error fetching Nifty 50: {str(e)}")

        # Fetch Sensex
        try:
            sensex_data = self._fetch_index(self.sensex_index, "Sensex")
            if sensex_data:
                indices["sensex"] = sensex_data
        except Exception as e:
            print(f"Error fetching Sensex: {str(e)}")

        return indices

    def _fetch_index(self, symbol: str, name: str) -> Optional[Dict]:
        """Fetch index data."""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="5d")

            if hist.empty or len(hist) < 1:
                return None

            current = hist["Close"].iloc[-1]
            previous = hist["Close"].iloc[-2] if len(hist) >= 2 else current

            change = current - previous
            change_percent = (change / previous * 100) if previous != 0 else 0

            return {
                "name": name,
                "symbol": symbol,
                "value": round(float(current), 2),
                "change": round(float(change), 2),
                "change_percent": round(float(change_percent), 2),
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            print(f"Error fetching index {symbol}: {str(e)}")
            return None

    def fetch_all_market_data(self) -> Dict:
        """Fetch all market data (indices + movers)."""
        gainers, losers, stats = self.fetch_nifty_50_movers(top_n=5)
        indices = self.fetch_index_data()

        return {
            "indices": indices,
            "gainers": gainers,
            "losers": losers,
            "stats": stats,
            "timestamp": datetime.now().isoformat(),
        }


if __name__ == "__main__":
    fetcher = MarketDataFetcher()

    print("🔄 Fetching Market Data...\n")

    # Fetch indices
    print("📊 Market Indices:")
    indices = fetcher.fetch_index_data()
    for key, data in indices.items():
        if data:
            print(f"  {data['name']}: {data['value']} ({data['change_percent']:+.2f}%)")

    # Fetch movers
    print("\n📈 Top 5 Gainers:")
    gainers, losers, stats = fetcher.fetch_nifty_50_movers()
    for i, stock in enumerate(gainers, 1):
        print(f"  {i}. {stock['display_name']}: ₹{stock['price']} ({stock['change_percent']:+.2f}%)")

    print("\n📉 Top 5 Losers:")
    for i, stock in enumerate(losers, 1):
        print(f"  {i}. {stock['display_name']}: ₹{stock['price']} ({stock['change_percent']:+.2f}%)")

    print(f"\n✅ Fetched: {stats['fetched']} stocks, Errors: {stats['errors']}")
