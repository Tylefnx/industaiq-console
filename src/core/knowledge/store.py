import os
import re
import pickle
import hashlib
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.config import settings
from src.core.knowledge.ingestion import PDFProcessor

class KnowledgeBase:
    def __init__(self):
        self.pages: List[Dict] = []
        self.vectorizer = None
        self.vectors = None
        
        if not os.path.exists(settings.CACHE_DIR):
            os.makedirs(settings.CACHE_DIR)
        self._initialize_library()

    def _initialize_library(self):
        if not os.path.exists(settings.SOURCES_DIR): return
        files = [os.path.join(settings.SOURCES_DIR, f) for f in os.listdir(settings.SOURCES_DIR) if f.lower().endswith('.pdf')]
        if not files: return

        lib_hash = self._compute_hash(files)
        cache_path = os.path.join(settings.CACHE_DIR, f"library_{lib_hash}.pkl")

        if os.path.exists(cache_path):
            self._load_cache(cache_path)
        else:
            self._build_index(files, cache_path)

    def _compute_hash(self, files: List[str]) -> str:
        hasher = hashlib.md5()
        for path in sorted(files):
            hasher.update(str(os.path.getmtime(path)).encode())
        return hasher.hexdigest()

    def _load_cache(self, path: str):
        print(f"⚡ Loading cache: {path}")
        with open(path, "rb") as f:
            data = pickle.load(f)
            self.pages, self.vectorizer, self.vectors = data["pages"], data["vectorizer"], data["vectors"]

    def _build_index(self, files: List[str], cache_path: str):
        print("⚙️ Processing PDFs...")
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(PDFProcessor.extract_content, files))
        
        for p in results: self.pages.extend(p)
        
        if self.pages:
            try:
                self.vectorizer = TfidfVectorizer()
                self.vectors = self.vectorizer.fit_transform([p['text'] for p in self.pages])
                with open(cache_path, "wb") as f:
                    pickle.dump({"pages": self.pages, "vectorizer": self.vectorizer, "vectors": self.vectors}, f)
            except Exception as e:
                print(f"Vectorization Error: {e}")

    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        if not self.pages: return []
        results, seen = [], set()

        # 1. Regex Search
        codes = re.findall(r'\b[A-Z]\d{3,7}\b', query.upper())
        if not codes and " " not in query.strip() and len(query) > 3:
            codes = [query.strip()]

        for code in codes:
            for idx, page in enumerate(self.pages):
                if code in page['text'] and idx not in seen:
                    results.append(page)
                    seen.add(idx)

        # 2. Vector Search (Fallback)
        if self.vectorizer and len(results) < 5:
            try:
                vec = self.vectorizer.transform([query])
                sims = cosine_similarity(vec, self.vectors).flatten()
                for idx in sims.argsort()[::-1]:
                    if len(results) >= 5: break
                    if idx not in seen and sims[idx] > 0.15:
                        results.append(self.pages[idx])
                        seen.add(idx)
            except Exception: pass
            
        return results[:5]
