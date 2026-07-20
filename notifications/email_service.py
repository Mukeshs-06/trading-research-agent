import os
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any
from core.logger import logger

def convert_markdown_to_clean_html(markdown_text: str) -> str:
    """
    Simple markdown-to-HTML converter for report synthesis.
    Converts headers, lists, code blocks, and basic bold text.
    """
    html_lines = []
    in_list = False

    for line in markdown_text.split("\n"):
        line_str = line.strip()
        if not line_str:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            continue

        if line_str.startswith("# "):
            html_lines.append(f"<h1 style='color:#38bdf8; font-family:sans-serif; margin-top:24px;'>{line_str[2:]}</h1>")
        elif line_str.startswith("## "):
            html_lines.append(f"<h2 style='color:#818cf8; font-family:sans-serif; margin-top:20px; border-bottom:1px solid #334155; padding-bottom:6px;'>{line_str[3:]}</h2>")
        elif line_str.startswith("### "):
            html_lines.append(f"<h3 style='color:#cbd5e1; font-family:sans-serif; margin-top:16px;'>{line_str[4:]}</h3>")
        elif line_str.startswith("- ") or line_str.startswith("* "):
            if not in_list:
                html_lines.append("<ul style='color:#e2e8f0; line-height:1.6;'>")
                in_list = True
            item_content = line_str[2:].replace("**", "<b>").replace("**", "</b>")
            html_lines.append(f"<li>{item_content}</li>")
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            p_content = line_str.replace("**", "<b>").replace("**", "</b>")
            html_lines.append(f"<p style='color:#cbd5e1; line-height:1.6;'>{p_content}</p>")

    if in_list:
        html_lines.append("</ul>")

    return "\n".join(html_lines)


def generate_html_email_digest(
    report_markdown: str,
    alerts: List[Dict[str, Any]],
    watchlist: List[str],
    execution_trace: List[Dict[str, Any]],
) -> str:
    """
    Generates a dark-themed HTML email digest with alert banners, stock tables, and execution logs.
    """
    date_str = datetime.datetime.now().strftime("%B %d, %Y")

    # Render Alert Banners if present
    alert_html = ""
    if alerts:
        alert_html = "<div style='margin-bottom:24px; padding:16px; background:#1e1b4b; border-left:4px solid #f43f5e; border-radius:8px;'>"
        alert_html += "<h3 style='margin:0 0 10px 0; color:#f43f5e; font-family:sans-serif;'>⚡ Significant Market Alerts Triggered</h3>"
        for alert in alerts:
            color = "#f43f5e" if alert["severity"] == "HIGH" else ("#fbbf24" if alert["severity"] == "WARNING" else "#10b981")
            alert_html += f"<p style='margin:4px 0; color:{color}; font-family:sans-serif; font-size:14px;'>• <b>[{alert['company']}]</b> {alert['message']}</p>"
        alert_html += "</div>"

    body_content = convert_markdown_to_clean_html(report_markdown)

    # Execution Trace Footer
    trace_html = "<div style='margin-top:30px; padding:16px; background:#0f172a; border-radius:8px; border:1px solid #1e293b;'>"
    trace_html += "<h4 style='color:#94a3b8; margin:0 0 10px 0; font-family:sans-serif;'>🤖 Autonomous Agent Telemetry Log</h4>"
    trace_html += "<table style='width:100%; font-size:12px; color:#cbd5e1; font-family:monospace; border-collapse:collapse;'>"
    trace_html += "<tr style='color:#64748b; text-align:left;'><th>Node</th><th>Status</th><th>Duration</th><th>Tools Invoked</th></tr>"
    for item in execution_trace:
        tools = ", ".join(item.get("tools_called", [])) or "LLM Reasoning"
        trace_html += f"<tr style='border-top:1px solid #1e293b;'><td style='padding:6px;'>{item['step'].upper()}</td><td style='color:#10b981;'>{item['status']}</td><td>{item['duration_seconds']}s</td><td>{tools}</td></tr>"
    trace_html += "</table></div>"

    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
    </head>
    <body style="background-color:#030712; color:#f3f4f6; font-family:'Segoe UI', Helvetica, Arial, sans-serif; margin:0; padding:20px;">
        <div style="max-width:700px; margin:0 auto; background-color:#0f172a; border:1px solid #1e293b; border-radius:12px; padding:30px;">
            <div style="border-bottom:1px solid #1e293b; padding-bottom:16px; margin-bottom:20px;">
                <h1 style="color:#38bdf8; margin:0; font-size:24px;">📈 Autonomous AI Market Intelligence</h1>
                <p style="color:#64748b; margin:6px 0 0 0; font-size:14px;">Daily Digest • {date_str} • Monitored Watchlist: {', '.join(watchlist)}</p>
            </div>

            {alert_html}

            <div style="font-size:15px;">
                {body_content}
            </div>

            {trace_html}

            <div style="margin-top:30px; text-align:center; font-size:12px; color:#475569; border-top:1px solid #1e293b; padding-top:16px;">
                Automated report generated by AI Trading Research Platform • Non-advisory financial intelligence
            </div>
        </div>
    </body>
    </html>
    """

    return html_template


def send_email_digest(
    subject: str,
    html_content: str,
    recipient_email: str = None
) -> Dict[str, Any]:
    """
    Sends the HTML email digest via Gmail SMTP using environment variables.
    EMAIL_USER and EMAIL_PASSWORD (App Password).
    """
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASSWORD")
    target_email = recipient_email or email_user

    if not email_user or not email_pass:
        logger.warning("EMAIL_USER or EMAIL_PASSWORD not set in environment. Skipping email dispatch.")
        return {
            "status": "SKIPPED",
            "reason": "Missing EMAIL_USER or EMAIL_PASSWORD environment variables."
        }

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"AI Market Intelligence <{email_user}>"
        msg["To"] = target_email

        html_part = MIMEText(html_content, "html")
        msg.attach(html_part)

        logger.info(f"Connecting to Gmail SMTP to send email digest to {target_email}...")
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(email_user, email_pass)
            server.sendmail(email_user, target_email, msg.as_string())

        logger.info("Email digest sent successfully via Gmail SMTP!")
        return {"status": "SUCCESS", "recipient": target_email}

    except Exception as e:
        logger.error(f"Failed to send email digest via Gmail SMTP: {e}")
        return {"status": "FAILED", "error": str(e)}
