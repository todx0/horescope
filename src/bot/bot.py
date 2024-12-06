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


class Bot:
    MENU = range(1)

    def __init__(self):
        self.application = Application.builder().token(Config.BOT_API_KEY).build()
        self.conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", self.start)],
            states={self.MENU: [CallbackQueryHandler(self.button)]},
            fallbacks=[CommandHandler("start", self.start)],
        )
        self.application.add_handler(self.conv_handler)
        self.keyboard = [
            [InlineKeyboardButton("♈ Овен", callback_data="aries")],
            [InlineKeyboardButton("♉ Телец", callback_data="taurus")],
            [InlineKeyboardButton("♊ Близнецы", callback_data="gemini")],
            [InlineKeyboardButton("♋ Рак", callback_data="cancer")],
            [InlineKeyboardButton("♌ Лев", callback_data="leo")],
            [InlineKeyboardButton("♍ Дева", callback_data="virgo")],
            [InlineKeyboardButton("♎ Весы", callback_data="libra")],
            [InlineKeyboardButton("♏ Скорпион", callback_data="scorpio")],
            [InlineKeyboardButton("♐ Стрелец", callback_data="sagittarius")],
            [InlineKeyboardButton("♑ Козерог", callback_data="capricorn")],
            [InlineKeyboardButton("♒ Водолей", callback_data="aquarius")],
            [InlineKeyboardButton("♓ Рыбы", callback_data="pisces")],
        ]

    async def start(self, update: Update, context: CallbackContext) -> int:
        reply_markup = InlineKeyboardMarkup(self.keyboard)
        ai_response = await Gemini.text(
            "Generate welcome message for horoscope bot and ask to choose an option below. Do not list zodiac signs"
        )
        await update.message.reply_text(ai_response, reply_markup=reply_markup)
        return self.MENU

    async def cancel(self, update: Update, context: CallbackContext) -> int:
        await update.message.reply_text("Operation cancelled.")
        return ConversationHandler.END

    async def button(self, update: Update, context: CallbackContext) -> int:
        query = update.callback_query
        await query.answer()

        if query.data in [
            "aries",
            "taurus",
            "gemini",
            "cancer",
            "leo",
            "virgo",
            "libra",
            "scorpio",
            "sagittarius",
            "capricorn",
            "aquarius",
            "pisces",
        ]:
            ai_response = await Gemini.text(
                f"Generate long horoscope response for {query.data}"
            )
            await query.edit_message_text(text=ai_response)

            file_path = f"images/{query.data}.png"
            await self.application.bot.send_photo(
                chat_id=query.from_user.id, photo=file_path
            )
        else:
            await query.edit_message_text(text="Unknown option selected.")
            return self.MENU

    def run(self):
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)
