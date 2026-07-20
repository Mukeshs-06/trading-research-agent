import pytest
from scripts.daily_report import load_watchlist_config
from memory.report_archive import detect_smart_alerts
from notifications.email_service import generate_html_email_digest, convert_markdown_to_clean_html

def test_load_watchlist_config():
    config = load_watchlist_config()
    assert isinstance(config, dict)
    assert "watchlist" in config
    assert isinstance(config["watchlist"], list)

def test_detect_smart_alerts():
    sample_state = {
        "technical_data": {
            "AAPL": {
                "current_price": 240.0,
                "RSI": 75.0,
                "Trend": "Bullish",
                "Support_6M": 200.0,
                "Resistance_6M": 242.0,
            }
        }
    }
    alerts = detect_smart_alerts(sample_state)
    assert isinstance(alerts, list)
    assert len(alerts) >= 1
    assert alerts[0]["type"] in ["RSI_OVERBOUGHT", "NEAR_RESISTANCE"]

def test_convert_markdown_to_clean_html():
    md = "# Header 1\n- Item 1\n- Item 2\n\n| Metric | AAPL |\n| --- | --- |\n| Price | 200 |"
    html = convert_markdown_to_clean_html(md)
    assert "<h1" in html
    assert "Item 1" in html
    assert "<table" in html
    assert "<th" in html
    assert "<td" in html

def test_generate_html_email_digest():
    html = generate_html_email_digest(
        report_markdown="# Daily Report\nTest content\n\n| Metric | AAPL |\n| --- | --- |\n| Price | $200 |",
        alerts=[],
        watchlist=["AAPL"],
        execution_trace=[{"step": "research", "status": "completed", "duration_seconds": 1.2, "tools_called": ["get_stock_data"]}]
    )
    assert "Autonomous AI Market Intelligence" in html
    assert "AAPL" in html
    assert "<table" in html
