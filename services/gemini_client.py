import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def get_gemini_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("No se encontró la variable de entorno GEMINI_API_KEY. Revisa tu archivo .env")
    return genai.Client(api_key=api_key)
