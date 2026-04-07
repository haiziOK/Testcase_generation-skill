"""
LLM client for test case generation.
Currently supports Ollama local server.
"""
import requests
import json
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class LLMClient:
    """Client for interacting with LLM services."""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "qwen2.5-coder:3b"):
        self.base_url = base_url
        self.model = model
        self.chat_url = f"{base_url}/api/chat"

    def chat(self, prompt: str, system: Optional[str] = None, temperature: float = 0.2) -> str:
        """Send a chat prompt to the LLM and return the response."""
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature}
        }

        try:
            logger.debug(f"Sending request to {self.chat_url}, model: {self.model}")
            response = requests.post(self.chat_url, json=payload, timeout=300)
            logger.debug(f"Response status: {response.status_code}")
            response.raise_for_status()
            data = response.json()
            content = data["message"]["content"].strip()
            logger.debug(f"Received response length: {len(content)}")
            return content
        except requests.exceptions.RequestException as e:
            logger.error(f"LLM request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Status code: {e.response.status_code}")
                logger.error(f"Response content: {e.response.text[:500]}")
            return ""
        except json.JSONDecodeError as e:
            logger.error(f"LLM response is not valid JSON: {e}")
            if 'response' in locals():
                logger.error(f"Raw response content: {response.text[:500]}")
            return ""
        except Exception as e:
            logger.error(f"Unexpected error in LLM call: {e}")
            return ""

    @staticmethod
    def get_default_client():
        """Get a default LLM client instance."""
        return LLMClient()