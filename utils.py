import requests
import streamlit as st
from db import get_connection


def send_telegram(message):
    try:
        token = st.secrets["TELEGRAM_BOT_TOKEN"]
        chat_id = st.secrets["TELEGRAM_CHAT_ID"]

        url = f"https://api.telegram.org/bot{token}/sendMessage"

        requests.post(url, data={
            "chat_id": chat_id,
            "text": message
        })
    except Exception as e:
        print("Telegram error:", e)


def get_daily_status(user):
    conn = get_connection()
    cursor = conn.cursor()

    # Tasks
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE user=?", (user,))
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE completed=1 AND user=?", (user,))
    completed = cursor.fetchone()[0]

    progress = (completed / total * 100) if total > 0 else 0

    # Next Day Plan
    cursor.execute("SELECT task, focus FROM schedule WHERE user=?", (user,))
    plans = cursor.fetchall()

    conn.close()

    # Format message
    msg = f"📊 SSB DAILY STATUS\n\n"
    msg += f"👤 User: {user}\n"
    msg += f"📋 Total Tasks: {total}\n"
    msg += f"✅ Completed: {completed}\n"
    msg += f"📈 Progress: {progress:.1f}%\n\n"

    if plans:
        msg += "📅 Next Day Plan:\n"
        for p in plans:
            msg += f"• {p[0]} ({p[1]})\n"
    else:
        msg += "⚠️ No plan set for tomorrow\n"

    return msg


def send_daily_update(user):
    message = get_daily_status(user)
    send_telegram(message)