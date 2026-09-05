import os
from io import BytesIO
from PIL import Image
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8990333641:AAGjEA5KvoyTYVEHh0HOcb18JF8GC3vxAuU")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AQ.Ab8RN6Iut9OuEhZwSBxg9WlODKlItFcWqecnlPFQmMQb0OLbyQ")

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
أنت خبير ومهندس ميكانيكا وكهرباء سيارات محترف.
حلل صورة العطل المرفقة وقدم تقريراً سريعاً ودقيقاً ومفهوماً:
1. اسم القطعة الظاهرة (بالعربي والإنجليزي).
2. تشخيص العطل بدقة.
3. مستوى الخطورة: (عادي وتكدر تمشي بيها مؤقتاً / خطر ولازم توقف فوراً).
4. نصيحة عملية للتصليح وتجنب الاستغلال.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! صور عطل السيارة ودز الصورة هنا للفحص فوراً.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("جاري فحص الصورة وتشخيص العطل...")
    try:
        photo_file = await update.message.photo[-1].get_file()
        image_bytes = await photo_file.download_as_bytearray()
        image = Image.open(BytesIO(image_bytes))

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=[SYSTEM_PROMPT, image]
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ: {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()
