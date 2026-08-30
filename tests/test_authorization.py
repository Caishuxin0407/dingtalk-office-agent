import pytest

from app.tools.expenses import query_my_expense_claims
from app.tools.todos import query_my_todos
from app.user_context import get_current_employee


def test_todo_query_requires_employee_identity():
    assert get_current_employee() is None

    with pytest.raises(
        RuntimeError,
        match="未识别到已授权员工身份",
    ):
        query_my_todos.invoke({})


def test_expense_query_requires_employee_identity():
    assert get_current_employee() is None

    result = query_my_expense_claims.invoke(
        {"status": "审核中"}
    )

    assert "未识别到已授权员工身份" in result

