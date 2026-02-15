import streamlit as st
import logging

# 1. SETUP
# We need to manually load translations for Page Title because Session State is not ready yet
try:
    from src.ui.localization import TRANSLATIONS
    qp_lang = st.query_params.get("lang", "en")
    lang_code = qp_lang if qp_lang in TRANSLATIONS else "en"
    page_title = TRANSLATIONS[lang_code]["page_title"]
except ImportError:
    page_title = "IndustAIQ Console"

st.set_page_config(page_title=page_title, layout="wide", page_icon="⚡")

# --- IMPORTS ---
from src.core.verifier import auth_manager 
from src.ui.components import init_page_layout, render_app_bar
from src.ui.state import init_session_state
from src.ui.controller import run_dashboard

# Configure Logger for UI
logger = logging.getLogger("main")

# 2. STYLE LOAD
init_page_layout()

def main():
    user = auth_manager.validate_session()
    if not user: st.stop()

    init_session_state()
    render_app_bar(user)
    
    run_dashboard()

if __name__ == "__main__":
    main()