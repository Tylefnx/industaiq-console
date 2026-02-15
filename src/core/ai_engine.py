from openai import OpenAI, APIError
import logging
from typing import List, Dict
from src.config import settings

class AIAnalysisEngine:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initializing Local AI Engine (Ollama) at {settings.LLM_BASE_URL} with model {settings.MODEL_ID}")
        
        # Ollama provides an OpenAI compatible API
        self.client = OpenAI(
            base_url=settings.LLM_BASE_URL,
            api_key="ollama" # api key required but ignored by ollama
        )

    def generate_report(self, alarm_payload: str, docs: List[Dict]) -> str:
        """
        Generates a diagnostic report using the Local LLM (Ollama).
        """
        if not docs:
            return f"⚠️ **No Data Found:** I could not find any information about `{alarm_payload}` in the manual."

        context_text = "\n\n".join([
            f"--- Source: {doc['source']} (Page {doc['page_num']}) ---\n{doc['text']}" 
            for doc in docs
        ])

        system_prompt = self._build_system_prompt()
        user_prompt = f"ALARM CODE: {alarm_payload}\n\nTECHNICAL CONTEXT:\n{context_text}"

        try:
            response = self.client.chat.completions.create(
                model=settings.MODEL_ID,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1, # Keep it deterministic
                max_tokens=600  # Ollama usually ignores this or handles it differently, but good practice
            )
            return response.choices[0].message.content

        except APIError as e:
            self.logger.error(f"AI Service Error: {e}")
            return f"AI Service Error: Connection to Local LLM failed. ({e})"
        except Exception as e:
            self.logger.error(f"Unexpected AI Error: {e}")
            return f"AI Service Error: Unexpected error. ({e})"

    def _build_system_prompt(self) -> str:
        return """You are an expert industrial maintenance assistant.
Your goal is to analyze the ALARM CODE provided by the machine and suggest a solution.

RULES:
1. Analyze ONLY using the provided TECHNICAL CONTEXT (Manuals).
2. If the context does not contain the specific error code, say "I don't know" - DO NOT HALLUCINATE.
3. Provide a structured response:
   - **Root Cause:** What triggered the alarm?
   - **Immediate Action:** What should the operator do right now?
   - **Checklist:** 2-3 bullet points for troubleshooting.
4. Keep the tone professional, concise, and safety-oriented.
"""