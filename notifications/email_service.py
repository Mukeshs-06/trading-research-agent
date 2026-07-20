import os
import smtplib
import datetime
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any
from core.logger import logger

def convert_markdown_to_clean_html(markdown_text: str) -> str:
    """
    Converts markdown text into email-compliant HTML, including full support for
    headers, lists, bold text, code tags, and Markdown Tables (| Col | Col |).
    """
    lines = markdown_text.split("\n")
    html_out = []
    in_list = False
    in_table = False
    table_lines = []

    def flush_list():
        nonlocal in_list
        if in_list:
            html_out.append("</ul>")
            in_list = False

    def process_table(t_lines: List[str]):
        if not t_lines:
            return ""
        
        header_cells = []
        body_rows = []

        for idx, tline in enumerate(t_lines):
            # Strip outer vertical bars if present
            clean_line = tline.strip()
            if clean_line.startswith("|"):
                clean_line = clean_line[1:]
            if clean_line.endswith("|"):
                clean_line = clean_line[:-1]

            cells = [c.strip() for c in clean_line.split("|")]

            # Skip table alignment delimiter row (| --- | --- |)
            if idx == 1 and all(set(c).issubset({"-", ":", " "}) for c in cells):
                continue

            if idx == 0:
                header_cells = cells
            else:
                body_rows.append(cells)

        t_html = ["<div style='overflow-x:auto; margin:20px 0;'><table style='width:100%; border-collapse:collapse; font-family:sans-serif; font-size:13px; background-color:#0f172a; border:1px solid #334155; border-radius:8px;'>"]
        
        # Header Row
        if header_cells:
            t_html.append("<thead><tr style='background-color:#1e293b; color:#38bdf8;'>")
            for cell in header_cells:
                t_html.append(f"<th style='padding:10px 12px; border:1px solid #334155; text-align:left; font-weight:600;'>{cell}</th>")
            t_html.append("</tr></thead>")

        # Body Rows
        if body_rows:
            t_html.append("<tbody>")
            for r_idx, row in enumerate(body_rows):
                bg_color = "#0f172a" if r_idx % 2 == 0 else "#1e293b"
                t_html.append(f"<tr style='background-color:{bg_color};'>")
                for cell in row:
                    t_html.append(f"<td style='padding:8px 12px; border:1px solid #334155; color:#cbd5e1;'>{cell}</td>")
                t_html.append("</tr>")
            t_html.append("tbody>")

        t_html.append("</table></div>")
        return "".join(t_html)

    for line in lines:
        line_str = line.strip()

        # Table Line Detection
        if line_str.startswith("|") and line_str.endswith("|") and len(line_str) > 2:
            flush_list()
            in_table = True
            table_lines.append(line_str)
            continue
        else:
            if in_table:
                html_out.append(process_table(table_lines))
                table_lines = []
                in_table = False

        if not line_str:
            flush_list()
            continue

        if line_str.startswith("# "):
            flush_list()
            html_out.append(f"<h1 style='color:#38bdf8; font-family:sans-serif; margin-top:24px; font-size:22px;'>{line_str[2:]}</h1>")
        elif line_str.startswith("## "):
            flush_list()
            html_out.append(f"<h2 style='color:#818cf8; font-family:sans-serif; margin-top:20px; border-bottom:1px solid #334155; padding-bottom:6px; font-size:18px;'>{line_str[3:]}</h2>")
        elif line_str.startswith("### "):
            flush_list()
            html_out.append(f"<h3 style='color:#cbd5e1; font-family:sans-serif; margin-top:16px; font-size:15px;'>{line_str[4:]}</h3>")
        elif line_str.startswith("- ") or line_str.startswith("* "):
            if not in_list:
                html_out.append("<ul style='color:#e2e8f0; line-height:1.6; margin:8px 0; padding-left:20px;'>")
                in_list = True
            item_content = line_str[2:].replace("**", "<b>").replace("**", "</b>")
            html_out.append(f"<li style='margin-bottom:4px;'>{item_content}</li>")
        else:
            flush_list()
            p_content = line_str.replace("**", "<b>").replace("**", "</b>")
            # Inline code formatting
            p_content = re.sub(r'`([^`]+)`', r'<code style="background:#1e293b; color:#38bdf8; padding:2px 6px; border-radius:4px; font-size:12px;">\1</code>', p_content)
            html_out.append(f"<p style='color:#cbd5e1; line-height:1.6; margin:8px 0;'>{p_content}</p>")

    flush_list()
    if in_table:
        html_out.append(process_table(table_lines))

    return "\n".join(html_out)


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
        <div style="max-width:750px; margin:0 auto; background-color:#0f172a; border:1px solid #1e293b; border-radius:12px; padding:30px;">
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
