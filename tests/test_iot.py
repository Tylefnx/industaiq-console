import unittest
from unittest.mock import patch, MagicMock
from src.core.telemetry import IoTClient

class TestIoT(unittest.TestCase):
    
    def setUp(self):
        # Reset singleton instance (for test isolation)
        IoTClient._instance = None
    
    @patch("src.core.telemetry.requests.post")
    def test_get_token_success(self, mock_post):
        """Should return string if token retrieval succeeds."""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"token": "SECRET_TOKEN"}
        
        # Mock _start_background_worker to avoid starting thread
        with patch.object(IoTClient, '_start_background_worker'):
            client = IoTClient()
            token = client._get_token()
            self.assertEqual(token, "SECRET_TOKEN")

    @patch("src.core.telemetry.requests.post")
    def test_get_token_fail(self, mock_post):
        """Should return None if login fails."""
        mock_post.return_value.status_code = 401
        
        with patch.object(IoTClient, '_start_background_worker'):
            client = IoTClient()
            token = client._get_token()
            self.assertIsNone(token)