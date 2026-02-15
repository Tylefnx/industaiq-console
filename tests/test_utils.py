import pytest
from src.utils import clean_telemetry_payload

@pytest.mark.parametrize("input_val, expected", [
    ("CODE=A01590", "A01590"),           # Prefix cleanup
    ("code=b999", "b999"),               # Case insensitive prefix
    ("AHHHH", "AHHHH"),                  # Stabil durum
    (b"CODE=C123", "C123"),              # Bytes input
    ("!!! A-500 ###", "A-500"),          # Regex cleaning (symbols removed)
    (None, "AHHHH"),                     # None input
    ("", "AHHHH"),                       # Empty string
    ("   CODE=  D555  ", "D555"),        # Space cleanup
])
def test_clean_telemetry_payload(input_val, expected):
    """Verifies telemetry data cleaning logic."""
    assert clean_telemetry_payload(input_val) == expected