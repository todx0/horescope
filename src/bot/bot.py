from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
    ConversationHandler,
)
from src.config.config import Config
from src.api.gemini import Gemini
from datetime import datetime


class Bot:
    MENU = range(1)
    ZODIAC_SIGNS = [
        ("aries", "♈ Овен"),
        ("taurus", "♉ Телец"),
        ("gemini", "♊ Близнецы"),
        ("cancer", "♋ Рак"),
        ("leo", "♌ Лев"),
        ("virgo", "♍ Дева"),
        ("libra", "♎ Весы"),
        ("scorpio", "♏ Скорпион"),
        ("sagittarius", "♐ Стрелец"),
        ("capricorn", "♑ Козерог"),
        ("aquarius", "♒ Водолей"),
        ("pisces", "♓ Рыбы"),
    ]

    def __init__(self):
        self.application = Application.builder().token(Config.BOT_API_KEY).build()
        self.conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", self.start)],
            states={self.MENU: [CallbackQueryHandler(self.button)]},
            fallbacks=[CommandHandler("start", self.start)],
        )
        self.application.add_handler(self.conv_handler)
        self.keyboard = [
            [InlineKeyboardButton(translation, callback_data=sign)]
            for sign, translation in self.ZODIAC_SIGNS
        ]

    def run(self):
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

    async def start(self, update: Update, context: CallbackContext) -> int:
        reply_markup = InlineKeyboardMarkup(self.keyboard)
        ai_response = await Gemini.text(
            "Generate welcome message for horoscope bot. Do not list zodiac signs. Cringe a lot."
        )
        await update.message.reply_text(ai_response, reply_markup=reply_markup)
        return self.MENU

    async def cancel(self, update: Update, context: CallbackContext) -> int:
        await update.message.reply_text("Operation cancelled.")
        return ConversationHandler.END

    async def button(self, update: Update, context: CallbackContext) -> int:
        query = update.callback_query
        await query.answer()

        if query.data in [sign for sign, _ in self.ZODIAC_SIGNS]:
            await self.edit_message_with_ai_generated_horoscope_result(query)
            await self.send_zodiac_sign_image(query)
        else:
            await query.edit_message_text(text="Unknown option selected.")
            return self.MENU

    async def edit_message_with_ai_generated_horoscope_result(self, query):
        current_date = datetime.now().strftime("%A, %d %B")
        ai_response = await Gemini.text(
            f"Generate long horoscope response. Zodiac sign: {query.data}, date: {current_date}"
        )
        await query.edit_message_text(text=ai_response)

    async def send_zodiac_sign_image(self, query):
        file_path = f"images/{query.data}.png"
        await self.application.bot.send_photo(
            chat_id=query.from_user.id, photo=file_path
        )
