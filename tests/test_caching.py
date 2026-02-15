import unittest
from unittest.mock import MagicMock, patch
import sqlite3
import os
from src.services.monitor import MonitorService
from src.services.db import DatabaseManager

class TestCaching(unittest.TestCase):
    
    def setUp(self):
        # Use a separate test database
        self.test_db = "test_caching.db"
        DatabaseManager.DB_NAME = self.test_db
        # Re-init db to ensure tables exist in test db
        DatabaseManager.init_db()
        
    def tearDown(self):
        # Cleanup
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    @patch("src.services.monitor.AIAnalysisEngine")
    def test_cache_miss_and_hit(self, MockAI):
        """
        Test Flow:
        1. Query 'E01' -> Cache Miss -> AI runs -> Saved to DB.
        2. Query 'E01' again -> Cache Hit -> AI does NOT run.
        """
        # Setup Mocks
        mock_ai_instance = MockAI.return_value
        mock_ai_instance.generate_report.return_value = "AI Generated Solution"
        
        mock_kb = MagicMock()
        mock_kb.search.return_value = []
        
        mock_translator = MagicMock()

        service = MonitorService(kb=mock_kb, ai_engine=mock_ai_instance, translator=mock_translator)
        
        # --- 1. First Call (Cache Miss) ---
        result1 = service.process_cycle(current_payload="E01", last_processed_payload=None)
        
        print("\n[Test] Cycle 1 Result:", result1.ai_report)
        self.assertEqual(result1.ai_report, "AI Generated Solution")
        # Verify AI was called
        mock_ai_instance.generate_report.assert_called_once()
        
        # Verify DB has the solution
        cached = DatabaseManager.get_cached_solution("E01")
        self.assertEqual(cached, "AI Generated Solution")

        # --- 2. Second Call (Cache Hit) ---
        # Reset mock to ensure we catch if it's called again
        mock_ai_instance.generate_report.reset_mock()
        
        result2 = service.process_cycle(current_payload="E01", last_processed_payload=None)
        
        print("[Test] Cycle 2 Result:", result2.ai_report)
        self.assertEqual(result2.ai_report, "AI Generated Solution")
        
        # Verify AI was NOT called this time
        mock_ai_instance.generate_report.assert_not_called()
        print("[Test] AI Engine was skipped as expected.")

if __name__ == "__main__":
    unittest.main()
