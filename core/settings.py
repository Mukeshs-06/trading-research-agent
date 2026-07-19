import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from core.constants import DEFAULT_MODEL, DEFAULT_TEMPERATURE
from core.logger import logger

# Load environment variables
load_dotenv(override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    logger.warning("GROQ_API_KEY is not set in environment variables!")

def get_llm(temperature: float = DEFAULT_TEMPERATURE, model: str = DEFAULT_MODEL) -> ChatGroq:
    """
    Constructs and returns a ChatGroq LLM client.
    """
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY environment variable is required to initialize LLM.")
    return ChatGroq(
        model=model,
        temperature=temperature,
        api_key=GROQ_API_KEY,
    )

llm = get_llm()
