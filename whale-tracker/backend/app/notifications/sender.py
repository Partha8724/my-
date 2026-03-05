import aiosmtplib
from email.message import EmailMessage
from telegram import Bot

from app.config import settings
from app.models.entities import Alert


def format_message(alert: Alert) -> str:
    return f"🚨 {alert.rule_name}\n{alert.message}"


async def send_telegram(alert: Alert) -> bool:
    if not settings.telegram_bot_token or not settings.telegram_chat_id:
        return False
    bot = Bot(token=settings.telegram_bot_token)
    await bot.send_message(chat_id=settings.telegram_chat_id, text=format_message(alert))
    return True


async def send_email(alert: Alert) -> bool:
    if not all([settings.smtp_host, settings.smtp_username, settings.smtp_password, settings.email_from, settings.email_to]):
        return False
    msg = EmailMessage()
    msg["From"] = settings.email_from
    msg["To"] = settings.email_to
    msg["Subject"] = f"Whale Tracker Alert: {alert.rule_name}"
    msg.set_content(format_message(alert))
    await aiosmtplib.send(
        msg,
        hostname=settings.smtp_host,
        port=settings.smtp_port,
        username=settings.smtp_username,
        password=settings.smtp_password,
        start_tls=True,
    )
    return True
