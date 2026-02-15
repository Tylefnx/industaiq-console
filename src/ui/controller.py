import streamlit as st
from src.core.container import get_service
from src.ui.localization import get_text
from src.ui.dashboard import render_logs_expander
import logging

logger = logging.getLogger("controller")

# CONSTANTS
STABLE_CODE = "BH"
REFRESH_RATE = 0.5

@st.fragment(run_every=REFRESH_RATE)
def smart_monitoring_cycle():
    service = get_service()
    plc = st.session_state.plc
    
    # 1. VERİ OKUMA
    raw_payload = plc.get_latest_payload()
    
    # 2. BAĞLANTI KONTROLÜ
    if raw_payload is None:
        st.warning(get_text("connecting"), icon="⏳")
        return

    # 3. İŞLEME
    last_proc = st.session_state.get("last_processed_payload", None)
    curr_lang = st.session_state.get("language", "en")
    
    try:
        result = service.process_cycle(raw_payload, last_processed_payload=last_proc, language=curr_lang)
    except Exception as e:
        logger.error(f"Cycle Error: {e}")
        st.error(f"{get_text('system_malfunction')}: {e}", icon="❌")
        return

    # --- UI RENDERING ---
    
    # A. NORMAL DURUM
    if result.status == "STABLE":
        st.success(f"{get_text('system_nominal')}  •  {get_text('signal_label')}: {result.payload}", icon="✅")
        st.session_state.last_processed_payload = None
             
    # B. ALARM DURUMU
    else:
        st.error(f"{get_text('critical_fault')}: {result.payload}", icon="🔥")

        # C. DIAGNOSTIC CARD
        if result.ai_report:
            st.session_state.last_report = result.ai_report
        
        current_report = st.session_state.get("last_report")
        current_sources = result.sources if result.is_new_alarm else st.session_state.get("last_docs")

        if current_report:
            with st.container(border=True):
                st.markdown(f"### 🛠️ {get_text('remediation_protocol')}")
                st.markdown(current_report)
                
                if current_sources:
                    st.divider()
                    refs = " | ".join([f"{d['source']} (p.{d['page_num']})" for d in current_sources])
                    st.caption(f"📄 **{get_text('reference_documents')}:** {refs}")

            # STATE VE LOG YÖNETİMİ
            if result.is_new_alarm:
                st.session_state.last_processed_payload = result.payload
                st.session_state.last_docs = result.sources
                st.rerun()

def run_dashboard():
    """Main dashboard runner"""
    try:
        smart_monitoring_cycle()
    except Exception as e:
        logger.critical(f"Runtime Exception: {e}")
        st.error(f"{get_text('runtime_exception')}: {e}")

    st.markdown("<br>", unsafe_allow_html=True)
    render_logs_expander()
