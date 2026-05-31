import yaml
from utils.path_tool import get_abs_path


def load_yaml_config(file_name: str, encoding: str = "utf-8") -> dict:
    """
    通用YAML配置加载函数
    :param file_name: config目录下的yml文件名（如 rag.yml）
    :param encoding: 文件编码
    :return: 解析后的配置字典
    """
    config_path = get_abs_path(f"config/{file_name}")
    with open(config_path, "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


# 原有接口兼容保留（可选，不改动原有调用处）
def load_rag_config():
    return load_yaml_config("rag.yml")

def load_chroma_config():
    return load_yaml_config("chroma.yml")

def load_prompts_config():
    return load_yaml_config("prompts.yml")

def load_agent_config():
    return load_yaml_config("agent.yml")


rag_conf = load_rag_config()
chroma_conf = load_chroma_config()
prompts_conf = load_prompts_config()
agent_conf = load_agent_config()

if __name__ == '__main__':
    print(rag_conf["chat_model_name"])