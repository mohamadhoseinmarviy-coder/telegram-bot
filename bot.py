from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

# -------------------
# تنظیمات
TOKEN = "8276217887:AAFb7FZh5dmQNVybnUTUP0NOLUqrEZclWBE"
URL = os.getenv("RAILWAY_URL")  # این رو بعد از گرفتن دامنه تو Railway ست می‌کنیم
# -------------------

app_telegram = ApplicationBuilder().token(TOKEN).build()
flask_app = Flask(__name__)

# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من با Webhook روی Railway اجرا می‌شوم ✅")

# اکو کردن پیام کاربر
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"شما گفتید: {update.message.text}")

# هندلرها
app_telegram.add_handler(CommandHandler("start", start))
app_telegram.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# مسیر Webhook
@flask_app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), app_telegram.bot)
    app_telegram.update_queue.put(update)
    return "ok"

# مسیر ست کردن Webhook
@flask_app.route("/setwebhook", methods=["GET"])
def set_webhook():
    webhook_url = f"{URL}/{TOKEN}"
    app_telegram.bot.set_webhook(webhook_url)
    return f"Webhook set to {webhook_url}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    flask_app.run(host="0.0.0.0", port=port)
