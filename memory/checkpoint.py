from langgraph.checkpoint.memory import MemorySaver
from core.logger import logger

def get_checkpointer() -> MemorySaver:
    """
    Instantiates and returns a MemorySaver checkpointer for state persistence.
    """
    logger.info("Initializing LangGraph MemorySaver checkpointer...")
    return MemorySaver()
