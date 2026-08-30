from app.user_context import (
    get_current_employee,
    reset_current_employee,
    set_current_employee,
)


def test_employee_context_is_set_and_reset():
    assert get_current_employee() is None

    token = set_current_employee("蔡淑欣")

    try:
        assert get_current_employee() == "蔡淑欣"
    finally:
        reset_current_employee(token)

    assert get_current_employee() is None


def test_nested_employee_context_restores_previous_value():
    outer_token = set_current_employee("蔡淑欣")

    try:
        assert get_current_employee() == "蔡淑欣"

        inner_token = set_current_employee("林晓")

        try:
            assert get_current_employee() == "林晓"
        finally:
            reset_current_employee(inner_token)

        assert get_current_employee() == "蔡淑欣"
    finally:
        reset_current_employee(outer_token)

    assert get_current_employee() is None

