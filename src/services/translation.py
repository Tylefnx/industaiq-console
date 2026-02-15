import streamlit as st
from deep_translator import GoogleTranslator

@st.cache_data(show_spinner=False)
def _cached_translate(text: str, target_lang: str) -> str:
    """
    Translates text using Google Translate (deep-translator).
    Cached by Streamlit to prevent redundant requests.
    """
    if target_lang == "en" or not text.strip():
        return text
        
    try:
        # Google Translate handles formatting relatively well, but we should be careful.
        # deep-translator is simple and effective.
        translator = GoogleTranslator(source='auto', target=target_lang)
        return translator.translate(text)
    except Exception as e:
        return f"{text}\n\n[Translation Failed: {e}]"

class TranslationService:
    def __init__(self):
        # No API key needed for basic Google Translate usage via deep-translator
        pass

    def translate_content(self, text: str, target_lang: str) -> str:
        """Translates the given text to the target language."""
        return _cached_translate(text, target_lang)
