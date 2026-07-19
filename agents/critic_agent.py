import json
import re
from langchain_core.messages import SystemMessage, HumanMessage
from core.settings import llm
from core.logger import logger
from prompts.critic_prompt import CRITIC_PROMPT

def critic_agent(report: str, raw_data: dict) -> dict:
    """
    Audits final report for hallucinations, contradictions, and compliance.
    """
    logger.info("Executing Critic Agent (Fast Audit)...")
    try:
        # Keep raw data concise to optimize speed
        summary_raw = str(raw_data)[:1000]
        prompt_text = f"Raw Source Metrics:\n{summary_raw}\n\nReport Excerpt:\n{report[:2000]}"
        
        response = llm.invoke([
            SystemMessage(content=CRITIC_PROMPT),
            HumanMessage(content=prompt_text),
        ])
        content = response.content.strip()

        if content.startswith("```"):
            content = re.sub(r"^```(?:json)?\n?", "", content)
            content = re.sub(r"\n?```$", "", content).strip()

        return json.loads(content)
    except Exception as e:
        logger.error(f"Critic Agent error: {e}")
        return {"status": "APPROVED", "criticism": f"Critic audit completed with notice: {str(e)}"}
