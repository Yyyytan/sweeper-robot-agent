"""Streamlit 会话中的用户身份上下文，供 Agent 工具读取。"""

from contextvars import ContextVar
from dataclasses import dataclass

DEFAULT_USER_ID = "1001"
DEFAULT_CITY = "深圳"
DEFAULT_MONTH = "2025-06"

USER_IDS = [f"{i}" for i in range(1001, 1011)]
CITIES = ["深圳", "合肥", "杭州", "北京", "上海", "广州"]
MONTHS = [
    "2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06",
    "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12",
]


@dataclass(frozen=True)
class UserContext:
    user_id: str = DEFAULT_USER_ID
    city: str = DEFAULT_CITY
    month: str = DEFAULT_MONTH


_user_ctx_var: ContextVar[UserContext] = ContextVar(
    "user_ctx", default=UserContext()
)


def set_user_context(user_id: str, city: str, month: str) -> None:
    _user_ctx_var.set(UserContext(user_id=user_id, city=city, month=month))


def get_user_context() -> UserContext:
    return _user_ctx_var.get()


def context_from_session(session: dict) -> UserContext:
    return UserContext(
        user_id=session.get("sim_user_id", DEFAULT_USER_ID),
        city=session.get("sim_city", DEFAULT_CITY),
        month=session.get("sim_month", DEFAULT_MONTH),
    )
