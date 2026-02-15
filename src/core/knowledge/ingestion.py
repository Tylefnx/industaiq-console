from pypdf import PdfReader
import os
from typing import List, Dict, Any

class PDFProcessor:
    @staticmethod
    def extract_content(file_path: str) -> List[Dict[str, Any]]:
        pages = []
        try:
            reader = PdfReader(file_path)
            filename = os.path.basename(file_path)
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    pages.append({
                        "source": filename,
                        "page_num": i + 1,
                        "text": text.replace('\n', ' ').strip(),
                        "raw_text": text
                    })
        except Exception as e:
            print(f"PDF Error ({file_path}): {e}")
        return pages
