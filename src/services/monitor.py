from dataclasses import dataclass
from typing import Optional, List, Dict
import logging
from src.services.logger import AlarmLogger
from src.services.db import DatabaseManager
# Type Hinting only
from src.core.knowledge.store import KnowledgeBase 
from src.core.ai_engine import AIAnalysisEngine
from src.services.translation import TranslationService

logger = logging.getLogger(__name__)

STABLE_SIGNAL = "BH"
IGNORED_SIGNALS = ["AHHHH"] # Legacy signal handling, to be deprecated

@dataclass
class CycleResult:
    status: str
    payload: str
    ai_report: Optional[str] = None
    sources: Optional[List[Dict]] = None
    is_new_alarm: bool = False

class MonitorService:
    def __init__(self, kb: KnowledgeBase, ai_engine: AIAnalysisEngine, translator: TranslationService):
        self.kb = kb
        self.ai = ai_engine
        self.translator = translator

    def process_cycle(self, current_payload: str, last_processed_payload: str, language: str = "en") -> CycleResult:
        # 1. Input Validation & Stability Check
        if not current_payload or current_payload in IGNORED_SIGNALS or current_payload == STABLE_SIGNAL:
            return CycleResult(status="STABLE", payload=STABLE_SIGNAL)

        # 2. State Change Detection
        is_new = (current_payload != last_processed_payload)

        # 3. Analysis or Cache Retrieval
        cached_solution = DatabaseManager.get_cached_solution(current_payload)
        
        if cached_solution:
            if is_new:
                logger.info(f"Cache Hit for payload: {current_payload}")
            report = cached_solution
            docs = [] 
        else:
            if is_new:
               logger.info(f"Triggering Analysis for payload: {current_payload}")
            
            docs = self.kb.search(current_payload)
            # Always analyze in English for cache consistency
            report_en = self.ai.generate_report(current_payload, docs)
            
            # Cache English result
            if not report_en.startswith("AI Service Error"):
                DatabaseManager.upsert_solution(current_payload, report_en)
                report = report_en
            else:
                logger.error(f"AI Service Error for payload {current_payload}: {report_en}")
                report = report_en

        # 4. Translation (if needed)
        if language != "en" and not report.startswith("AI Service Error"):
            # Note: Translating cached/fresh English report to target language
            report = self.translator.translate_content(report, language)
        
        # 5. Persistent Logging
        # We log every cycle for history trace, even if cached
        if not report.startswith("AI Service Error"):
            try:
                AlarmLogger.log_alarm(current_payload, report)
            except Exception as e:
                logger.error(f"Failed to log alarm: {e}")
        
        return CycleResult(
            status="ALARM",
            payload=current_payload,
            ai_report=report,
            sources=docs,
            is_new_alarm=is_new
        )