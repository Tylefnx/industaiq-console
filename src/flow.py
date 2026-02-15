import streamlit as st
from src.ui.components import display_status, display_ai_report
from src.services.logger import AlarmLogger
from src.ui.state import reset_analysis_cache

def run_system_cycle(status_ph, ai_ph):
    payload = st.session_state.plc.get_latest_payload()
    is_stable = display_status(payload, status_ph)

    if is_stable:
        ai_ph.empty()
        reset_analysis_cache()
    else:
        if st.session_state.get("last_error") != payload:
            ai_ph.empty()
            with ai_ph.container():
                _handle_new_alarm(payload)

        if "last_report" in st.session_state:
            with ai_ph.container():
                display_ai_report(st.session_state.last_report, st.session_state.last_docs)

def _handle_new_alarm(payload):
    with st.spinner(f"Analysing Fault: {payload}..."):
        docs = st.session_state.kb.search(payload)
        report = st.session_state.ai.generate_report(payload, docs)

        st.session_state.last_report = report
        st.session_state.last_docs = docs
        st.session_state.last_error = payload

        if st.session_state.last_logged_alarm != payload:
            if not report.startswith("AI Service Error"):
                AlarmLogger.log_alarm(payload, report)
            st.session_state.last_logged_alarm = payload
