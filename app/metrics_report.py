import re
from pathlib import Path

LOG_FILE = Path("logs/agent.log")

PATTERN = re.compile(
    r"success=(True|False) duration_ms=([0-9.]+)"
)


def main() -> None:
    if not LOG_FILE.exists():
        print("暂未找到请求日志。请先运行一次 Agent 或钉钉机器人。")
        return

    records = []

    for line in LOG_FILE.read_text(encoding="utf-8").splitlines():
        match = PATTERN.search(line)

        if match:
            records.append(
                {
                    "success": match.group(1) == "True",
                    "duration_ms": float(match.group(2)),
                }
            )

    if not records:
        print("日志中暂未找到可统计的 Agent 请求记录。")
        return

    total = len(records)
    success_count = sum(item["success"] for item in records)
    success_rate = success_count / total * 100
    average_duration = sum(
        item["duration_ms"] for item in records
    ) / total

    print(f"请求总数：{total}")
    print(f"成功请求：{success_count}")
    print(f"成功率：{success_rate:.2f}%")
    print(f"平均响应时间：{average_duration:.2f} ms")


if __name__ == "__main__":
    main()

