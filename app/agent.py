import os
from time import perf_counter
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from app.tools.announcements import search_announcements
from app.tools.expenses import query_my_expense_claims
from app.tools.todos import complete_my_todo, create_my_todo, query_my_todos
from app.user_context import reset_current_employee, set_current_employee
from app.metrics import log_agent_request

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("未读取到 OPENAI_API_KEY，请检查 .env 文件。")

model = ChatOpenAI(
    model="gpt-5-mini",
    temperature=0,
)

agent = create_agent(
    model=model,
    tools=[
        search_announcements,
        query_my_expense_claims,
        query_my_todos,
        create_my_todo,
        complete_my_todo,
    ],
    system_prompt=(
        "你是企业办公助手。"
        "当用户询问公告、报销材料、会议或系统维护相关信息时，"
        "必须调用 search_announcements 工具查询后再回答。"
        "调用公告工具时，keyword 只能传入简短主题词，例如“报销”“会议”或“维护”，"
        "不要把用户的完整问题作为 keyword。"
        "当用户询问本人报销单、报销金额或报销状态时，"
        "当用户询问待办、任务或日程待办时，必须调用 query_my_todos 工具查询。 "
        "当用户明确要求新增、创建或添加待办时，必须调用 create_my_todo 工具；如未提供任务标题，应追问。 "
        "当用户明确要求完成、办结或标记某项待办为已完成时，必须调用 complete_my_todo 工具；如未提供准确任务标题，应追问。 "

        "必须调用 query_my_expense_claims 工具。"
        "该工具只能查询当前用户本人，不能回答其他员工的报销数据。"
        "只根据工具返回内容作答；查询不到时明确说明。"
        "不得把相对日期自行推算为具体日期；工具未提供的信息必须说明无法确认。"
        "不得声称可以执行未实现的操作，例如撤回报销单、修改数据或查看未提供的详情。"
    ),
)



def ask_agent(user_message: str, employee: str) -> str:
    token = set_current_employee(employee)
    started_at = perf_counter()
    success = False
    error = None

    try:
        result = agent.invoke(
            {"messages": [{"role": "user", "content": user_message}]}
        )
        success = True
        return result["messages"][-1].content
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        duration_ms = (perf_counter() - started_at) * 1000

        try:
            log_agent_request(
                employee=employee,
                message=user_message,
                duration_ms=duration_ms,
                success=success,
                error=error,
            )
        finally:
            reset_current_employee(token)

