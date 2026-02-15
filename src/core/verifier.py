import streamlit as st
import requests
import logging
from typing import Optional, Dict, Any
from src.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UltraSecureVerifier:
    """
    Handles internal JWT validation to bypass Cloudflare loop issues
    and ensure only authenticated ThingsBoard users can access the UI.
    """
    def __init__(self):
        # SECURITY MASTER STROKE: 
        # We bypass the public URL and hit TB directly on the local port (9090).
        # This fixes the 'Internal authentication connection failed' error.
        self.internal_auth_url = "http://127.0.0.1:9090/api/auth/user"

    def validate_session(self) -> Optional[Dict[str, Any]]:
        # 1. OPTIMIZATION: Check Cache First
        # If we already have a validated user in this session, return it immediately.
        if "user" in st.session_state:
            return st.session_state.user

        # 2. TOKEN RETRIEVAL
        token = st.query_params.get("token")
        
        # If no token in session OR url, deny access.
        if not token:
            self._abort("Access Restricted", "Direct access is prohibited. Please use the ThingsBoard Dashboard.")
            return None

        # 3. VALIDATION
        try:
            # Standardize token format
            clean_token = token.replace("Bearer ", "")
            headers = {"X-Authorization": f"Bearer {clean_token}"}
            
            # Internal request: No SSL validation needed for localhost
            response = requests.get(
                self.internal_auth_url, 
                headers=headers, 
                timeout=5, 
                verify=False
            )

            if response.status_code == 200:
                user_info = response.json()
                logger.info(f"Authorized access: {user_info.get('email')}")
                
                # Cache the result
                st.session_state.user = user_info
                st.session_state.auth_token = token
                
                # 4. SECURITY: Consume the Token (Clear it from URL)
                # This ensures the token doesn't linger in the browser history or address bar.
                if "token" in st.query_params:
                    # del st.query_params["token"] # Deprecated in newer Streamlit versions if using query_params dictionary style
                    # Using the new way allows us to just pop it or set it to None, but Streamlit's st.query_params behaves like a dict.
                    try:
                        del st.query_params["token"]
                    except KeyError:
                        pass
                
                return user_info
            
            # Handle expired sessions
            logger.warning("Auth Failed: Invalid/Expired Token provided.")
            self._abort("Session Invalid", "Your session has expired. Please refresh ThingsBoard.")
            return None

        except Exception as e:
            logger.error(f"Critical Auth Failure: {str(e)}")
            self._abort("System Error", "The security gateway is currently unreachable.")
            return None

    def _abort(self, title: str, msg: str):
        """Strictly halts app execution and displays security notice."""
        st.set_page_config(page_title=title, page_icon="🚫")
        st.error(f"### 🚫 {title}")
        st.markdown(f"**{msg}**")
        st.stop() # Logic barrier

auth_manager = UltraSecureVerifier()
