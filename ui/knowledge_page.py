import os

import streamlit as st

from rag.knowledge_service import (
    get_index_status,
    list_knowledge_files,
    rebuild_knowledge_index,
)
from ui.styles import render_hero
from utils.config_handler import chroma_conf
from utils.path_tool import get_abs_path


def render() -> None:
    render_hero(
        "知识库管理",
        "上传文档、重建向量索引，为智能客服 RAG 检索提供资料",
    )

    status = get_index_status()
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("已索引文件数", status["indexed_files"])
    with c2:
        chunk = status["chunk_count"]
        st.metric("向量片段数", chunk if chunk is not None else "—")
    with c3:
        st.metric("待处理文档", len(list_knowledge_files()))

    st.markdown("#### 上传知识文档")
    st.caption(f"支持格式：{', '.join(chroma_conf['allow_knowledge_file_type'])}，保存至 data 目录")

    uploaded = st.file_uploader(
        "选择 txt 或 pdf 文件",
        type=chroma_conf["allow_knowledge_file_type"],
        accept_multiple_files=True,
    )
    if uploaded and st.button("保存上传文件", type="primary"):
        data_path = get_abs_path(chroma_conf["data_path"])
        os.makedirs(data_path, exist_ok=True)
        saved = []
        for f in uploaded:
            dest = os.path.join(data_path, f.name)
            with open(dest, "wb") as out:
                out.write(f.getbuffer())
            saved.append(f.name)
        st.success(f"已保存：{', '.join(saved)}")
        st.rerun()

    st.markdown("#### 文档列表")
    files = list_knowledge_files()
    if not files:
        st.info("data 目录暂无文档，请先上传。")
    else:
        st.dataframe(
            [{"文件名": f["name"], "大小(KB)": f["size_kb"]} for f in files],
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("#### 索引维护")
    st.caption(
        f"向量库路径：`{status['persist_directory']}` · "
        f"仅会索引新增或变更的文件（MD5 去重）"
    )

    if st.button("重建 / 增量索引", type="primary", use_container_width=True):
        with st.spinner("正在写入向量库，请稍候…"):
            result = rebuild_knowledge_index()
        if result["loaded"]:
            st.success(
                f"新入库 {result['loaded']} 个文件：{', '.join(result['files'])}"
            )
        else:
            st.info(
                f"无新文件入库（跳过 {result['skipped']}，失败 {result['failed']}）"
            )
        st.rerun()

    with st.expander("路径与配置"):
        st.json({
            "data_path": status["data_path"],
            "persist_directory": status["persist_directory"],
            "chunk_size": chroma_conf["chunk_size"],
            "retrieval_k": chroma_conf["k"],
        })
