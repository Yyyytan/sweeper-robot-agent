from datetime import datetime

import streamlit as st

from ui.session import (
    apply_user_context,
    clear_conversation,
    context_from_session,
    is_report_content,
    render_user_simulator_sidebar,
)
from ui.styles import render_hero


QUICK_PROMPTS = [
    "小户型适合哪些扫地机器人？",
    "机器人迷路了怎么办？",
    "帮我查一下我所在城市的天气，是否适合今天扫地",
    "给我生成我的使用报告",
]


def _render_sidebar_extras() -> None:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 快捷提问")
    for text in QUICK_PROMPTS:
        if st.sidebar.button(text, use_container_width=True, key=f"quick_{text[:12]}"):
            st.session_state.pending_prompt = text

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 对话管理")
    if st.sidebar.button("新对话", use_container_width=True, type="primary"):
        clear_conversation()
        st.rerun()

    msg_count = len(st.session_state.messages)
    st.sidebar.metric("本轮消息数", msg_count)

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 报告导出")
    if st.session_state.last_report:
        st.sidebar.download_button(
            label="下载 Markdown 报告",
            data=st.session_state.last_report,
            file_name=f"扫地机器人报告_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
            use_container_width=True,
        )
    else:
        st.sidebar.caption("生成使用报告后，可在此导出 Markdown 文件。")


def render() -> None:
    render_user_simulator_sidebar()
    _render_sidebar_extras()

    render_hero(
        "智扫通 · 智能客服",
        "支持多轮对话、知识检索、天气适配与个性化使用报告",
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            '<div class="stat-card"><strong>RAG</strong><span>向量知识库</span></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            '<div class="stat-card"><strong>ReAct</strong><span>工具自主调用</span></div>',
            unsafe_allow_html=True,
        )
    with col3:
        ctx = context_from_session(st.session_state)
        st.markdown(
            f'<div class="stat-card"><strong>{ctx.user_id}</strong>'
            f"<span>{ctx.city} · {ctx.month}</span></div>",
            unsafe_allow_html=True,
        )

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.session_state.pop("pending_prompt", None) or st.chat_input(
        "请输入您的问题，例如故障排查、选购建议、使用报告…"
    )

    if not prompt:
        return

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    apply_user_context()
    ctx = context_from_session(st.session_state)

    full_response = ""
    with st.chat_message("assistant"):
        with st.spinner("智能客服思考中…"):
            try:
                stream = st.session_state.agent.execute_stream(
                    st.session_state.messages,
                    user_context=ctx,
                )

                def accumulate(generator):
                    nonlocal full_response
                    for chunk in generator:
                        full_response += chunk
                        yield chunk

                st.write_stream(accumulate(stream))
            except Exception as e:
                full_response = f"抱歉，服务暂时出现问题：{e}"
                st.error(full_response)

    if full_response:
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )
        if is_report_content(full_response):
            st.session_state.last_report = full_response
            st.toast("报告已生成，可在侧边栏导出", icon="✅")
