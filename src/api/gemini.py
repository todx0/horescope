from src.config.config import Config
import google.generativeai as genai


class Gemini:
    async def get_gemini_model():
        genai.configure(api_key=Config.GEMINI_API_KEY)
        return genai.GenerativeModel(
            model_name=Config.GEMINI_API_MODEL,
            safety_settings=Config.GEMINI_SAFETY_SETTINGS,
            system_instruction=Config.GEMINI_SYSTEM_INSTRUCTIONS,
        )

    @staticmethod
    async def text(request: str) -> str:
        try:
            model = await Gemini.get_gemini_model()
            response = await model.generate_content_async(request)
            if not response.text:
                raise ValueError("No content received from the model.")
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
