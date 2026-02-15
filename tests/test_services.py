import unittest
from unittest.mock import patch
from src.services.logger import AlarmLogger

class TestLogger(unittest.TestCase):

    @patch("src.services.logger.DatabaseManager")
    def test_log_alarm_calls_db(self, mock_db_manager):
        """Test if log_alarm calls DatabaseManager.log_fault correctly."""
        error_code = "E123"
        report = "Analysis Report"
        
        AlarmLogger.log_alarm(error_code, report)
        
        mock_db_manager.log_fault.assert_called_once_with(error_code, report)

    @patch("src.services.logger.DatabaseManager")
    def test_get_logs_calls_db(self, mock_db_manager):
        """Test if get_logs calls DatabaseManager.get_logs_as_df."""
        AlarmLogger.get_logs()
        mock_db_manager.get_logs_as_df.assert_called_once()