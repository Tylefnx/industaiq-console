import re
from typing import Any

def clean_telemetry_payload(text: Any) -> str:
    """Cleans and standardizes telemetry data."""
    if not text:
        return "AHHHH"
    
    if isinstance(text, bytes):
        text = text.decode('utf-8', errors='ignore')
            
    text_str = str(text).strip()
    
    if "CODE=" in text_str.upper():
        parts = re.split(r'CODE=', text_str, flags=re.IGNORECASE)
        if len(parts) > 1:
            text_str = parts[-1]
    elif "CODE" in text_str.upper() and "=" not in text_str:
         text_str = re.sub(r'CODE', '', text_str, flags=re.IGNORECASE)

    cleaned = re.sub(r'[^a-zA-Z0-9\s:.,_-]', '', text_str)
    return cleaned.strip()