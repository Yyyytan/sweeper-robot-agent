import streamlit as st

from ui.styles import inject_styles
from ui.session import init_session
from ui import chat_page, knowledge_page

st.set_page_config(
    page_title="智扫通智能客服",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_styles()
init_session()

with st.sidebar:
    st.markdown("## 智扫通")
    st.caption("扫地机器人智能客服系统")
    page = st.radio(
        "功能导航",
        ["智能客服", "知识库管理"],
        label_visibility="collapsed",
    )

if page == "智能客服":
    chat_page.render()
else:
    knowledge_page.render()
