import streamlit as st

from agent.react_agent import ReactAgent
from utils.user_context import (
    DEFAULT_USER_ID,
    DEFAULT_CITY,
    DEFAULT_MONTH,
    USER_IDS,
    CITIES,
    MONTHS,
    context_from_session,
    set_user_context,
)

REPORT_MARKERS = ("使用情况报告", "保养建议", "扫地机器人使用情况报告")


def init_session() -> None:
    if "agent" not in st.session_state:
        st.session_state.agent = ReactAgent()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 兼容旧版 session key
    if "message" in st.session_state and st.session_state.message:
        st.session_state.messages = st.session_state.pop("message")

    if "last_report" not in st.session_state:
        st.session_state.last_report = None

    if "sim_user_id" not in st.session_state:
        st.session_state.sim_user_id = DEFAULT_USER_ID
    if "sim_city" not in st.session_state:
        st.session_state.sim_city = DEFAULT_CITY
    if "sim_month" not in st.session_state:
        st.session_state.sim_month = DEFAULT_MONTH


def clear_conversation() -> None:
    st.session_state.messages = []
    st.session_state.last_report = None


def apply_user_context() -> None:
    ctx = context_from_session(st.session_state)
    set_user_context(ctx.user_id, ctx.city, ctx.month)


def is_report_content(text: str) -> bool:
    return any(marker in text for marker in REPORT_MARKERS)


def render_user_simulator_sidebar() -> None:
    st.sidebar.markdown("### 用户身份模拟")
    st.session_state.sim_user_id = st.sidebar.selectbox(
        "用户 ID",
        USER_IDS,
        index=USER_IDS.index(st.session_state.sim_user_id)
        if st.session_state.sim_user_id in USER_IDS
        else 0,
    )
    st.session_state.sim_city = st.sidebar.selectbox(
        "所在城市",
        CITIES,
        index=CITIES.index(st.session_state.sim_city)
        if st.session_state.sim_city in CITIES
        else 0,
    )
    st.session_state.sim_month = st.sidebar.selectbox(
        "报告月份",
        MONTHS,
        index=MONTHS.index(st.session_state.sim_month)
        if st.session_state.sim_month in MONTHS
        else 5,
    )
    st.sidebar.caption("工具 get_user_id / get_user_location / get_current_month 将使用以上模拟身份。")
