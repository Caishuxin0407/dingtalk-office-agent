from langchain_core.tools import tool
from app.user_context import get_current_employee
from app.database import query_expense_claims



@tool
def query_my_expense_claims(status: str = "") -> str:
    """查询当前登录用户本人的报销单。

    可按状态筛选，例如“审核中”“待补材料”“已通过”。
    仅能查询当前用户本人，不能查询其他员工。
    """
    normalized_status = status.strip() or None
    employee = get_current_employee()

    if not employee:
        return "当前请求未识别到已授权员工身份，无法查询报销记录。"

    items = query_expense_claims(
        employee=employee,
        status=normalized_status,
    )

    if not items:
        return "未找到符合条件的本人报销记录。"

    lines = []
    for item in items:
        lines.append(
            f"报销类型：{item['claim_type']}\n"
            f"金额：{item['amount']:.2f} 元\n"
            f"状态：{item['status']}\n"
            f"提交时间：{item['submitted_at']}"
        )

    return "\n\n".join(lines)

