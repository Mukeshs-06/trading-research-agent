from graph.workflow import graph
from core.logger import logger
import sys

def main():
    print("=" * 60)
    print("   AI TRADING RESEARCH AGENT — CLI RUNNER")
    print("=" * 60)

    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("\nEnter company analysis query (e.g. 'Analyze Apple and Microsoft fundamentals'):\n> ").strip()

    if not query:
        query = "Compare Apple and Microsoft fundamentals and technicals"

    print(f"\nProcessing query: '{query}'...\n")

    initial_state = {
        "user_request": query,
        "companies": [],
        "execution_plan": [],
        "current_step": 0,
        "execution_trace": [],
        "timings": {},
        "errors": [],
    }

    final_state = graph.invoke(initial_state)

    print("\n" + "=" * 60)
    print("   EXECUTION TIMELINE & TRACE")
    print("=" * 60)
    for trace in final_state.get("execution_trace", []):
        print(f"[{trace['step'].upper()}] - {trace['status']} ({trace['duration_seconds']}s) - Tools: {trace.get('tools_called', [])}")

    print("\n" + "=" * 60)
    print("   SYNTHESIZED EQUITY RESEARCH REPORT")
    print("=" * 60)
    print(final_state.get("report", "No report generated."))
    print("=" * 60)

if __name__ == "__main__":
    main()