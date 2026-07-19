import time
from typing import List, Dict, Any
from core.logger import logger

class ConversationMemory:
    """
    In-memory conversation history store for cross-request context.
    """
    def __init__(self):
        self._history: List[Dict[str, Any]] = []

    def add_entry(self, user_request: str, companies: List[str], report_summary: str, trace: List[Dict[str, Any]]) -> None:
        entry = {
            "timestamp": time.time(),
            "user_request": user_request,
            "companies": companies,
            "report_summary": report_summary[:300] + "..." if len(report_summary) > 300 else report_summary,
            "trace_summary": [t["step"] for t in trace],
        }
        self._history.append(entry)
        logger.info(f"Added memory entry for query: '{user_request}' ({len(companies)} companies)")

    def get_recent_history(self, limit: int = 5) -> List[Dict[str, Any]]:
        return self._history[-limit:]

    def clear(self) -> None:
        self._history.clear()

memory_store = ConversationMemory()
