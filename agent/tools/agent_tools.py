import json
import os

from langchain_core.tools import tool

from rag.rag_service import RagSummarizeService
from utils.config_handler import agent_conf
from utils.logger_handler import logger
from utils.path_tool import get_abs_path
from utils.user_context import get_user_context

rag = RagSummarizeService()

external_data: dict = {}
_external_data_loaded = False


def _ensure_external_data() -> None:
    global _external_data_loaded
    if _external_data_loaded:
        return

    external_data_path = get_abs_path(agent_conf["external_data_path"])
    if not os.path.exists(external_data_path):
        raise FileNotFoundError(f"外部数据文件 {external_data_path} 不存在")

    with open(external_data_path, "r", encoding="utf-8") as f:
        for line in f.readlines()[1:]:
            arr: list[str] = line.strip().split(",")
            if len(arr) < 6:
                continue

            user_id = arr[0].replace('"', "")
            feature = arr[1].replace('"', "")
            efficiency = arr[2].replace('"', "")
            consumables = arr[3].replace('"', "")
            comparison = arr[4].replace('"', "")
            time = arr[5].replace('"', "")

            if user_id not in external_data:
                external_data[user_id] = {}

            external_data[user_id][time] = {
                "特征": feature,
                "效率": efficiency,
                "耗材": consumables,
                "对比": comparison,
            }

    _external_data_loaded = True


@tool(description="从向量存储中检索参考资料")
def rag_summarize(query: str) -> str:
    return rag.rag_summarize(query)


@tool(description="获取指定城市的天气，以消息字符串的形式返回")
def get_weather(city: str) -> str:
    return (
        f"城市{city}天气为晴天，气温26摄氏度，空气湿度50%，"
        f"南风1级，AQI21，最近6小时降雨概率极低"
    )


@tool(description="获取用户所在城市的名称，以纯字符串形式返回")
def get_user_location() -> str:
    return get_user_context().city


@tool(description="获取用户的ID，以纯字符串形式返回")
def get_user_id() -> str:
    return get_user_context().user_id


@tool(description="获取当前月份，以纯字符串形式返回")
def get_current_month() -> str:
    return get_user_context().month


@tool(
    description=(
        "从外部系统中获取指定用户在指定月份的使用记录，"
        "以纯字符串形式返回，如果未检索到返回空字符串"
    )
)
def fetch_external_data(user_id: str, month: str) -> str:
    _ensure_external_data()

    try:
        record = external_data[user_id][month]
        return json.dumps(record, ensure_ascii=False)
    except KeyError:
        logger.warning(
            f"[fetch_external_data] 未能检索到用户 {user_id} 在 {month} 的使用记录"
        )
        return ""


@tool(
    description=(
        "无入参，调用后触发中间件自动为报告生成的场景动态注入上下文信息，"
        "为后续提示词切换提供上下文信息"
    )
)
def fill_context_for_report() -> str:
    return "fill_context_for_report已调用"
