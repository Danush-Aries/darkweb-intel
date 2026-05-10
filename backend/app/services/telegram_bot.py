from telegram import Bot
from telegram.ext import Application
from ..core.config import settings
import asyncio

async def send_alert(message: str):
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=settings.TELEGRAM_CHAT_ID, text=message)

async def test_bot():
    await send_alert("DarkWeb Intel: System test message successful.")
