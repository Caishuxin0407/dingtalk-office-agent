from contextvars import ContextVar, Token


_current_employee: ContextVar[str | None] = ContextVar(
    "current_employee",
    default=None,
)


def set_current_employee(employee: str) -> Token:
    return _current_employee.set(employee)


def reset_current_employee(token: Token) -> None:
    _current_employee.reset(token)


def get_current_employee() -> str | None:
    return _current_employee.get()


