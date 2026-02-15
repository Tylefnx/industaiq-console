import streamlit as st
from src.core.container import Container
from src.core.telemetry import IoTClient
from src.ui.localization import TRANSLATIONS

def init_session_state():
    if "plc" not in st.session_state:
        # Wrapper for services
        # We rely on the Controller to initialize the full stack via Container when needed.
        # However, if we need to store something in session state, we can.
        
        st.session_state.plc = IoTClient() 
        st.session_state.last_logged_alarm = None
        
        # Localization Init
        qp = st.query_params.get("lang")
        st.session_state.language = qp if qp in TRANSLATIONS.keys() else "en"

def reset_analysis_cache():
    """Clears AI history when system is stable."""
    for key in ['last_report', 'last_docs', 'last_error']:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.last_logged_alarm = None