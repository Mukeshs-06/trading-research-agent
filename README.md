# 📈 Autonomous AI Market Intelligence & Research Platform

[![Live Streamlit Demo](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://trading-research-agent-hxwhnkaau9mebe4arh2arz.streamlit.app/)
[![CI Test Suite](https://github.com/Mukeshs-06/trading-research-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/Mukeshs-06/trading-research-agent/actions/workflows/ci.yml)
[![Daily Autonomous Intelligence](https://github.com/Mukeshs-06/trading-research-agent/actions/workflows/daily_report.yml/badge.svg)](https://github.com/Mukeshs-06/trading-research-agent/actions/workflows/daily_report.yml)

> 🚀 **Live Web Dashboard**: [https://trading-research-agent-hxwhnkaau9mebe4arh2arz.streamlit.app/](https://trading-research-agent-hxwhnkaau9mebe4arh2arz.streamlit.app/)

A production-grade **Autonomous AI Market Intelligence Platform** for automated equity research, technical indicator evaluation, news sentiment synthesis, and daily email digests built with **LangGraph**, **LangChain**, **FastAPI**, **Streamlit**, and **Groq (Llama-3.3-70B)**.

---

## 🌟 Key Architectural Capabilities

- **Autonomous Daily Market Intelligence**: Scheduled GitHub Actions workflow (`.github/workflows/daily_report.yml`) runs daily cron scans across a configurable stock watchlist (`config/watchlist.yaml`).
- **Smart Alert Engine**: Automatically detects RSI overbought/oversold levels (>70 / <30), 6-month support/resistance breaches, and trend shifts vs cached state.
- **Gmail SMTP HTML Email Digest**: Dispatches responsive HTML email reports (`notifications/email_service.py`) featuring dark-theme formatting, comparison tables, alert badges, and tool logs.
- **Daily Markdown Archival**: Archives daily market intelligence reports to `reports/YYYY-MM-DD.md` and commits them back to GitHub automatically.
- **Parallel LangGraph Execution**: Runs `Research`, `Technical`, and `News` data collection nodes concurrently in parallel branches.
- **Atomic Tool Orchestration**: Agents directly invoke atomic tools (`resolve_company`, `get_stock_data`, `technical_analysis`, `get_company_news`) without heavy wrappers.
- **Human-in-the-Loop (HITL)**: Built-in human analyst approval & revision workflow.
- **Production Suite**: FastAPI REST API, Streamlit Web UI, Docker Compose deployment, 100% Pytest coverage, and structured rotating logs.

---

## 🏗️ System Architecture

```text
                 GitHub Actions Cron Workflow
             (.github/workflows/daily_report.yml)
                              │
                              ▼
                  Watchlist Configuration
                   (config/watchlist.yaml)
                              │
                              ▼
                 LangGraph Multi-Agent Swarm
            (Planner → Research, Technical, News → Report)
                              │
           ┌──────────────────┼──────────────────┐
           ▼                  ▼                  ▼
     Smart Alert      Report Archiver       HTML Email Engine
      Detector       (reports/YYYY-MM-DD)  (notifications/email_service.py)
           │                                     │
           └──────────────────┬──────────────────┘
                              ▼
                     Gmail SMTP Dispatcher
                 (EMAIL_USER / EMAIL_PASSWORD)
```

---

## 📁 Repository Structure

```
trading-research-agent/
├── config/
│   ├── watchlist.yaml       # Configurable stock watchlist & alert thresholds
│   ├── settings.py          # Environment, API keys & LLM initialization
│   ├── logger.py            # Centralized logging with console & file rotation
│   └── constants.py         # System constants & defaults
├── scripts/
│   └── daily_report.py      # Headless daily autonomous runner & email dispatcher
├── notifications/
│   └── email_service.py     # HTML email template generator & Gmail SMTP dispatcher
├── reports/                 # Historical daily archived markdown reports (YYYY-MM-DD.md)
├── agents/
│   ├── planner_agent.py     # Parses query and returns selective plan JSON
│   ├── research_agent.py    # Fundamental stock data synthesis
│   ├── news_agent.py        # News aggregation & LLM sentiment reasoning
│   ├── technical_agent.py   # Historical prices, RSI, MACD, Moving Averages
│   ├── report_agent.py      # Non-advisory equity report writer with tool footer
│   ├── reflection_agent.py  # Optional report completeness auditor
│   └── critic_agent.py      # Fast compliance & hallucination auditor
├── tools/
│   ├── financial/
│   │   ├── stock_tool.py    # Yahoo Finance fundamental metrics
│   │   └── technical_tool.py# Swing support/resistance, RSI, MACD, evidence count
│   ├── market/
│   │   └── news_tool.py     # RSS news headline fetcher
│   ├── utility/
│   │   └── company_resolver.py# Company name to Ticker lookup tool
│   └── registry.py          # Unified tool registry
├── graph/
│   ├── state.py             # GraphState with HITL & trace telemetry
│   ├── router.py            # Parallel fanout router & reflection revision router
│   ├── nodes.py             # Graph nodes executing tools and agents
│   └── workflow.py          # Compiled LangGraph StateGraph
├── memory/
│   ├── report_archive.py    # Report archival & smart alert detection engine
│   ├── conversation.py      # Conversation history manager
│   └── checkpoint.py        # Thread state checkpointer
├── api/
│   ├── main.py              # FastAPI application entrypoint
│   ├── routes.py            # REST endpoints (/analyze, /health, /tools, /agents, /history)
│   └── schemas.py           # Pydantic request & response models
├── frontend/
│   └── app.py               # Streamlit Dashboard with Parallel Diagram & HITL
├── tests/
│   ├── unit/                # Unit tests for tools, planner, and automation
│   └── integration/         # Integration tests for workflow & API
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## ⚡ Quick Start

### 1. Environment Setup

Configure environment variables in `.env`:

```bash
GROQ_API_KEY=your_groq_api_key_here
EMAIL_USER=your_gmail_address@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Run Daily Autonomous Script Locally

Run dry-run (generates report & archives without sending email):

```bash
python scripts/daily_report.py --dry-run
```

Run full execution & send HTML email digest:

```bash
python scripts/daily_report.py
```

### 3. Run Web Dashboard (Streamlit)

```bash
streamlit run frontend/app.py
```

### 4. Run REST API (FastAPI)

```bash
uvicorn api.main:app --reload --port 8000
```

---

## 🔐 Setting Up Gmail SMTP Email Notifications

To receive free daily HTML email digests:
1. Enable **2-Step Verification** on your Google Account.
2. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).
3. Create an **App Password** named `AI Market Intelligence`.
4. On GitHub: Go to your Repo -> **Settings** -> **Secrets and variables** -> **Actions**.
5. Add Secret `EMAIL_USER`: your Gmail address.
6. Add Secret `EMAIL_PASSWORD`: your 16-character App Password.

---

## 🧪 Testing

Run all 13 unit and integration tests using Pytest:

```bash
pytest tests/
```

---

## 🐳 Docker Deployment

Run the complete platform via Docker Compose:

```bash
docker-compose -f docker/docker-compose.yml up --build
```
