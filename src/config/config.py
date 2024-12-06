import os
from dotenv import load_dotenv
from google.generativeai.types import HarmCategory, HarmBlockThreshold

load_dotenv()


class Config:
    # MISC
    LANGUAGE = os.getenv("LANGUAGE")

    # BOT
    BOT_API_KEY = os.getenv("BOT_API_KEY")

    # GEMINI
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_API_MODEL = "gemini-1.5-flash"
    GEMINI_SAFETY_SETTINGS = [
        {
            "category": HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            "threshold": HarmBlockThreshold.BLOCK_NONE,
        },
        {
            "category": HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            "threshold": HarmBlockThreshold.BLOCK_NONE,
        },
        {
            "category": HarmCategory.HARM_CATEGORY_HARASSMENT,
            "threshold": HarmBlockThreshold.BLOCK_NONE,
        },
        {
            "category": HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            "threshold": HarmBlockThreshold.BLOCK_NONE,
        },
    ]
    GEMINI_SYSTEM_INSTRUCTIONS = f"You are a telegram horoscope bot. Adjust the tone of the reply to be very blunt and impolite. Use horoscope and magic emoji. Reply in {LANGUAGE}"
