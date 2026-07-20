import os
import sys
import yaml
import argparse
import datetime

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from graph.workflow import graph
from core.logger import logger
from memory.report_archive import archive_daily_report, detect_smart_alerts
from notifications.email_service import generate_html_email_digest, send_email_digest

WATCHLIST_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "watchlist.yaml")

def load_watchlist_config() -> dict:
    """
    Loads watchlist tickers and configuration settings from config/watchlist.yaml.
    """
    default_config = {
        "watchlist": ["AAPL", "NVDA", "MSFT", "TSLA"],
        "settings": {"smart_alert_only": False, "email_recipient": None}
    }

    if os.path.exists(WATCHLIST_PATH):
        try:
            with open(WATCHLIST_PATH, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if data and "watchlist" in data:
                    return data
        except Exception as e:
            logger.warning(f"Error loading {WATCHLIST_PATH}: {e}. Falling back to default.")

    return default_config

def main():
    parser = argparse.ArgumentParser(description="Autonomous Daily AI Market Intelligence Script")
    parser.add_argument("--dry-run", action="store_true", help="Run workflow and archival without sending email digest")
    args = parser.parse_args()

    print("=" * 70)
    print("   AUTONOMOUS AI MARKET INTELLIGENCE — DAILY RUNNER")
    print("=" * 70)

    config = load_watchlist_config()
    watchlist = config.get("watchlist", ["AAPL", "NVDA", "MSFT"])
    settings = config.get("settings", {})

    query = f"Provide a complete market intelligence report covering fundamental analysis, technical indicators, and news sentiment for: {', '.join(watchlist)}"

    logger.info(f"Starting autonomous daily analysis for watchlist ({len(watchlist)} companies): {watchlist}")

    initial_state = {
        "user_request": query,
        "companies": watchlist,
        "execution_plan": ["research", "technical", "news", "report", "reflection", "critic"],
        "current_step": 0,
        "execution_trace": [],
        "timings": {},
        "errors": [],
    }

    final_state = graph.invoke(initial_state)
    report_markdown = final_state.get("report", "# Daily Market Intelligence Report\n\nNo report output generated.")
    trace = final_state.get("execution_trace", [])

    # Step 1: Detect Smart Alerts
    alerts = detect_smart_alerts(final_state)
    logger.info(f"Smart Alert Engine detected {len(alerts)} alerts.")

    # Step 2: Archive Daily Report Markdown File
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    archived_path = archive_daily_report(report_markdown, date_str)
    print(f"\n[+] Daily Markdown Report Archived: {archived_path}")

    # Step 3: Check Smart Alert Filter
    smart_alert_only = settings.get("smart_alert_only", False)
    if smart_alert_only and not alerts:
        logger.info("Smart alert filter enabled and no alerts were triggered. Skipping email dispatch.")
        print("\n[i] Smart Alert filter enabled — No critical alerts triggered today. Email skipped.")
        return

    # Step 4: Render HTML Email Digest
    html_email = generate_html_email_digest(
        report_markdown=report_markdown,
        alerts=alerts,
        watchlist=watchlist,
        execution_trace=trace
    )

    # Step 5: Dispatch Email (unless --dry-run)
    subject_line = f"📈 AI Market Intelligence Daily Digest — {date_str}"
    if alerts:
        subject_line = f"⚡ [{len(alerts)} ALERTS] AI Market Intelligence Digest — {date_str}"

    if args.dry_run:
        print("\n[i] Dry run complete. Email generation verified (not sent).")
    else:
        recipient = settings.get("email_recipient")
        result = send_email_digest(
            subject=subject_line,
            html_content=html_email,
            recipient_email=recipient
        )
        print(f"\n[+] Email Dispatch Status: {result.get('status')} ({result.get('reason') or result.get('recipient') or result.get('error')})")

    print("\n" + "=" * 70)
    print("   DAILY AUTONOMOUS WORKFLOW COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()
