from src.services.db import DatabaseManager

class AlarmLogger:
    @staticmethod
    def log_alarm(error_code: str, report: str):
        """
        Alarmı veritabanına kaydeder.
        Operator parametresi gereksiz olduğu için kaldırıldı.
        """
        DatabaseManager.log_fault(error_code, report)

    @staticmethod
    def get_logs():
        return DatabaseManager.get_logs_as_df()

    @staticmethod
    def get_daily_logs():
        """Sadece bugünün loglarını getirir."""
        return DatabaseManager.get_daily_logs_as_df()
