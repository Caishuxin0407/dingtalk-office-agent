import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("office_agent")
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = logging.FileHandler(
        LOG_DIR / "agent.log",
        encoding="utf-8",
    )
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )
    )
    logger.addHandler(file_handler)


def log_agent_request(
    *,
    employee: str | None,
    message: str,
    duration_ms: float,
    success: bool,
    error: str | None = None,
) -> None:
    logger.info(
        "event=agent_request employee=%s success=%s "
        "duration_ms=%.2f message_length=%d error=%s",
        employee or "unknown",
        success,
        duration_ms,
        len(message),
        error or "-",
    )

