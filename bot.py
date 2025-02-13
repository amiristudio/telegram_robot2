from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import nest_asyncio
from datetime import datetime
import logging

# فعال‌سازی nest_asyncio برای حل مشکل حلقه رویداد
nest_asyncio.apply()

# تنظیمات اولیه
TOKEN = "7433323934:AAEabuR3x9vybKKuNNvJosXFgZl29-yVSfU"  # توکن ربات شما
CHANNEL_ID = -1002329362562  # آیدی کانال شما

# لاگ‌گیری
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    user_name = update.message.from_user.first_name
    
    # پیام خوش‌آمدگویی
    welcome_message = (
        f"سلام {user_name}! 👋\n\n"
        "لحظات زیبای شما برای ما ارزشمندترین خاطره‌ها هستند، و حالا وقتشه که عکس‌ها و ویدیوهای خاصتون رو ببینید.\n\n"
        "اینجا می‌تونید با وارد کردن تاریخ عکاسی خود، فایل‌های مربوط به اون تاریخ رو دریافت کنید.\n"
        "فقط کافیه تاریخ عکاسی‌تون رو به صورت `MM.DD` وارد کنید (مثل 8.01 برای اول ماه هشتم).\n\n"
        "اگر سوالی داشتید، می‌تونید با پشتیبانی ما در تماس باشید."
    )
    
    await update.message.reply_text(welcome_message)

# دریافت پیام‌های متنی
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message or not update.message.text:
            logger.warning("پیام دریافتی نامعتبر است.")
            return
        
        # بررسی اینکه پیام فقط شامل متن باشه (فایل یا عکس نباشه)
        if update.message.document or update.message.photo or update.message.video:
            await update.message.reply_text("لطفاً فقط تاریخ عکاسی خود را به صورت متن وارد کنید.")
            return

        user_message = update.message.text.strip()

        # بررسی صحت تاریخ ورودی
        if len(user_message) < 4 or '.' not in user_message:
            await update.message.reply_text("فرمت تاریخ نادرست است. لطفاً تاریخ را به صورت MM.DD وارد کنید.")
            return

        try:
            month, day = map(int, user_message.split('.'))
            if not (1 <= month <= 12 and 1 <= day <= 31):
                raise ValueError("ماه یا روز نامعتبر است.")
            # بررسی تعداد روزهای ماه
            try:
                datetime(year=2023, month=month, day=day)
            except ValueError:
                raise ValueError("تاریخ وارد شده نامعتبر است.")
        except ValueError as e:
            await update.message.reply_text(str(e))
            return

        # نام فایل بر اساس تاریخ وارد شده
        file_name = f"{month:02d}.{day:02d}.zip"

        # جستجو در تاریخ در کانال (دریافت پیام‌ها از کانال)
        try:
            messages = await context.bot.get_chat_history(chat_id=CHANNEL_ID, limit=50)
            file_found = False
            for message in messages:
                if message.document and message.document.file_name == file_name:
                    await context.bot.copy_message(
                        chat_id=update.message.chat_id,
                        from_chat_id=CHANNEL_ID,
                        message_id=message.message_id,
                        caption="امیدوارم لحظات شیرینتون رو با عشق ثبت کرده باشیم، خیلی خوشحال می‌شیم اگر احساستون رو با ما در واتس‌آپ به اشتراک بزارید و با امتیازگیری عکس و فیلم‌های رایگان دریافت کنید.\n\n"
                                "برای دیدن فایل‌ها برنامه WinRAR یا WinZip را روی سیستم خود داشته باشید."
                    )
                    file_found = True
                    break
            if not file_found:
                await update.message.reply_text("کم کم به لحظه خاص نزدیک می‌شیم ولی فقط کمی صبر کنید تا زمان شما تکمیل شود.")
        except Exception as e:
            logger.error(f"خطا در جستجو یا ارسال فایل: {e}")
            await update.message.reply_text("خطایی رخ داده است. لطفاً بعداً تلاش کنید.")

    except Exception as e:
        logger.error(f"خطا در پردازش پیام: {e}")
        await update.message.reply_text("خطایی رخ داده است. لطفاً بعداً تلاش کنید.")

# اجرای ربات
def main():
    application = Application.builder().token(TOKEN).build()

    # دستورات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # شروع ربات
    application.run_polling()

if __name__ == "__main__":
    main()