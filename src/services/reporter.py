import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os
import sys
from datetime import datetime
import pandas as pd
import logging
import time

# Ensure root directory is in sys.path BEFORE importing src modules
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.config import settings
from src.services.logger import AlarmLogger

# Configure logging
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

class EmailReporter:
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.user = settings.SMTP_USER
        self.password = settings.SMTP_PASSWORD
        self.recipients = [email.strip() for email in settings.REPORT_RECIPIENTS.split(",") if email.strip()]

    def generate_excel_report(self) -> str | None:
        """Fetch daily logs and save to a temporary Excel file."""
        logger.info("Fetching daily logs from database...")
        df = AlarmLogger.get_daily_logs()
        
        if df.empty:
            logger.warning("No logs found for today.")
            return None

        filename = f"maintenance_report_{datetime.now().strftime('%Y%m%d')}.xlsx"
        file_path = os.path.join(os.getcwd(), filename)
        
        try:
            logger.info(f"Generating Excel file: {filename}")
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            return file_path
        except Exception as e:
            logger.error(f"Failed to create Excel file: {e}")
            return None

    def send_email(self, file_path: str):
        if not self.recipients:
            logger.error("No recipients configured.")
            return
            
        if not self.password:
             logger.error("SMTP Password missing. Cannot send email.")
             return

        msg = MIMEMultipart()
        msg['From'] = self.user
        msg['To'] = ", ".join(self.recipients)
        msg['Subject'] = f"Endustry 4.0 Maintenance Report - {datetime.now().strftime('%Y-%m-%d')}"

        body = "Please find attached the latest maintenance logs report."
        msg.attach(MIMEText(body, 'plain'))

        try:
            with open(file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {os.path.basename(file_path)}",
            )
            msg.attach(part)
            
            logger.info(f"Connecting to SMTP server {self.smtp_host}:{self.smtp_port}...")
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()
            server.login(self.user, self.password)
            
            server.sendmail(self.user, self.recipients, msg.as_string())
            server.quit()
            logger.info(f"Email sent successfully to {len(self.recipients)} recipients.")

        except Exception as e:
            logger.error(f"Failed to send email: {e}")

    def run(self):
        logger.info("Starting manual report generation...")
        file_path = self.generate_excel_report()
        
        if file_path:
            self.send_email(file_path)
            try:
                os.remove(file_path)
                logger.info(f"Cleaned up temporary file: {file_path}")
            except OSError as e:
                logger.warning(f"Failed to delete temp file: {e}")
        else:
            logger.info("No report generated (no data or error), skipping email.")

if __name__ == "__main__":
    reporter = EmailReporter()
    reporter.run()
