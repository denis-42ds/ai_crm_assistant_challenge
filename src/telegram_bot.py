import os
import re
import json
import logging
import requests
from telegram import Update
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://fastapi-app:8000")
RESERVED_CHARS = r"([_*\[\]()~`>#+-=|{}.!])"

def escape_markdown(text: str) -> str:
    """Escapes Telegram's MarkdownV2 reserved characters."""
    return re.sub(RESERVED_CHARS, r'\\\1', text)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я ваш CRM-ассистент. Отправьте мне текст заметки по сделке, и я оценю риски."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    note_text = update.message.text
    
    try:
        response = requests.post(f"{FASTAPI_URL}/risk-assessment", json={"text": note_text})
        response.raise_for_status()

        try:
            risk_data = response.json()
            is_at_risk = risk_data.get("is_at_risk", False)
            reason = risk_data.get("reason", "нет")
            
            escaped_reason = escape_markdown(reason)

            if is_at_risk:
                reply_text = f"🚨 **ВНИМАНИЕ, РИСК\!** 🚨\n\n**Причина:** {escaped_reason}"
            else:
                reply_text = "✅ **Сделка без видимых рисков\.**"

            await update.message.reply_markdown_v2(reply_text)

        except json.JSONDecodeError:
            logging.error(f"Failed to decode JSON from FastAPI. Status: {response.status_code}, Response: {response.text}")
            await update.message.reply_text(
                "Ошибка: Сервис вернул невалидный ответ. Проверьте логи FastAPI-приложения."
            )

    except requests.exceptions.RequestException as e:
        logging.error(f"Error calling FastAPI service: {e}")
        await update.message.reply_text("Произошла ошибка при обработке запроса. Пожалуйста, попробуйте еще раз.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        await update.message.reply_text("Произошла непредвиденная ошибка.")

def main():
    if not TELEGRAM_BOT_TOKEN:
        logging.error("TELEGRAM_BOT_TOKEN not found in environment variables.")
        return

    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    application.run_polling(poll_interval=1.0)
    
if __name__ == '__main__':
    main()
