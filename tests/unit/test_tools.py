import pytest
from tools.utility.company_resolver import resolve_company
from tools.financial.stock_tool import get_stock_data
from tools.financial.technical_tool import technical_analysis
from tools.market.news_tool import get_company_news

def test_resolve_company():
    ticker = resolve_company.invoke({"company_name": "Apple"})
    assert ticker == "AAPL"

def test_get_stock_data():
    data = get_stock_data.invoke({"ticker": "AAPL"})
    assert isinstance(data, dict)
    assert data.get("ticker") == "AAPL"
    assert "current_price" in data or "error" in data

def test_technical_analysis():
    data = technical_analysis.invoke({"ticker": "AAPL"})
    assert isinstance(data, dict)
    assert data.get("ticker") == "AAPL"
    assert "RSI" in data or "error" in data

def test_get_company_news():
    news = get_company_news.invoke({"company_name": "Apple"})
    assert isinstance(news, list)
