from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from utils.config_handler import chroma_conf
from utils.path_tool import get_abs_path
from model.factory import embed_model
from utils.file_handler import (
    pdf_loader,
    txt_loader,
    listdir_with_allowed_type,
    get_file_md5_hex,
)
from utils.logger_handler import logger
import os


def _load_md5_set() -> set[str]:
    md5_path = get_abs_path(chroma_conf["md5_hex_store"])
    if not os.path.exists(md5_path):
        open(md5_path, "w", encoding="utf-8").close()
        return set()
    with open(md5_path, "r", encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}


def _save_md5_hex(md5_hex: str, known: set[str]) -> None:
    if md5_hex in known:
        return
    md5_path = get_abs_path(chroma_conf["md5_hex_store"])
    with open(md5_path, "a", encoding="utf-8") as f:
        f.write(md5_hex + "\n")
    known.add(md5_hex)


class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],
            embedding_function=embed_model,
            persist_directory=get_abs_path(chroma_conf["persist_directory"]),
        )

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            separators=chroma_conf["separators"],
            length_function=len,
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})

    def load_document(self) -> dict:
        """
        从数据文件夹读取文件并写入向量库。
        :return: 加载统计信息
        """
        stats = {"loaded": 0, "skipped": 0, "failed": 0, "files": []}
        known_md5 = _load_md5_set()

        def get_file_document(read_path: str):
            if read_path.endswith(".txt"):
                return txt_loader(read_path)
            if read_path.endswith(".pdf"):
                return pdf_loader(read_path)
            return []

        allowed_files_path = listdir_with_allowed_type(
            get_abs_path(chroma_conf["data_path"]),
            tuple(chroma_conf["allow_knowledge_file_type"]),
        )

        for path in allowed_files_path:
            md5_hex = get_file_md5_hex(path)
            if not md5_hex:
                stats["failed"] += 1
                continue

            if md5_hex in known_md5:
                logger.info(f"[加载知识库] {path} 已存在，跳过")
                stats["skipped"] += 1
                continue

            try:
                document: list[Document] = get_file_document(path)
                if not document:
                    logger.warning(f"[加载知识库] {path} 无有效文本，跳过")
                    stats["skipped"] += 1
                    continue

                split_document: list[Document] = self.spliter.split_documents(document)
                if not split_document:
                    logger.warning(f"[加载知识库] {path} 分片后无内容，跳过")
                    stats["skipped"] += 1
                    continue

                self.vector_store.add_documents(split_document)
                _save_md5_hex(md5_hex, known_md5)
                stats["loaded"] += 1
                stats["files"].append(os.path.basename(path))
                logger.info(f"[加载知识库] {path} 加载成功")
            except Exception as e:
                logger.error(f"[加载知识库] {path} 加载失败：{e}", exc_info=True)
                stats["failed"] += 1

        return stats


if __name__ == "__main__":
    vs = VectorStoreService()
    print(vs.load_document())
    retriever = vs.get_retriever()
    res = retriever.invoke("迷路")
    for r in res:
        print(r.page_content)
        print("-" * 20)
