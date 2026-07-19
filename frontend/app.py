import streamlit as st
import streamlit.components.v1 as components
import time
import os
import sys
import json

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from graph.workflow import graph
from tools.registry import TOOLS

# Page Configuration
st.set_page_config(
    page_title="AI Trading Research Agent — Quantum Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Glassmorphism & Cyberpunk Dark Theme Styling
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;800&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #f3f4f6;
}

/* Background gradient */
.stApp {
    background: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #0f172a 40%, #030712 100%) !important;
}

/* Main Container Card */
.glass-card {
    background: rgba(15, 23, 42, 0.65);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
    margin-bottom: 20px;
}

/* Glowing Neon Headers */
.gradient-heading {
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.5rem;
    margin-bottom: 0.2rem;
}

.gradient-subheading {
    color: #94a3b8;
    font-size: 1.05rem;
    font-weight: 400;
}

/* Custom Prompt Pill Buttons */
.prompt-pill {
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(148, 163, 184, 0.2);
    border-radius: 20px;
    padding: 8px 16px;
    color: #e2e8f0;
    font-size: 0.88rem;
    cursor: pointer;
    transition: all 0.3s ease;
    display: inline-block;
    margin-right: 8px;
    margin-bottom: 8px;
}
.prompt-pill:hover {
    border-color: #38bdf8;
    background: rgba(56, 189, 248, 0.15);
    box-shadow: 0 0 15px rgba(56, 189, 248, 0.3);
}

/* Agent Node Status Cards */
.node-card {
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 10px;
    transition: transform 0.2s ease, border-color 0.2s ease;
}
.node-card:hover {
    transform: translateY(-2px);
    border-color: #818cf8;
}

.node-title {
    font-family: 'Outfit', sans-serif;
    font-weight: 700;
    font-size: 0.95rem;
    color: #38bdf8;

    display: flex;
    justify-content: space-between;
}

/* Markdown Tables formatting */
table {
    width: 100% !important;
    border-collapse: separate !important;
    border-spacing: 0 !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    margin: 16px 0 !important;
}

th {
    background: rgba(30, 41, 59, 0.9) !important;
    color: #38bdf8 !important;
    font-weight: 600 !important;
    padding: 12px 16px !important;
    text-align: left !important;
}

td {
    background: rgba(15, 23, 42, 0.6) !important;
    padding: 12px 16px !important;
    border-top: 1px solid rgba(255, 255, 255, 0.05) !important;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# 3D Interactive WebGL Financial Particle Sphere Canvas Header Component
THREEJS_3D_CANVAS = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; background: transparent; }
        canvas { display: block; width: 100vw; height: 180px; }
    </style>
</head>
<body>
    <div id="canvas-container"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / 180, 0.1, 1000);
        camera.position.z = 200;

        const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        renderer.setSize(window.innerWidth, 180);
        container.appendChild(renderer.domElement);

        // Create Quantum Financial Sphere Particle System
        const geometry = new THREE.BufferGeometry();
        const count = 700;
        const positions = new Float32Array(count * 3);
        const colors = new Float32Array(count * 3);

        const color1 = new THREE.Color('#38bdf8');
        const color2 = new THREE.Color('#818cf8');
        const color3 = new THREE.Color('#c084fc');

        for(let i=0; i<count; i++) {
            const u = Math.random();
            const v = Math.random();
            const theta = u * 2.0 * Math.PI;
            const phi = Math.acos(2.0 * v - 1.0);
            const r = 65 + Math.random() * 8;

            positions[i*3] = r * Math.sin(phi) * Math.cos(theta);
            positions[i*3+1] = r * Math.sin(phi) * Math.sin(theta);
            positions[i*3+2] = r * Math.cos(phi);

            let mixedColor = color1.clone().lerp(color2, Math.random()).lerp(color3, Math.random());
            colors[i*3] = mixedColor.r;
            colors[i*3+1] = mixedColor.g;
            colors[i*3+2] = mixedColor.b;
        }

        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

        const material = new THREE.PointsMaterial({
            size: 2.2,
            vertexColors: true,
            transparent: true,
            opacity: 0.85
        });

        const particles = new THREE.Points(geometry, material);
        scene.add(particles);

        // Outer Wireframe Ring
        const ringGeo = new THREE.TorusGeometry(85, 0.4, 16, 100);
        const ringMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8, wireframe: true, transparent: true, opacity: 0.25 });
        const ring = new THREE.Mesh(ringGeo, ringMat);
        ring.rotation.x = Math.PI / 3;
        scene.add(ring);

        function animate() {
            requestAnimationFrame(animate);
            particles.rotation.y += 0.003;
            particles.rotation.x += 0.001;
            ring.rotation.z += 0.002;
            renderer.render(scene, camera);
        }
        animate();

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / 180;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, 180);
        });
    </script>
</body>
</html>
"""

# Render 3D Canvas
components.html(THREEJS_3D_CANVAS, height=185)

# Application Title & Subtitle
st.markdown('<div class="gradient-heading">AI Trading Research Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="gradient-subheading">Next-Gen Multi-Agent Financial Intelligence Platform with Parallel LangGraph Orchestration & Live Tracing</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Sidebar Design
with st.sidebar:
    st.image("https://img.icons8.com/isometric-folders/100/combo-chart.png", width=64)
    st.markdown("### ⚡ System Command Center")
    st.info("Powered by LangGraph, Llama-3.3-70B & Atomic Financial Tools.")

    st.markdown("---")
    st.markdown("#### 🛠️ Atomic Tools Registered")
    for tool in TOOLS:
        st.markdown(f"🔹 **`{tool.name}`**")
        st.caption(tool.description.split('.')[0])

    st.markdown("---")
    st.markdown("#### 🤖 Specialized Agent Swarm")
    st.markdown("• **Planner**: Selective Query Planner\n• **Research**: Fundamentals & Market Cap\n• **Technical**: Momentum, RSI, Support/Resistance\n• **News**: Headlines & Sentiment Reasoning\n• **Report**: Factual Synthesizer\n• **Reflection**: Completeness Audit\n• **Critic**: Fast Compliance Auditor")

# Preset Prompt Chips
st.markdown("#### 💡 Quick Prompts")
p_col1, p_col2, p_col3, p_col4 = st.columns(4)
selected_prompt = None

if p_col1.button("⚡ Compare Apple & Microsoft"):
    selected_prompt = "Compare Apple and Microsoft fundamentals, technical indicators, and recent news."

if p_col2.button("📈 Tesla Technicals & Swing Levels"):
    selected_prompt = "What are Tesla technical indicators, momentum, RSI, and swing support/resistance levels?"

if p_col3.button("📰 NVIDIA Headlines & Sentiment"):
    selected_prompt = "Show me recent NVIDIA headlines, business impact, and sentiment."

if p_col4.button("🔍 Full Audit: Apple Stock"):
    selected_prompt = "Conduct a full deep research audit on Apple stock fundamentals and technicals."

# Conversational Input Box (ChatGPT/Claude Style)
user_query = st.text_area(
    "Ask anything about stocks, technicals, or market intelligence:",
    value=selected_prompt or "",
    placeholder="e.g. Compare Apple and Microsoft fundamentals, technical indicators, and recent news...",
    height=90,
    key="main_user_query",
)

if st.button("✨ Run Quantum Agent Swarm", type="primary", use_container_width=True):
    if not user_query.strip():
        st.warning("Please enter a stock query or click a quick prompt.")
    else:
        st.markdown("---")
        st.markdown("### ⚡ Live Multi-Agent Parallel Graph Execution")

        # Parallel Topology Flow Visualizer
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
                         [ Reflection / Critic / HITL ]
        ```
        """)

        initial_state = {
            "user_request": user_query,
            "companies": [],
            "execution_plan": [],
            "current_step": 0,
            "execution_trace": [],
            "timings": {},
            "errors": [],
        }

        with st.spinner("Executing agent swarm in parallel branches..."):
            start_t = time.time()
            final_state = graph.invoke(initial_state)
            total_duration = round(time.time() - start_t, 2)

        st.session_state["graph_state"] = final_state
        st.success(f"Execution completed in **{total_duration} seconds** across parallel agent nodes!")

# If results exist in session state, render output tabs
if "graph_state" in st.session_state:
    final_state = st.session_state["graph_state"]
    trace = final_state.get("execution_trace", [])

    # Execution Trace Nodes Timeline
    with st.expander("⏱️ Live Execution Timeline & Atomic Tool Invocation Logs", expanded=True):
        t_cols = st.columns(len(trace)) if len(trace) > 0 else [st.container()]
        for i, item in enumerate(trace):
            step_name = item["step"].upper()
            duration = item["duration_seconds"]
            tools = item.get("tools_called", [])
            with t_cols[min(i, len(t_cols)-1)]:
                st.markdown(f"""
                <div class="node-card">
                    <div class="node-title"><span>✓ {step_name}</span> <span>{duration}s</span></div>
                    <div style="font-size:0.8rem; color:#94a3b8; margin-top:6px;">
                        Tools: {', '.join([f'`{t}`' for t in tools]) if tools else 'LLM Reasoning'}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")
    tab1, tab2, tab3, tab4 = st.tabs([
        "📄 Institutional Equity Report",
        "🤝 Human-in-the-Loop Analyst Gate",
        "📊 Telemetry & Audit Matrix",
        "🔍 Raw Graph State"
    ])

    with tab1:
        report_content = final_state.get("report", "No report generated.")
        st.markdown(report_content)
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="📥 Download Full Equity Research Report (.md)",
            data=report_content,
            file_name="equity_research_report.md",
            mime="text/markdown",
        )

    with tab2:
        st.markdown("### 🤝 Human Analyst Approval & Feedback Workflow")
        st.write("Inspect the generated report above. As a senior analyst, you can approve the report or request automated LLM revision with custom feedback.")

        h_col1, h_col2 = st.columns(2)
        with h_col1:
            if st.button("✅ Approve Report Integrity", type="primary"):
                final_state["human_approved"] = True
                st.success("Report successfully approved by Human Analyst!")

        with h_col2:
            feedback_text = st.text_input("Revision Instructions:", placeholder="e.g. Add deeper breakdown of 52-week price range...")
            if st.button("🔄 Request Revision with Feedback"):
                if feedback_text.strip():
                    with st.spinner("Re-invoking Report Agent with custom human analyst feedback..."):
                        final_state["human_approved"] = False
                        final_state["human_feedback"] = feedback_text
                        final_state["revision_count"] = final_state.get("revision_count", 0) + 1
                        updated_state = graph.invoke(final_state)
                        st.session_state["graph_state"] = updated_state
                        st.rerun()
                else:
                    st.warning("Please enter feedback before requesting revision.")

    with tab3:
        st.markdown("### ⏱️ Agent Latency & Performance Breakdown")
        timings = final_state.get("timings", {})
        st.bar_chart(timings)

        col_audit1, col_audit2 = st.columns(2)
        with col_audit1:
            st.markdown("#### 🔍 Reflection Agent Audit")
            st.json(final_state.get("reflection", {"status": "NOT_EXECUTED"}))

        with col_audit2:
            st.markdown("#### ⚖️ Critic Compliance Audit")
            st.json(final_state.get("critic", {"status": "NOT_EXECUTED"}))

    with tab4:
        st.json(final_state)
