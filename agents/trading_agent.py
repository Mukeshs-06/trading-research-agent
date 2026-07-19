from langchain_core.messages import (
    HumanMessage,
    ToolMessage,
    SystemMessage,
)
from prompts.system_prompt import SYSTEM_PROMPT
from config import llm

from tools.registry import TOOLS

tools = TOOLS

tool_map = {
    tool.name: tool
    for tool in TOOLS
}

llm_with_tools = llm.bind_tools(tools)


def run_agent(user_request: str):

    messages = [
    SystemMessage(content=SYSTEM_PROMPT),
    HumanMessage(content=user_request),
    ]

    while True:

        response = llm_with_tools.invoke(messages)

        messages.append(response)

        if not response.tool_calls:
            return response.content

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]

            tool_args = tool_call["args"]

            tool = tool_map[tool_name]

            result = tool.invoke(tool_args)

            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"],
                )
            )