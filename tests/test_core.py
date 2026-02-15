import unittest
from unittest.mock import MagicMock, patch, mock_open
from src.core.ai_engine import AIAnalysisEngine
from src.core.knowledge import KnowledgeBase
from src.core.knowledge.ingestion import PDFProcessor

class TestCoreModules(unittest.TestCase):

    # --- AI ENGINE TESTS ---
    @patch("src.core.ai_engine.Groq")  # Mock Groq library
    def test_ai_generate_report(self, mock_groq):
        """Does AI Engine generate correct prompt and return response?"""
        # Setup
        mock_client = mock_groq.return_value
        mock_client.chat.completions.create.return_value.choices[0].message.content = "Mocked Report"
        
        engine = AIAnalysisEngine()
        docs = [{"source": "test.pdf", "page_num": 1, "text": "Error details..."}]
        
        # Action
        report = engine.generate_report("E01", docs)
        
        # Assert
        self.assertEqual(report, "Mocked Report")
        # Does error code and text appear in messages sent to AI?
        call_args = mock_client.chat.completions.create.call_args[1]
        sent_messages = call_args['messages']
        user_content = sent_messages[1]['content']
        
        self.assertIn("E01", user_content)
        self.assertIn("Error details...", user_content)

    def test_ai_generate_report_no_docs(self):
        """Should return default message without calling AI if no documents found."""
        engine = AIAnalysisEngine()
        # No mock needed as it should return before reaching there
        report = engine.generate_report("E01", [])
        self.assertIn("No Data Found", report)

    # --- KNOWLEDGE BASE TESTS ---
    @patch("src.core.knowledge.store.os.path.exists")
    @patch("src.core.knowledge.store.os.listdir")
    def test_knowledge_search_regex(self, mock_listdir, mock_exists):
        """Does code search with regex work correctly?"""
        mock_exists.return_value = True
        mock_listdir.return_value = ["manuel.pdf"]
        
        # Bypass disk operations when initializing KnowledgeBase
        with patch.object(KnowledgeBase, '_initialize_library'):
            kb = KnowledgeBase()
            # Manually load mock data
            kb.pages = [
                {"text": "This page explains A01590 error code.", "page_num": 1, "source": "test.pdf"},
                {"text": "Irrelevant page.", "page_num": 2, "source": "test.pdf"}
            ]
            
            # Action: Provide a code that should be found by regex
            results = kb.search("CODE=A01590")
            
            # Assert
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]['page_num'], 1)

    # --- PDF PROCESSOR TEST ---
    @patch("src.core.knowledge.ingestion.PdfReader")
    def test_pdf_extraction(self, mock_reader):
        """PDF reading and text extraction logic."""
        # Setup: Simulate a 2-page PDF
        mock_page1 = MagicMock()
        mock_page1.extract_text.return_value = "Page 1\nDetail"
        mock_page2 = MagicMock()
        mock_page2.extract_text.return_value = None # Empty page scenario
        
        mock_reader.return_value.pages = [mock_page1, mock_page2]
        
        # Action
        pages = PDFProcessor.extract_content("dummy.pdf")
        
        # Assert: Should return only the page with text
        self.assertEqual(len(pages), 1)
        self.assertEqual(pages[0]['text'], "Page 1 Detail")
        self.assertEqual(pages[0]['source'], "dummy.pdf")