"""
Backwards-compatibility bridge for config imports.
Refers directly to core.settings.
"""

from core.settings import (
    GROQ_API_KEY as api_key,
    get_llm,
    llm,
)

__all__ = ["api_key", "get_llm", "llm"]