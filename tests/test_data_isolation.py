from app.tools.expenses import query_my_expense_claims
from app.tools.todos import query_my_todos
from app.user_context import (
    reset_current_employee,
    set_current_employee,
)


def test_employee_only_sees_own_todos():
    token = set_current_employee("蔡淑欣")

    try:
        result = query_my_todos.invoke({})
    finally:
        reset_current_employee(token)

    assert "确认下周例会参会名单" in result
    assert "更新采购预算表" not in result


def test_employee_only_sees_own_expense_claims():
    token = set_current_employee("蔡淑欣")

    try:
        result = query_my_expense_claims.invoke({})
    finally:
        reset_current_employee(token)

    assert "差旅报销" in result
    assert "采购报销" not in result


