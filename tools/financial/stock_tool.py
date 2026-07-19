from langchain_core.tools import tool
import yfinance as yf
from core.logger import logger

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

        if not info or "regularMarketPrice" not in info and "currentPrice" not in info:
            logger.warning(f"Limited data found for ticker {ticker}")

        return {
            "ticker": ticker.upper(),
            "company_name": info.get("longName") or info.get("shortName") or ticker.upper(),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "current_price": info.get("currentPrice") or info.get("regularMarketPrice") or info.get("previousClose"),
            "market_cap": info.get("marketCap", "N/A"),
            "pe_ratio": info.get("trailingPE") or info.get("forwardPE") or "N/A",
            "eps": info.get("trailingEps") or "N/A",
            "fifty_two_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "fifty_two_week_low": info.get("fiftyTwoWeekLow", "N/A"),
        }
    except Exception as e:
        logger.error(f"Error fetching stock data for {ticker}: {e}")
        return {
            "ticker": ticker.upper(),
            "error": f"Failed to retrieve stock data: {str(e)}"
        }
