from functools import lru_cache

from django.conf import settings
from langchain_google_genai import ChatGoogleGenerativeAI


@lru_cache
def get_gemini_model() -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=settings.GOOGLE_GEMINI_API_KEY,
    )
