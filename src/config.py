import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class AppConfig:
    # ThingsBoard
    TB_BASE_URL: str = os.getenv("TB_BASE_URL", "")
    TB_USER: str = os.getenv("TB_USER", "tenant@thingsboard.org")
    TB_PASS: str = os.getenv("TB_PASS", "tenant")
    TB_DEVICE_ID: str = os.getenv("TB_DEVICE_ID", "")
    
    # LLM Settings (Local / Ollama)
    LLM_BASE_URL: str = os.getenv("LLM_BASE_URL", "http://192.168.1.54:11434/v1") 
    MODEL_ID: str = os.getenv("AI_MODEL_ID", "llama3.1")
    
    # Paths
    SOURCES_DIR: str = os.getenv("PDF_SOURCE_DIR", "sources")
    CACHE_DIR: str = os.getenv("CACHE_DIR", "cache")
    LOG_FILE: str = os.getenv("XLSX_SOURCE", "alarm_gecmisi.xlsx")

    # Email Reporting
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.mailgun.org")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    REPORT_RECIPIENTS: str = os.getenv("REPORT_RECIPIENTS", "") # Comma separated emails

    @property
    def tb_host(self) -> str:
        return self.TB_BASE_URL.replace("https://", "").replace("http://", "").rstrip("/")

settings = AppConfig()