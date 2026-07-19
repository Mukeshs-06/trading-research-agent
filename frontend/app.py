import streamlit as st
import time
import os
import sys

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from graph.workflow import graph
from tools.registry import TOOLS

st.set_page_config(
    page_title="AI Trading Research Agent",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📈 AI Trading Research Platform")
st.caption("Production Multi-Agent Financial Intelligence Platform with Parallel LangGraph Execution & Human-in-the-Loop")

# Sidebar
with st.sidebar:
    st.header("⚙️ System Architecture")
    st.success("⚡ Parallel Branch Execution Enabled")
    st.info("System uses ChatGroq Llama-3.3-70B & yfinance atomic tools.")
    
    st.subheader("🛠️ Atomic Tools Exposed")
    for tool in TOOLS:
        st.markdown(f"• **`{tool.name}`**: {tool.description.split('.')[0]}")
    
    st.markdown("---")
    st.subheader("🤖 Active Agents")
    st.markdown("• **Planner**: Selective Query Planning\n• **Research**: Fundamentals & Market Cap\n• **Technical**: Momentum, RSI, Swing Support/Resistance\n• **News**: Headlines & LLM Sentiment Reasoning\n• **Report**: Non-advisory Synthesizer\n• **Reflection**: Completeness Audit\n• **Critic**: Fast Compliance Auditor")

# Sample Queries
st.subheader("💡 Preset Research Queries")
col1, col2, col3, col4 = st.columns(4)
selected_prompt = None

if col1.button("Compare Apple & Microsoft"):
    selected_prompt = "Compare Apple and Microsoft fundamentals, technical indicators, and recent news."

if col2.button("Tesla Technicals"):
    selected_prompt = "What are Tesla technical indicators, momentum, RSI, and support/resistance?"

if col3.button("NVIDIA Recent News"):
    selected_prompt = "Show me recent NVIDIA headlines, business impact, and sentiment."

if col4.button("Full Deep Research"):
    selected_prompt = "Conduct a deep research audit on Apple stock fundamentals and technicals."

# User Input Form
user_query = st.text_area(
    "Enter Stock Query or Company Analysis Request:",
    value=selected_prompt or "",
    placeholder="e.g., Conduct thorough fundamental and technical analysis on Apple and Google...",
    height=90,
)

if st.button("🚀 Execute Multi-Agent Graph", type="primary", use_container_width=True):
    if not user_query.strip():
        st.warning("Please enter a research query or select a sample prompt.")
    else:
        st.markdown("---")
        st.subheader("⚡ Parallel Execution Timeline & Graph Tracing")
        
        # Display Parallel Execution Branch Diagram
        st.markdown("""
        ```text
                               ┌─────────────┐
                               │ Planner Node│
                               └──────┬──────┘
                                      │ (Parallel Branch Scheduling)
                  ┌───────────────────┼───────────────────┐
                  ▼                   ▼                   ▼
           ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
           │Research Node │    │Technical Node│    │  News Node   │
           └──────┬───────┘    └──────┬───────┘    └──────┬───────┘
                  │                   │                   │
                  └───────────────────┼───────────────────┘
                                      ▼
                               ┌──────────────┐
                               │ Report Node  │
                               └──────┬───────┘
                                      ▼
                           [Reflection / Critic / HITL]
        ```
        """)

        timeline_container = st.container()

        initial_state = {
            "user_request": user_query,
            "companies": [],
            "execution_plan": [],
            "current_step": 0,
            "execution_trace": [],
            "timings": {},
            "errors": [],
        }

        with st.spinner("Executing parallel LangGraph workflow..."):
            start_total = time.time()
            final_state = graph.invoke(initial_state)
            total_duration = round(time.time() - start_total, 2)

        st.session_state["graph_state"] = final_state
        st.success(f"Graph execution completed in {total_duration} seconds!")

# If state exists in session state, render results & HITL
if "graph_state" in st.session_state:
    final_state = st.session_state["graph_state"]
    trace = final_state.get("execution_trace", [])

    with st.expander("⏱️ Detailed Execution Traces & Timings", expanded=True):
        cols = st.columns(len(trace)) if len(trace) > 0 else [st.container()]
        for i, item in enumerate(trace):
            step_name = item["step"].upper()
            duration = item["duration_seconds"]
            tools = item.get("tools_called", [])
            with cols[min(i, len(cols)-1)]:
                st.metric(label=f"✓ {step_name}", value=f"{duration}s")
                if tools:
                    st.caption(f"Tools: `{', '.join(tools)}`")

    st.markdown("---")
    tab1, tab2, tab3, tab4 = st.tabs([
        "📄 Synthesized Report",
        "🤝 Human-in-the-Loop Review",
        "📊 Telemetry & Audit",
        "🔍 Raw State JSON"
    ])

    with tab1:
        report_content = final_state.get("report", "No report generated.")
        st.markdown(report_content)
        st.download_button(
            label="📥 Download Equity Research Report",
            data=report_content,
            file_name="equity_research_report.md",
            mime="text/markdown",
        )

    with tab2:
        st.subheader("🤝 Human-in-the-Loop Approval & Revision Gate")
        st.info("As a human analyst, you can inspect the generated report, approve it, or provide feedback for automated report revision.")
        
        hitl_col1, hitl_col2 = st.columns(2)
        with hitl_col1:
            if st.button("✅ Approve Report", type="primary"):
                st.success("Report approved by Human Analyst!")
                final_state["human_approved"] = True

        with hitl_col2:
            feedback_input = st.text_input("Feedback for Revision:", placeholder="e.g. Include more context on PE ratio comparison...")
            if st.button("🔄 Request Revision with Feedback"):
                if feedback_input:
                    with st.spinner("Re-executing Report Node with Human Analyst Feedback..."):
                        final_state["human_approved"] = False
                        final_state["human_feedback"] = feedback_input
                        final_state["revision_count"] = final_state.get("revision_count", 0) + 1
                        updated_state = graph.invoke(final_state)
                        st.session_state["graph_state"] = updated_state
                        st.rerun()
                else:
                    st.warning("Please enter feedback before requesting revision.")

    with tab3:
        st.subheader("⏱️ Timing & Performance Breakdown")
        timings = final_state.get("timings", {})
        st.bar_chart(timings)

        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("🔍 Reflection Agent Outcome")
            st.json(final_state.get("reflection", {"status": "NOT_EXECUTED"}))

        with col_b:
            st.subheader("⚖️ Critic Audit Outcome")
            st.json(final_state.get("critic", {"status": "NOT_EXECUTED"}))

    with tab4:
        st.json(final_state)
