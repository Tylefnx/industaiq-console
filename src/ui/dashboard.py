import streamlit as st
import io
import pandas as pd
from src.services.logger import AlarmLogger
from src.ui.localization import get_text

def render_logs_expander():
    st.markdown(f"### 📋 {get_text('system_logs')}")
    with st.expander(get_text("view_alarm_history")):
        df = AlarmLogger.get_logs()
        if not df.empty:
            st.dataframe(df, width="stretch", height=300)
            
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            st.download_button(f"📥 {get_text('download_report')}", buffer.getvalue(), "industaiq_logs.xlsx")
        else:
            st.info(get_text("no_data"))
