import os
import shutil
import tempfile
from pathlib import Path

import pytest

_TEST_DIR = Path(tempfile.mkdtemp(prefix="dingtalk-office-agent-tests-"))
_TEST_DB = _TEST_DIR / "office_agent_test.db"

# 必须在导入 app.database 前设置，确保测试使用独立临时数据库。
os.environ["DATABASE_URL"] = f"sqlite:///{_TEST_DB}"


@pytest.fixture(autouse=True)
def reset_database():
    from app.database import Base, engine, init_db

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    init_db()

    yield

    Base.metadata.drop_all(engine)


def pytest_sessionfinish(session, exitstatus):
    shutil.rmtree(_TEST_DIR, ignore_errors=True)

