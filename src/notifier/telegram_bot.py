"""
HoneySense — AI-driven Honeypot
Author & Maintainer: Ali Vaghefi — Backend & Network Security Engineer
Passionate about secure software, DevSecOps, and ethical development.
Arc.dev: https://arc.dev/@alivaghefi77ui?preview=1 | GitHub: https://github.com/alivaghefi77-ui
"""
import os
from typing import Optional


def send_alert(message: str) -> bool:
    """Send a Telegram alert. Supports dry-run via TELEGRAM_DRY_RUN=1.
    Returns True on success or dry-run, False on failure.
    """
    if os.getenv('TELEGRAM_DRY_RUN', '0') == '1':
        print(f"[DRY RUN] Telegram message:\n{message}")
        return True

    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    if not token or not chat_id:
        return False

    try:
        from telegram import Bot
        bot = Bot(token=token)
        bot.send_message(chat_id=chat_id, text=message)
        return True
    except Exception:
        return False
