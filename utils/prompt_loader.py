from functools import lru_cache

from utils.config_handler import prompts_conf
from utils.path_tool import get_abs_path
from utils.logger_handler import logger


def _read_prompt_file(path_key: str, log_name: str) -> str:
    try:
        prompt_path = get_abs_path(prompts_conf[path_key])
    except KeyError as e:
        logger.error(f"[{log_name}]在 yaml 配置中没有 {path_key} 配置项")
        raise e

    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"[{log_name}]解析提示词出错, {str(e)}")
        raise e


@lru_cache(maxsize=1)
def load_system_prompts() -> str:
    return _read_prompt_file("main_prompt_path", "load_system_prompts")


@lru_cache(maxsize=1)
def load_rag_prompts() -> str:
    return _read_prompt_file("rag_summarize_prompt_path", "load_rag_prompts")


@lru_cache(maxsize=1)
def load_report_prompts() -> str:
    return _read_prompt_file("report_prompt_path", "load_report_prompts")
