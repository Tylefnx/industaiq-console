from typing import Optional
from src.core.knowledge.store import KnowledgeBase
from src.core.ai_engine import AIAnalysisEngine
from src.services.translation import TranslationService
from src.services.monitor import MonitorService

class Container:
    """
    Dependency Injection Container.
    Framework-agnostic Singleton implementation.
    """
    _kb_instance: Optional[KnowledgeBase] = None
    _ai_instance: Optional[AIAnalysisEngine] = None
    _trans_instance: Optional[TranslationService] = None
    _monitor_instance: Optional[MonitorService] = None

    @classmethod
    def get_knowledge_base(cls) -> KnowledgeBase:
        if cls._kb_instance is None:
            print("🧠 Loading Neural Knowledge Base...")
            cls._kb_instance = KnowledgeBase()
        return cls._kb_instance

    @classmethod
    def get_ai_engine(cls) -> AIAnalysisEngine:
        if cls._ai_instance is None:
            cls._ai_instance = AIAnalysisEngine()
        return cls._ai_instance

    @classmethod
    def get_translation_service(cls) -> TranslationService:
        if cls._trans_instance is None:
            cls._trans_instance = TranslationService()
        return cls._trans_instance

    @classmethod
    def get_monitor_service(cls) -> MonitorService:
        if cls._monitor_instance is None:
            kb = cls.get_knowledge_base()
            ai = cls.get_ai_engine()
            translator = cls.get_translation_service()
            cls._monitor_instance = MonitorService(kb=kb, ai_engine=ai, translator=translator)
        return cls._monitor_instance

# Global accessor using the Container
def get_service():
    return Container.get_monitor_service()