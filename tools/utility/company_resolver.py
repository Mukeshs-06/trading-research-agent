from langchain_core.tools import tool
import yfinance as yf
from core.logger import logger

# Static mapping dictionary for common tickers
TICKER_MAP = {
    "apple": "AAPL",
    "microsoft": "MSFT",
    "google": "GOOGL",
    "alphabet": "GOOGL",
    "amazon": "AMZN",
    "meta": "META",
    "facebook": "META",
    "tesla": "TSLA",
    "nvidia": "NVDA",
    "tcs": "TCS.NS",
    "tata consultancy services": "TCS.NS",
    "infosys": "INFY",
    "reliance": "RELIANCE.NS",
    "hDFC": "HDFCBANK.NS",
}

@tool
def resolve_company(company_name: str) -> str:
    """
    Resolve a company name (e.g. Apple, Microsoft, Tesla, TCS, Reliance)
    into its valid Yahoo Finance ticker symbol (e.g. AAPL, MSFT, TSLA, TCS.NS).
    """
    cleaned = company_name.strip().lower()
    if cleaned in TICKER_MAP:
        return TICKER_MAP[cleaned]

    try:
        search = yf.Search(company_name)
        if search.quotes and len(search.quotes) > 0:
            symbol = search.quotes[0].get("symbol")
            if symbol:
                return symbol.upper()
    except Exception as e:
        logger.warning(f"Yahoo Search failed for {company_name}: {e}")

    # Default fallback to uppercase query if lookup fails
    return company_name.strip().upper()