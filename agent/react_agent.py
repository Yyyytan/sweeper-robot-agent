from langchain.agents import create_agent
from langchain_core.messages import AIMessage

from model.factory import chat_model
from utils.prompt_loader import load_system_prompts
from utils.user_context import set_user_context, UserContext
from agent.tools.agent_tools import (
    rag_summarize,
    get_weather,
    get_user_location,
    get_user_id,
    get_current_month,
    fetch_external_data,
    fill_context_for_report,
)
from agent.tools.middleware import monitor_tool, log_before_model, report_prompt_switch


class ReactAgent:
    def __init__(self):
        self.agent = create_agent(
            model=chat_model,
            system_prompt=load_system_prompts(),
            tools=[
                rag_summarize,
                get_weather,
                get_user_location,
                get_user_id,
                get_current_month,
                fill_context_for_report,
                fetch_external_data,
            ],
            middleware=[monitor_tool, log_before_model, report_prompt_switch],
        )

    def execute_stream(
        self,
        messages: list[dict],
        user_context: UserContext | None = None,
    ):
        if user_context:
            set_user_context(
                user_context.user_id,
                user_context.city,
                user_context.month,
            )

        lc_messages = [
            {"role": m["role"], "content": m["content"]}
            for m in messages
            if m.get("role") in ("user", "assistant") and m.get("content")
        ]

        last_content = ""
        for chunk in self.agent.stream(
            {"messages": lc_messages},
            stream_mode="values",
            context={"report": False},
        ):
            msg = chunk["messages"][-1]
            if not isinstance(msg, AIMessage) or not msg.content:
                continue
            if getattr(msg, "tool_calls", None):
                continue

            text = msg.content if isinstance(msg.content, str) else str(msg.content)
            text = text.strip()
            if not text or text == last_content:
                continue

            if text.startswith(last_content):
                delta = text[len(last_content):]
            else:
                delta = text
            last_content = text
            if delta:
                yield delta


if __name__ == "__main__":
    agent = ReactAgent()
    history = [{"role": "user", "content": "给我生成我的使用报告"}]
    for chunk in agent.execute_stream(history):
        print(chunk, end="", flush=True)
