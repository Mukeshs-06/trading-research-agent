import os
import json
import datetime
from typing import Dict, Any, List
from core.logger import logger

REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

LATEST_METRICS_FILE = os.path.join(REPORTS_DIR, "latest_metrics.json")

def archive_daily_report(report_markdown: str, date_str: str = None) -> str:
    """
    Saves the generated daily report to reports/YYYY-MM-DD.md.
    """
    if not date_str:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")

    filepath = os.path.join(REPORTS_DIR, f"{date_str}.md")
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(report_markdown)
        logger.info(f"Successfully archived daily report to: {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"Error archiving report to {filepath}: {e}")
        return ""

def load_previous_metrics() -> Dict[str, Any]:
    """
    Loads previous day's metrics from reports/latest_metrics.json if present.
    """
    if os.path.exists(LATEST_METRICS_FILE):
        try:
            with open(LATEST_METRICS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load previous metrics: {e}")
    return {}

def save_current_metrics(metrics: Dict[str, Any]) -> None:
    """
    Saves current day's metrics to reports/latest_metrics.json for historical diffing.
    """
    try:
        with open(LATEST_METRICS_FILE, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2)
        logger.info("Saved latest metrics to JSON cache.")
    except Exception as e:
        logger.error(f"Failed to save current metrics: {e}")

def detect_smart_alerts(current_state: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Analyzes current technical and fundamental state to detect significant market alerts:
    - RSI Overbought (>70) or Oversold (<30)
    - Trend Reversals vs Previous Cached State
    - Support / Resistance proximity
    """
    alerts = []
    prev_metrics = load_previous_metrics()

    tech_data = current_state.get("technical_data", {})
    stock_data = current_state.get("stock_data", {})

    for company, tech in tech_data.items():
        if isinstance(tech, dict) and "error" not in tech:
            rsi = tech.get("RSI", 50)
            trend = tech.get("Trend", "Neutral")
            current_price = tech.get("current_price", 0)
            support = tech.get("Support_6M", 0)
            resistance = tech.get("Resistance_6M", 0)

            # RSI Alert
            if rsi >= 70:
                alerts.append({
                    "company": company,
                    "type": "RSI_OVERBOUGHT",
                    "severity": "WARNING",
                    "message": f"RSI is {rsi} (Overbought > 70). Downside pullback risk."
                })
            elif rsi <= 30:
                alerts.append({
                    "company": company,
                    "type": "RSI_OVERSOLD",
                    "severity": "OPPORTUNITY",
                    "message": f"RSI is {rsi} (Oversold < 30). Potential reversal bounce."
                })

            # Trend Shift Detection
            prev_trend = prev_metrics.get(company, {}).get("Trend")
            if prev_trend and prev_trend != trend:
                alerts.append({
                    "company": company,
                    "type": "TREND_SHIFT",
                    "severity": "HIGH",
                    "message": f"Trend shifted from '{prev_trend}' to '{trend}'."
                })

            # Near Support or Resistance (within 2%)
            if support > 0 and abs(current_price - support) / support < 0.02:
                alerts.append({
                    "company": company,
                    "type": "NEAR_SUPPORT",
                    "severity": "HIGH",
                    "message": f"Price (${current_price}) is testing 6M Support (${support})."
                })
            elif resistance > 0 and abs(current_price - resistance) / resistance < 0.02:
                alerts.append({
                    "company": company,
                    "type": "NEAR_RESISTANCE",
                    "severity": "HIGH",
                    "message": f"Price (${current_price}) is testing 6M Resistance (${resistance})."
                })

    # Save current metrics state for future diffing
    cache_payload = {}
    for company, tech in tech_data.items():
        if isinstance(tech, dict):
            cache_payload[company] = {
                "current_price": tech.get("current_price"),
                "RSI": tech.get("RSI"),
                "Trend": tech.get("Trend"),
                "timestamp": datetime.datetime.now().isoformat(),
            }
    if cache_payload:
        save_current_metrics(cache_payload)

    return alerts
