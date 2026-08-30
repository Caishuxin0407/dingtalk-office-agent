from datetime import datetime

from langchain_core.tools import tool

from app.database import complete_todo, create_todo, query_todos

from app.user_context import get_current_employee
def current_employee() -> str:
    employee = get_current_employee()

    if not employee:
        raise RuntimeError("当前请求未识别到已授权员工身份。")

    return employee


@tool
def query_my_todos(status: str = "") -> str:
    """查询当前用户的待办任务。status 可传：待办、已完成。"""
    items = query_todos(
        owner=current_employee(),
        status=status or None,
    )

    if not items:
        return "没有找到符合条件的待办任务。"

    lines = ["查询到以下待办："]
    for item in items:
        due_at = item["due_at"] or "未设置截止时间"
        lines.append(
            f"- {item['title']}｜状态：{item['status']}｜截止：{due_at}"
        )

    return "\n".join(lines)


@tool
def create_my_todo(title: str, due_at: str = "") -> str:
    """为当前用户创建待办。due_at 使用 ISO 格式，例如 2026-09-01T10:00:00。"""
    parsed_due_at = None

    if due_at:
        try:
            parsed_due_at = datetime.fromisoformat(due_at)
        except ValueError:
            return (
                "截止时间格式不正确，请使用 "
                "2026-09-01T10:00:00 这种格式。"
            )

    item = create_todo(
        owner=current_employee(),
        title=title,
        due_at=parsed_due_at,
    )

    due_text = item["due_at"] or "未设置截止时间"
    return (
        f"已创建待办：{item['title']}；"
        f"状态：{item['status']}；截止：{due_text}。"
    )

@tool
def complete_my_todo(title: str) -> str:
    """将当前用户指定标题的待办标记为已完成。title 必须是待办标题。"""
    item = complete_todo(
        owner=current_employee(),
        title=title,
    )

    if item is None:
        return f"没有找到标题为“{title}”的待办，未做任何修改。"


    return f"已完成待办：{item['title']}。"

