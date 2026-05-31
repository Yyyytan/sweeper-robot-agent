from langchain.agents import AgentState
from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest
from langchain.tools.tool_node import ToolCallRequest
from typing import Callable
from utils.prompt_loader import load_system_prompts,load_report_prompts
from langchain_core.messages import ToolMessage
from langgraph.runtime import Runtime
from langgraph.types import Command
from utils.logger_handler import logger

MAX_TOOL_CALLS = 5


@wrap_tool_call
def monitor_tool(
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], ToolMessage | Command],
) -> ToolMessage | Command:
    runtime = request.runtime
    count = runtime.context.get("tool_call_count", 0)
    if count >= MAX_TOOL_CALLS:
        logger.warning("[tool monitor] 已达工具调用上限")
        return ToolMessage(
            content="已达到工具调用次数上限，请基于已有信息回答用户。",
            tool_call_id=request.tool_call["id"],
        )

    runtime.context["tool_call_count"] = count + 1
    logger.info(f"[tool monitor]执行工具：{request.tool_call['name']}")
    logger.info(f"[tool monitor]传入参数：{request.tool_call['args']}")

    try:
        result = handler(request)
        logger.info(f"[tool monitor]工具{request.tool_call['name']}调用成功")

        if request.tool_call['name'] == "fill_context_for_report":
            request.runtime.context["report"] = True

        return result
    except Exception as e:
        logger.error(f"工具{request.tool_call['name']}调用失败，原因：{str(e)}")
        raise e


@before_model           #在模型执行前输出日志
def log_before_model(
        state: AgentState,      #整个agent智能体中的状态记录
        runtime: Runtime,       #记录了整个执行过程中的上下文信息
):
    msg_list = state["messages"]
    logger.info(f"[log_before_model]即将调用模型，带有{len(msg_list)}条消息。")

    # 先判断消息列表非空再取值
    if msg_list:
        last_msg = msg_list[-1]
        logger.debug(f"[log_before_model]{type(last_msg).__name__} | {last_msg.content}")
    else:
        logger.debug("[log_before_model] 消息列表为空，无最新消息")

    return None


@dynamic_prompt         #每一次生成提示词之前，调用此函数
def report_prompt_switch(request: ModelRequest):       #动态切换提示词
    is_report = request.runtime.context.get("report", False)
    if is_report:       #根据生成场景，返回报告生成提示词内容
        return load_report_prompts()

    return load_system_prompts()

