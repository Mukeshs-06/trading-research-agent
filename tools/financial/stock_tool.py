from langchain_core.tools import tool
import yfinance as yf
from core.logger import logger

def _format_market_cap(market_cap: float) -> str:
    if not market_cap or not isinstance(market_cap, (int, float)):
        return "N/A"
    if market_cap >= 1e12:
        return f"${market_cap / 1e12:.2f}T"
    elif market_cap >= 1e9:
        return f"${market_cap / 1e9:.2f}B"
    elif market_cap >= 1e6:
        return f"${market_cap / 1e6:.2f}M"
    return f"${market_cap:,.0f}"

@tool
def get_stock_data(ticker: str) -> dict:
    """
    Retrieve stock market fundamental information from Yahoo Finance.

    Returns:
    - Company name, current price, market cap, sector, industry, PE ratio, EPS, 52-week high/low.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info or {}

        if not info or ("regularMarketPrice" not in info and "currentPrice" not in info):
            logger.warning(f"Limited data found for ticker {ticker}")

        raw_cap = info.get("marketCap")
        formatted_cap = _format_market_cap(raw_cap) if raw_cap else "N/A"

        pe = info.get("trailingPE") or info.get("forwardPE")

        return {
            "ticker": ticker.upper(),
            "company_name": info.get("longName") or info.get("shortName") or ticker.upper(),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "current_price": info.get("currentPrice") or info.get("regularMarketPrice") or info.get("previousClose"),
            "market_cap": formatted_cap,
            "pe_ratio": round(float(pe), 2) if pe else "N/A",
            "eps": round(float(info.get("trailingEps")), 2) if info.get("trailingEps") else "N/A",
            "fifty_two_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "fifty_two_week_low": info.get("fiftyTwoWeekLow", "N/A"),
        }
    except Exception as e:
        logger.error(f"Error fetching stock data for {ticker}: {e}")
        return {
            "ticker": ticker.upper(),
            "error": f"Failed to retrieve stock data: {str(e)}"
        }
