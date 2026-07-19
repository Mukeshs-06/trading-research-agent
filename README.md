# 📈 AI Trading Research Platform

A production-grade, multi-agent AI system for automated equity research, fundamental analysis, technical indicator evaluation, and news sentiment synthesis built with **LangGraph**, **LangChain**, **FastAPI**, **Streamlit**, and **Groq (Llama-3.3-70B)**.

---

## 🌟 Key Architectural Features

- **Parallel LangGraph Execution**: Runs `Research`, `Technical`, and `News` data collection nodes concurrently in parallel branches, reducing total pipeline latency.
- **Selective Query Planning**: `Planner Agent` dynamically selects only the necessary specialized agents based on user intent (e.g. news-only vs. full comparative research).
- **Atomic Tool Orchestration**: Agents directly invoke atomic financial tools (`resolve_company`, `get_stock_data`, `technical_analysis`, `get_company_news`) without unnecessary composite wrappers.
- **Support & Resistance Precision**: swing high/low 6-month support (`df["Low"].min()`) and resistance (`df["High"].max()`) calculations.
- **Strict Non-Advisory Neutrality**: Enforces non-advisory quantitative reporting standards (no "buy/sell" recommendations or predictive assertions).
- **Human-in-the-Loop (HITL)**: Built-in human analyst approval & revision workflow.
- **Execution Trace & Telemetry**: Records real-time step duration, tool calls, evidence counts (`X Bullish, Y Bearish, Z Neutral`), and confidence metrics.
- **Production Suite**: FastAPI REST service, interactive Streamlit dashboard, Pytest test suites, structured rotating logs, and Docker containerization.

---

## 🏗️ Parallel Architecture Diagram

```
                             [ User Request / Query ]
                                         │
                                         ▼
                                  ┌─────────────┐
                                  │ Planner Node│
                                  └──────┬──────┘
                                         │ (Selective & Parallel Branch Scheduling)
           ┌─────────────────────────────┼─────────────────────────────┐
           ▼                             ▼                             ▼
   ┌──────────────┐              ┌──────────────┐              ┌──────────────┐
   │Research Node │              │Technical Node│              │  News Node   │
   └──────┬───────┘              └──────┬───────┘              └──────┬───────┘
          │ (Atomic Tools)              │ (Atomic Tools)              │ (Atomic Tools)
          ▼                             ▼                             ▼
  • resolve_company             • resolve_company             • get_company_news
  • get_stock_data              • technical_analysis          (LLM Sentiment Reasoning)
          │                             │                             │
          └─────────────────────────────┼─────────────────────────────┘
                                        │ (Parallel Branch Convergence)
                                        ▼
                                 ┌──────────────┐
                                 │ Report Node  │
                                 └──────┬───────┘
                                        │ (Optional Audit & Revision)
                                        ▼
                              ┌────────────────────┐
                              │ Reflection / Critic│
                              └─────────┬──────────┘
                                        │ (Human Analyst Approval)
                                        ▼
                              ┌────────────────────┐
                              │    HITL Review     │
                              └─────────┬──────────┘
                                        │
                                        ▼
                           [ Execution Trace & Report ]
```

---

## 📁 Repository Structure

```
trading-research-agent/
├── core/
│   ├── settings.py          # Environment, API keys & LLM initialization
│   ├── logger.py            # Centralized logging with console & file rotation
│   └── constants.py         # System constants & defaults
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
│   ├── state.py             # GraphState with HITL fields & trace telemetry
│   ├── router.py            # Parallel fanout router & reflection revision router
│   ├── nodes.py             # Graph nodes executing tools and agents
│   └── workflow.py          # Compiled LangGraph StateGraph
├── prompts/                 # System prompts
├── memory/
│   ├── conversation.py      # Conversation history manager
│   └── checkpoint.py        # Thread state checkpointer
├── api/
│   ├── main.py              # FastAPI application entrypoint
│   ├── routes.py            # REST endpoints (/analyze, /health, /tools, /agents, /history)
│   └── schemas.py           # Pydantic request & response models
├── frontend/
│   └── app.py               # Streamlit Dashboard with Parallel Diagram & HITL
├── tests/
│   ├── unit/                # Unit tests for tools & planner
│   └── integration/         # Integration tests for workflow & API
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── config.py                # Backward compatibility bridge
├── app.py                   # CLI runner
├── requirements.txt
└── README.md
```

---

## ⚡ Quick Start

### 1. Environment Setup

Copy `.env` and set your `GROQ_API_KEY`:

```bash
GROQ_API_KEY=your_groq_api_key_here
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Run CLI

```bash
python app.py "Compare Apple and Microsoft fundamentals and technicals"
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

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Service health status & LLM model parameters |
| `POST` | `/analyze` | Executes multi-agent research workflow |
| `GET` | `/tools` | Returns registered atomic tools |
| `GET` | `/agents` | Returns registered specialized agents |
| `GET` | `/history` | Returns recent research query history |

---

## 🧪 Testing

Run all unit and integration tests using Pytest:

```bash
pytest tests/
```

---

## 🐳 Docker Deployment

Run the complete platform via Docker Compose:

```bash
docker-compose -f docker/docker-compose.yml up --build
```
