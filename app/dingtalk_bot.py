import json
import logging
import os
import dingtalk_stream
from dotenv import load_dotenv
from dingtalk_stream import AckMessage

from app.agent import ask_agent

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)
def get_employee_from_sender(
    sender_id: str | None,
) -> str | None:
    raw_user_map = os.getenv("DINGTALK_USER_MAP", "{}")

    try:
        user_map = json.loads(raw_user_map)
    except json.JSONDecodeError:
        logger.error("DINGTALK_USER_MAP 不是有效的 JSON 格式。")
        return None

    return user_map.get(sender_id)

class OfficeBotHandler(dingtalk_stream.ChatbotHandler):
    async def process(
        self,
        callback: dingtalk_stream.CallbackMessage,
    ):
        incoming_message = dingtalk_stream.ChatbotMessage.from_dict(
            callback.data
        )

        user_message = getattr(
            getattr(incoming_message, "text", None),
            "content",
            "",
        ).strip()
        logger.info(
            "收到钉钉消息 sender_id=%s sender_staff_id=%s sender_nick=%s",
            incoming_message.sender_id,
            incoming_message.sender_staff_id,
            incoming_message.sender_nick,
        )

        employee = get_employee_from_sender(
            incoming_message.sender_id
        )

        if not user_message:
            answer = "目前仅支持文本消息。"
        elif not employee:
            answer = (
                "当前钉钉账号尚未完成身份映射，"
                "无法查询或修改个人数据。请联系管理员。"
            )
        else:
            try:
                answer = ask_agent(
                    user_message,
                    employee=employee,
                )
            except Exception:
                logger.exception("Agent 调用失败")
                answer = "抱歉，当前服务暂时不可用，请稍后重试。"

        self.reply_text(answer, incoming_message)
        return AckMessage.STATUS_OK, "OK"


def main():
    client_id = os.getenv("DINGTALK_CLIENT_ID")
    client_secret = os.getenv("DINGTALK_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise RuntimeError(
            "未读取到钉钉凭证，请检查 .env 中的配置。"
        )

    credential = dingtalk_stream.Credential(
        client_id,
        client_secret,
    )

    client = dingtalk_stream.DingTalkStreamClient(credential)

    client.register_callback_handler(
        dingtalk_stream.chatbot.ChatbotMessage.TOPIC,
        OfficeBotHandler(),
    )

    logger.info("钉钉 Stream 机器人正在启动")
    client.start_forever()


if __name__ == "__main__":
    main()

