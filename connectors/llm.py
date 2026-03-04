"""
LLM Integration for PersonAI
Supports multiple LLM providers: OpenRouter, OpenAI, Ollama
"""
import os
from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod
import httpx
from enum import Enum


class LLMProvider(Enum):
    OPENROUTER = "openrouter"
    OPENAI = "openai"
    OLLAMA = "ollama"


class BaseLLM(ABC):
    """Base class for LLM integrations"""
    
    @abstractmethod
    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Send a chat completion request"""
        pass
    
    @abstractmethod
    async def stream_chat(self, messages: List[Dict[str, str]], **kwargs):
        """Stream a chat completion request"""
        pass


class OpenRouterLLM(BaseLLM):
    """OpenRouter LLM integration"""
    
    def __init__(self, api_key: str, model: str = "qwen/qwen2.5-coder-7b-instruct"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1"
        
    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Send a chat completion request to OpenRouter"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "HTTP-Referer": "https://inquiryinstitute.github.io/PersonAI",
                    "X-Title": "PersonAI"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    **kwargs
                },
                timeout=60.0
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
    
    async def stream_chat(self, messages: List[Dict[str, str]], **kwargs):
        """Stream a chat completion request from OpenRouter"""
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "HTTP-Referer": "https://inquiryinstitute.github.io/PersonAI",
                    "X-Title": "PersonAI"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": True,
                    **kwargs
                },
                timeout=60.0
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        if line.strip() == "data: [DONE]":
                            break
                        try:
                            import json
                            data = json.loads(line[6:])
                            if "choices" in data and len(data["choices"]) > 0:
                                delta = data["choices"][0].get("delta", {})
                                if "content" in delta:
                                    yield delta["content"]
                        except json.JSONDecodeError:
                            continue


class OpenAILLM(BaseLLM):
    """OpenAI LLM integration"""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.openai.com/v1"
        
    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Send a chat completion request to OpenAI"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    **kwargs
                },
                timeout=60.0
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
    
    async def stream_chat(self, messages: List[Dict[str, str]], **kwargs):
        """Stream a chat completion request from OpenAI"""
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": True,
                    **kwargs
                },
                timeout=60.0
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        if line.strip() == "data: [DONE]":
                            break
                        try:
                            import json
                            data = json.loads(line[6:])
                            if "choices" in data and len(data["choices"]) > 0:
                                delta = data["choices"][0].get("delta", {})
                                if "content" in delta:
                                    yield delta["content"]
                        except json.JSONDecodeError:
                            continue


class OllamaLLM(BaseLLM):
    """Ollama LLM integration for local models"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.1:8b"):
        self.base_url = base_url
        self.model = model
        
    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Send a chat completion request to Ollama"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    **kwargs
                },
                timeout=120.0
            )
            response.raise_for_status()
            data = response.json()
            return data["message"]["content"]
    
    async def stream_chat(self, messages: List[Dict[str, str]], **kwargs):
        """Stream a chat completion request from Ollama"""
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": True,
                    **kwargs
                },
                timeout=120.0
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line:
                        try:
                            import json
                            data = json.loads(line)
                            if "message" in data and "content" in data["message"]:
                                yield data["message"]["content"]
                        except json.JSONDecodeError:
                            continue


def create_llm(provider: Optional[str] = None, **kwargs) -> BaseLLM:
    """
    Factory function to create an LLM instance based on environment configuration
    
    Args:
        provider: Override the LLM provider from environment
        **kwargs: Additional arguments for the LLM
    
    Returns:
        BaseLLM instance
    """
    provider = provider or os.getenv("LLM_PROVIDER", "openrouter")
    
    if provider == "openrouter":
        api_key = kwargs.get("api_key") or os.getenv("OPENROUTER_API_KEY")
        model = kwargs.get("model") or os.getenv("OPENROUTER_MODEL", "qwen/qwen2.5-coder-7b-instruct")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is required")
        return OpenRouterLLM(api_key=api_key, model=model)
    
    elif provider == "openai":
        api_key = kwargs.get("api_key") or os.getenv("OPENAI_API_KEY")
        model = kwargs.get("model") or os.getenv("OPENAI_MODEL", "gpt-4")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        return OpenAILLM(api_key=api_key, model=model)
    
    elif provider == "ollama":
        base_url = kwargs.get("base_url") or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        model = kwargs.get("model") or os.getenv("OLLAMA_MODEL", "llama3.1:8b")
        return OllamaLLM(base_url=base_url, model=model)
    
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")
