from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

DATABASE_URL = "sqlite:///./office_agent.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)


class Base(DeclarativeBase):
    pass


class Announcement(Base):
    __tablename__ = "announcements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    publish_time: Mapped[datetime] = mapped_column(DateTime)


class ExpenseClaim(Base):
    __tablename__ = "expense_claims"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    employee: Mapped[str] = mapped_column(String(100))
    claim_type: Mapped[str] = mapped_column(String(100))
    amount: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(50))
    submitted_at: Mapped[datetime] = mapped_column(DateTime)

class TodoItem(Base):
    __tablename__ = "todo_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner: Mapped[str] = mapped_column(String(100))
    title: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(20))
    due_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime)

def init_db():
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        existing_announcement = session.scalar(
            select(Announcement.id).limit(1)
        )

        if existing_announcement is None:
            session.add_all(
                [
                    Announcement(
                        title="报销材料提交提醒",
                        content="请于本周五前提交差旅与业务报销材料。",
                        publish_time=datetime(2026, 8, 24, 9, 0),
                    ),
                    Announcement(
                        title="周例会通知",
                        content="本周例会将于周三下午 3 点在 3A 会议室举行。",
                        publish_time=datetime(2026, 8, 25, 10, 30),
                    ),
                    Announcement(
                        title="系统维护公告",
                        content="报销系统将于周六 22:00 至周日 02:00 维护。",
                        publish_time=datetime(2026, 8, 26, 14, 0),
                    ),
                ]
            )

        existing_claim = session.scalar(
            select(ExpenseClaim.id).limit(1)
        )

        if existing_claim is None:
            session.add_all(
                [
                    ExpenseClaim(
                        employee="蔡淑欣",
                        claim_type="差旅报销",
                        amount=1280.50,
                        status="审核中",
                        submitted_at=datetime(2026, 8, 25, 16, 20),
                    ),
                    ExpenseClaim(
                        employee="蔡淑欣",
                        claim_type="业务招待",
                        amount=450.00,
                        status="待补材料",
                        submitted_at=datetime(2026, 8, 22, 11, 0),
                    ),
                    ExpenseClaim(
                        employee="林晓",
                        claim_type="采购报销",
                        amount=760.00,
                        status="已通过",
                        submitted_at=datetime(2026, 8, 21, 9, 30),
                    ),
                ]
            )
        existing_todo = session.scalar(
            select(TodoItem.id).limit(1)
        )


        if existing_todo is None:
            session.add_all(
                [
                    TodoItem(
                        owner="蔡淑欣",
                        title="整理本周项目周报",
                        status="待办",
                        due_at=datetime(2026, 8, 30, 18, 0),
                        created_at=datetime(2026, 8, 29, 16, 0),
                    ),
                    TodoItem(
                        owner="蔡淑欣",
                        title="确认下周例会参会名单",
                        status="待办",
                        due_at=datetime(2026, 9, 1, 10, 0),
                        created_at=datetime(2026, 8, 29, 16, 5),
                    ),
                    TodoItem(
                        owner="林晓",
                        title="更新采购预算表",
                        status="已完成",
                        due_at=datetime(2026, 8, 28, 17, 0),
                        created_at=datetime(2026, 8, 27, 9, 0),
                    ),
                ]
            )

        session.commit()


def query_announcements(keyword: str | None = None) -> list[dict]:
    statement = select(Announcement).order_by(
        Announcement.publish_time.desc()
    )

    if keyword:
        statement = statement.where(
            Announcement.title.contains(keyword)
            | Announcement.content.contains(keyword)
        )

    with Session(engine) as session:
        items = session.scalars(statement).all()

    return [
        {
            "id": item.id,
            "title": item.title,
            "content": item.content,
            "publish_time": item.publish_time.isoformat(),
        }
        for item in items
    ]


def query_expense_claims(
    employee: str | None = None,
    status: str | None = None,
) -> list[dict]:
    statement = select(ExpenseClaim).order_by(
        ExpenseClaim.submitted_at.desc()
    )

    if employee:
        statement = statement.where(ExpenseClaim.employee == employee)

    if status:
        statement = statement.where(ExpenseClaim.status == status)

    with Session(engine) as session:
        items = session.scalars(statement).all()

    return [
        {
            "id": item.id,
            "employee": item.employee,
            "claim_type": item.claim_type,
            "amount": item.amount,
            "status": item.status,
            "submitted_at": item.submitted_at.isoformat(),
        }
        for item in items
    ]

def query_todos(
    owner: str | None = None,
    status: str | None = None,
) -> list[dict]:
    statement = select(TodoItem).order_by(
        TodoItem.created_at.desc()
    )

    if owner:
        statement = statement.where(TodoItem.owner == owner)

    if status:
        statement = statement.where(TodoItem.status == status)

    with Session(engine) as session:
        items = session.scalars(statement).all()

    return [
        {
            "id": item.id,
            "owner": item.owner,
            "title": item.title,
            "status": item.status,
            "due_at": (
                item.due_at.isoformat()
                if item.due_at
                else None
            ),
            "created_at": item.created_at.isoformat(),
        }
        for item in items
    ]

def create_todo(
    owner: str,
    title: str,
    due_at: datetime | None = None,
) -> dict:
    todo = TodoItem(
        owner=owner,
        title=title,
        status="待办",
        due_at=due_at,
        created_at=datetime.now(),
    )

    with Session(engine) as session:
        session.add(todo)
        session.commit()
        session.refresh(todo)

        return {
            "id": todo.id,
            "owner": todo.owner,
            "title": todo.title,
            "status": todo.status,
            "due_at": (
                todo.due_at.isoformat()
                if todo.due_at
                else None
            ),
            "created_at": todo.created_at.isoformat(),
        }

def complete_todo(
    owner: str,
    title: str,
) -> dict | None:
    with Session(engine) as session:
        todo = session.scalar(
            select(TodoItem)
            .where(TodoItem.owner == owner)
            .where(TodoItem.title == title)
            .order_by(TodoItem.id.desc())
        )

        if todo is None:
            return None

        todo.status = "已完成"
        session.commit()
        session.refresh(todo)

        return {
            "id": todo.id,
            "owner": todo.owner,
            "title": todo.title,
            "status": todo.status,
            "due_at": (
                todo.due_at.isoformat()
                if todo.due_at
                else None
            ),
            "created_at": todo.created_at.isoformat(),
        }

