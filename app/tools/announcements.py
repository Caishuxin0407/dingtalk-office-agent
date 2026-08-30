from langchain_core.tools import tool

from app.database import query_announcements


@tool
def search_announcements(keyword: str = "") -> str:
    """Search internal announcements by keyword. Use this tool when a user asks about notices, policies, reimbursements, meetings, or maintenance."""

    normalized_keyword = keyword.strip() or None
    items = query_announcements(normalized_keyword)

    if not items:
        return "No matching announcements were found."

    lines = []

    for item in items:
        lines.append(
            f"Title: {item['title']}\n"
            f"Content: {item['content']}\n"
            f"Published: {item['publish_time']}"
        )

    return "\n\n".join(lines)

