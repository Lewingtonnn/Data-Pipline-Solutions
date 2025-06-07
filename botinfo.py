from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os

token=os.getenv('TELEGRAM_TOKEN')
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Your chat ID is: {update.effective_chat.id}")

app = ApplicationBuilder().token(token).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
