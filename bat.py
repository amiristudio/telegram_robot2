import os
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext

# خواندن توکن و آیدی کانال از محیط
TOKEN = os.getenv('TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

# تابع پاسخ به دستور /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text('سلام! من یه ربات هستم.')

# تابع ارسال پیام به کانال
def send_to_channel(context: CallbackContext, message: str):
    bot = context.bot
    bot.send_message(chat_id=CHANNEL_ID, text=message)

# تابع تست ارسال پیام به کانال با دستور /send
def send_message_to_channel(update: Update, context: CallbackContext):
    message = " ".join(context.args)
    if not message:
        update.message.reply_text("لطفاً متن پیام رو وارد کنید.")
        return
    
    send_to_channel(context, message)
    update.message.reply_text("پیام با موفقیت به کانال ارسال شد.")

# تنظیمات اصلی ربات
def main():
    updater = Updater(TOKEN)
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("send", send_message_to_channel))
    updater.start_polling()
    print("ربات فعال شد...")
    updater.idle()

if __name__ == '__main__':
    main()