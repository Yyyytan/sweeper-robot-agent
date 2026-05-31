"""知识库管理：单例向量服务、索引状态、文档加载。"""

import os
from functools import lru_cache

from utils.config_handler import chroma_conf
from utils.path_tool import get_abs_path
from rag.vector_store import VectorStoreService


@lru_cache(maxsize=1)
def get_vector_store_service() -> VectorStoreService:
    return VectorStoreService()


def list_knowledge_files() -> list[dict]:
    data_path = get_abs_path(chroma_conf["data_path"])
    allowed = tuple(chroma_conf["allow_knowledge_file_type"])
    if not os.path.isdir(data_path):
        os.makedirs(data_path, exist_ok=True)
        return []

    files = []
    for name in sorted(os.listdir(data_path)):
        if name.endswith(allowed):
            path = os.path.join(data_path, name)
            if os.path.isfile(path):
                files.append({
                    "name": name,
                    "path": path,
                    "size_kb": round(os.path.getsize(path) / 1024, 1),
                })
    return files


def get_index_status() -> dict:
    md5_path = get_abs_path(chroma_conf["md5_hex_store"])
    indexed = 0
    if os.path.exists(md5_path):
        with open(md5_path, "r", encoding="utf-8") as f:
            indexed = sum(1 for line in f if line.strip())

    vs = get_vector_store_service()
    try:
        count = vs.vector_store._collection.count()
    except Exception:
        count = None

    return {
        "indexed_files": indexed,
        "chunk_count": count,
        "data_path": get_abs_path(chroma_conf["data_path"]),
        "persist_directory": get_abs_path(chroma_conf["persist_directory"]),
    }


def rebuild_knowledge_index() -> dict:
    return get_vector_store_service().load_document()
