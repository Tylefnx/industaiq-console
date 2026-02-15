import streamlit as st
from src.ui.localization import get_text

def render_app_bar(user_data):
    if not user_data: return
    email = user_data.get('email', 'Operator')
    
    # Init Selectbox State
    curr_lang = st.session_state.get("language", "en")
    
    # --- NATIVE HEADER LAYOUT ---
    
    # Styling for the container that wraps these columns (hacky but works for top commands)
    st.markdown("""
        <style>
            div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stHorizontalBlock"]) {
                /* structural adjustments if needed */
            }
        </style>
    """, unsafe_allow_html=True)

    # Layout: Brand | Spacer | User | Lang
    c_brand, c_spacer, c_user, c_lang = st.columns([6, 2, 2, 2], gap="small", vertical_alignment="center")
    
    with c_brand:
        st.markdown(f"""
        <div class="brand" style="margin: 0; padding: 0;">
            <div class="brand-icon">🏭</div>
            IndustAIQ <span style="border-left: 1px solid #30363d; margin-left: 10px; padding-left: 10px;">{get_text("app_tagline")}</span>
        </div>
        """, unsafe_allow_html=True)
        
    with c_user:
        st.markdown(f"""
        <div class="user-pill">
            <div class="status-indicator"></div>
            <span class="user-text">{email}</span>
        </div>
        """, unsafe_allow_html=True)
        
    with c_lang:
        # Custom Popover Dropdown (Best of both worlds: Native Rerun + Custom Style)
        lang_map = {
            "en": "English", "tr": "Türkçe", "de": "Deutsch",
            "es": "Español", "fr": "Français", "zh": "中文",
            "ja": "日本語", "pt": "Português", "ru": "Русский", "it": "Italiano"
        }
        curr_label = lang_map.get(curr_lang, "Language")
        
        # The Popover Container
        # We label it with the current language so it acts like the selected value
        with st.popover(f"🌐  {curr_label}", use_container_width=True):
            for code, name in lang_map.items():
                # If clicked, update state and rerun
                if st.button(name, key=f"lang_btn_{code}", use_container_width=True):
                    st.session_state.language = code
                    st.query_params["lang"] = code
                    st.rerun()
            
    # Add a separator line to mimic the bottom border of the old app bar
    st.markdown("<hr style='margin-top: 5px; margin-bottom: 25px; border: 0; border-top: 1px solid #30363d;'>", unsafe_allow_html=True)
