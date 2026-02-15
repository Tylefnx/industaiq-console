import os
import sys
import re
import logging
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

# Ensure root directory is in sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.config import settings
from src.core.knowledge.store import KnowledgeBase
from src.services.db import DatabaseManager

# Konfigürasyon
MAX_WORKERS = 3 # Aynı anda kaç sorgu atılsın (Ollama'yı boğmamak için düşük tutun)
REGEX_PATTERN = r'\b[A-Z]\d{3,7}\b' # F01662, E101 vb. yakalar

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("CacheWarmer")

def extract_all_error_codes(kb: KnowledgeBase):
    """PDF'lerdeki tüm olası hata kodlarını regex ile çıkarır."""
    unique_codes = set()
    logger.info("📚 Scanning Knowledge Base for error codes...")
    
    for page in kb.pages:
        matches = re.findall(REGEX_PATTERN, page['text'])
        for match in matches:
            unique_codes.add(match)
            
    logger.info(f"✅ Found {len(unique_codes)} unique potential error codes.")
    return list(unique_codes)

def extract_codes_from_excel(excel_path: str):
    """
    Excel dosyasından alarm kodlarını ve açıklamalarını çıkarır.
    Returns: List of dicts with 'code' and 'context' keys
    """
    logger.info(f"📊 Reading Excel file: {excel_path}")
    
    try:
        df = pd.read_excel(excel_path)
        logger.info(f"✅ Loaded {len(df)} rows from Excel")
        
        alarm_data = []
        
        for idx, row in df.iterrows():
            code = str(row.get('_Number', '')).strip()
            if not code or pd.isna(code):
                continue
            
            # Alarm bilgilerini topla
            long_name = row.get('LongName', '')
            short_name = row.get('ShortName', '')
            
            # Cause texts (tüm cause sütunlarını topla)
            causes = []
            for i in range(100):  # Max 100 cause column
                cause_col = f'Cause/CauseText/{i}'
                if cause_col in df.columns and pd.notna(row.get(cause_col)):
                    causes.append(str(row[cause_col]))
            
            # Remedy texts (tüm remedy sütunlarını topla)
            remedies = []
            for i in range(100):  # Max 100 remedy column
                remedy_col = f'Remedy/RemedyText/{i}'
                if remedy_col in df.columns and pd.notna(row.get(remedy_col)):
                    remedies.append(str(row[remedy_col]))
            
            # Context oluştur (AI için)
            context_parts = []
            if long_name and pd.notna(long_name):
                context_parts.append(f"Description: {long_name}")
            if causes:
                context_parts.append(f"Causes: {' '.join(causes)}")
            if remedies:
                context_parts.append(f"Remedies: {' '.join(remedies)}")
            
            context = '\n'.join(context_parts)
            
            alarm_data.append({
                'code': code,
                'context': context
            })
        
        logger.info(f"✅ Extracted {len(alarm_data)} alarm codes from Excel")
        return alarm_data
        
    except Exception as e:
        logger.error(f"❌ Failed to read Excel file: {e}")
        return []


from src.core.ai_engine import AIAnalysisEngine

# Global AI Engine (Thread safe enough for this script)
ai_engine = AIAnalysisEngine()

def process_code(kb: KnowledgeBase, code: str, excel_context: str = None):
    """
    Tek bir kod için çözüm üretir ve SADECE CACHE'e yazar (Loglamaz).
    
    Args:
        kb: Knowledge base for PDF search
        code: Alarm code
        excel_context: Pre-built context from Excel (optional)
    """
    # Veritabanında zaten var mı kontrol et
    try:
        existing = DatabaseManager.get_cached_solution(code)
        if existing:
            return f"⏭️ {code} - Already Cached"
        
        # 1. Doküman Ara veya Excel context kullan
        if excel_context:
            # Excel'den gelen context'i kullan
            docs = [{
                'source': 'alarmlist_V90_en_raw.xlsx',
                'page_num': 1,
                'text': excel_context
            }]
            logger.info(f"📊 Using Excel context for {code}")
        else:
            # PDF'lerden ara
            docs = kb.search(code)
            logger.info(f"📚 Using PDF search for {code}")
        
        # 2. AI Analiz (İngilizce)
        logger.info(f"🤖 Analyzing {code}...")
        report_en = ai_engine.generate_report(code, docs)
        
        # 3. Cache'e Yaz (Loglamadan!)
        if not report_en.startswith("AI Service Error"):
            DatabaseManager.upsert_solution(code, report_en)
            return f"✅ {code} - Solved & Cached"
        else:
            return f"⚠️ {code} - AI Error: {report_en}"

    except Exception as e:
        return f"❌ {code} - Error: {e}"


def main():
    """
    Cache Warmer - PDF ve/veya Excel kaynaklarından alarm kodlarını cache'e yükler.
    
    Kullanım:
        python -m src.scripts.cache_warmer              # Sadece PDF
        python -m src.scripts.cache_warmer --excel      # Sadece Excel
        python -m src.scripts.cache_warmer --both       # Hem PDF hem Excel
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Cache Warmer for Alarm Codes')
    parser.add_argument('--excel', action='store_true', help='Use Excel file only')
    parser.add_argument('--both', action='store_true', help='Use both PDF and Excel')
    parser.add_argument('--excel-path', type=str, default='sources/alarmlist_V90_en_raw.xlsx',
                       help='Path to Excel file (default: sources/alarmlist_V90_en_raw.xlsx)')
    args = parser.parse_args()
    
    logger.info("🔥 Starting Cache Warmer...")
    
    all_tasks = []  # List of (code, excel_context) tuples
    
    # Knowledge Base Yükle (PDF için)
    kb = KnowledgeBase()
    
    # Excel işleme
    if args.excel or args.both:
        excel_path = os.path.join(project_root, args.excel_path)
        if os.path.exists(excel_path):
            alarm_data = extract_codes_from_excel(excel_path)
            for item in alarm_data:
                all_tasks.append((item['code'], item['context']))
            logger.info(f"📊 Added {len(alarm_data)} codes from Excel")
        else:
            logger.error(f"❌ Excel file not found: {excel_path}")
            if not args.both:
                return
    
    # PDF işleme
    if not args.excel or args.both:
        if not kb.pages:
            logger.warning("⚠️ Knowledge Base is empty! No PDF files in 'sources' folder.")
            if not args.excel and not args.both:
                return
        else:
            pdf_codes = extract_all_error_codes(kb)
            for code in pdf_codes:
                # Excel'de yoksa ekle (both modunda duplicate önleme)
                if not any(task[0] == code for task in all_tasks):
                    all_tasks.append((code, None))  # None = use PDF search
            logger.info(f"📚 Added {len(pdf_codes)} codes from PDF")
    
    if not all_tasks:
        logger.warning("⚠️ No alarm codes found to process!")
        return
    
    logger.info(f"🚀 Processing {len(all_tasks)} unique codes with {MAX_WORKERS} workers...")
    
    # Paralel İşleme (Thread Pool)
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {}
        for code, context in all_tasks:
            future = executor.submit(process_code, kb, code, context)
            futures[future] = code
        
        completed = 0
        for future in as_completed(futures):
            result = future.result()
            completed += 1
            print(f"[{completed}/{len(all_tasks)}] {result}")

    logger.info("🎉 Cache Warming Completed!")

if __name__ == "__main__":
    main()

