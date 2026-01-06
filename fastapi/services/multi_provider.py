"""
Multi-Provider LLM Proxy Service
================================
Supports OpenAI, OpenRouter (100+ models), and future providers.

Provider Routing:
- OpenAI models (gpt-*) -> OpenAI API
- OpenRouter models (anthropic/*, google/*, meta-llama/*) -> OpenRouter API
- Pass-through mode: Use user's API key directly

OpenRouter gives access to:
- Anthropic (Claude 3.5 Sonnet, Claude 3 Opus)
- Google (Gemini Pro, Gemini Flash)
- Meta (Llama 3.1 70B, 405B)
- Mistral (Mixtral, Mistral Large)
- And 100+ more models
"""

import httpx
import json
import time
import logging
from typing import AsyncIterator, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from config import settings

logger = logging.getLogger(__name__)


class Provider(str, Enum):
    OPENAI = "openai"
    OPENROUTER = "openrouter"
    GROQ = "groq"
    DEEPSEEK = "deepseek"
    MISTRAL = "mistral"
    OLLAMA = "ollama"
    QWEN = "qwen"


@dataclass
class ProviderConfig:
    """Provider configuration"""
    name: Provider
    base_url: str
    api_key: str
    extra_headers: dict = None


# Model -> Provider mapping
OPENROUTER_PREFIXES = [
    "anthropic/",      # Claude models
    "google/",         # Gemini models
    "meta-llama/",     # Llama models
    "mistralai/",      # Mistral models (via OpenRouter)
    "cohere/",         # Cohere models
    "perplexity/",     # Perplexity models
    "deepseek/",       # DeepSeek (via OpenRouter)
    "qwen/",           # Qwen models (via OpenRouter)
    "openrouter/",     # OpenRouter specific
    "groq/",           # Groq (via OpenRouter)
]

# Direct provider prefixes (bypass OpenRouter)
GROQ_PREFIXES = ["llama-3", "mixtral", "gemma"]  # Groq native models
DEEPSEEK_PREFIXES = ["deepseek-chat", "deepseek-coder", "deepseek-reasoner"]
MISTRAL_PREFIXES = ["mistral-", "codestral", "pixtral", "ministral"]
OLLAMA_PREFIXES = ["ollama/", "local/"]
QWEN_PREFIXES = ["qwen-"]

# OpenRouter model aliases (shortcuts)
OPENROUTER_ALIASES = {
    "claude-3.5-sonnet": "anthropic/claude-3.5-sonnet",
    "claude-3-opus": "anthropic/claude-3-opus",
    "claude-3-sonnet": "anthropic/claude-3-sonnet",
    "claude-sonnet-4": "anthropic/claude-sonnet-4",
    "gemini-pro": "google/gemini-pro",
    "gemini-flash": "google/gemini-flash-1.5",
    "llama-3.1-70b": "meta-llama/llama-3.1-70b-instruct",
    "llama-3.1-405b": "meta-llama/llama-3.1-405b-instruct",
    "mixtral-8x7b": "mistralai/mixtral-8x7b-instruct",
    "mistral-large": "mistralai/mistral-large",
}


def detect_provider(model: str) -> Provider:
    """
    Detect which provider to use based on model name
    
    Examples:
        gpt-4 -> OPENAI
        anthropic/claude-3.5-sonnet -> OPENROUTER
        claude-3.5-sonnet -> OPENROUTER (alias)
        llama-3.1-70b-versatile -> GROQ (native)
        deepseek-chat -> DEEPSEEK (native)
        mistral-large-latest -> MISTRAL (native)
        ollama/llama3 -> OLLAMA (local)
    """
    # Check aliases first
    if model in OPENROUTER_ALIASES:
        return Provider.OPENROUTER
    
    # Check Ollama (local)
    for prefix in OLLAMA_PREFIXES:
        if model.startswith(prefix):
            return Provider.OLLAMA
    
    # Check Groq native
    for prefix in GROQ_PREFIXES:
        if model.startswith(prefix) and not model.startswith("meta-llama/"):
            return Provider.GROQ
    
    # Check DeepSeek native
    for prefix in DEEPSEEK_PREFIXES:
        if model.startswith(prefix):
            return Provider.DEEPSEEK
    
    # Check Mistral native
    for prefix in MISTRAL_PREFIXES:
        if model.startswith(prefix) and not model.startswith("mistralai/"):
            return Provider.MISTRAL
    
    # Check Qwen native
    for prefix in QWEN_PREFIXES:
        if model.startswith(prefix) and not model.startswith("qwen/"):
            return Provider.QWEN
    
    # Check OpenRouter prefixes
    for prefix in OPENROUTER_PREFIXES:
        if model.startswith(prefix):
            return Provider.OPENROUTER
    
    # Default to OpenAI for gpt-* models
    return Provider.OPENAI


def resolve_model(model: str) -> str:
    """Resolve model aliases to full names"""
    return OPENROUTER_ALIASES.get(model, model)


def get_provider_config(provider: Provider, user_api_key: Optional[str] = None) -> ProviderConfig:
    """Get provider configuration"""
    
    if provider == Provider.OPENAI:
        return ProviderConfig(
            name=Provider.OPENAI,
            base_url=settings.OPENAI_BASE_URL,
            api_key=user_api_key or settings.OPENAI_API_KEY,
        )
    
    elif provider == Provider.OPENROUTER:
        return ProviderConfig(
            name=Provider.OPENROUTER,
            base_url=settings.OPENROUTER_BASE_URL,
            api_key=user_api_key or settings.OPENROUTER_API_KEY,
            extra_headers={
                "HTTP-Referer": "https://agentwall.io",
                "X-Title": "AgentWall",
            }
        )
    
    elif provider == Provider.GROQ:
        return ProviderConfig(
            name=Provider.GROQ,
            base_url=settings.GROQ_BASE_URL,
            api_key=user_api_key or settings.GROQ_API_KEY,
        )
    
    elif provider == Provider.DEEPSEEK:
        return ProviderConfig(
            name=Provider.DEEPSEEK,
            base_url=settings.DEEPSEEK_BASE_URL,
            api_key=user_api_key or settings.DEEPSEEK_API_KEY,
        )
    
    elif provider == Provider.MISTRAL:
        return ProviderConfig(
            name=Provider.MISTRAL,
            base_url=settings.MISTRAL_BASE_URL,
            api_key=user_api_key or settings.MISTRAL_API_KEY,
        )
    
    elif provider == Provider.OLLAMA:
        return ProviderConfig(
            name=Provider.OLLAMA,
            base_url=settings.OLLAMA_BASE_URL,
            api_key="ollama",  # Ollama doesn't need API key
        )
    
    elif provider == Provider.QWEN:
        return ProviderConfig(
            name=Provider.QWEN,
            base_url=settings.QWEN_BASE_URL,
            api_key=user_api_key or settings.QWEN_API_KEY,
        )
    
    else:
        raise ValueError(f"Unknown provider: {provider}")


@dataclass
class StreamMetrics:
    """Metrics collected during streaming"""
    run_id: str
    provider: str = ""
    model: str = ""
    chunk_count: int = 0
    total_chars: int = 0
    first_chunk_ms: float = 0
    total_ms: float = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0


class MultiProviderError(Exception):
    """Multi-provider API error"""
    def __init__(self, status_code: int, message: str, provider: str):
        self.status_code = status_code
        self.message = message
        self.provider = provider
        super().__init__(f"{provider} API error {status_code}: {message}")


class MultiProviderProxy:
    """
    Multi-provider LLM proxy with automatic routing
    
    Usage:
        # Auto-detect provider from model name
        response = await proxy.chat_completion({"model": "gpt-4", ...})
        response = await proxy.chat_completion({"model": "anthropic/claude-3.5-sonnet", ...})
        response = await proxy.chat_completion({"model": "claude-3.5-sonnet", ...})  # alias
    """
    
    def __init__(self):
        self.timeout = settings.OPENAI_TIMEOUT
    
    def _get_headers(self, config: ProviderConfig) -> dict:
        """Get headers for provider request"""
        headers = {
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
        }
        if config.extra_headers:
            headers.update(config.extra_headers)
        return headers
    
    async def chat_completion(
        self,
        request_data: dict,
        run_id: str,
        api_key: Optional[str] = None,
        force_provider: Optional[Provider] = None,
    ) -> dict:
        """
        Non-streaming chat completion with auto provider routing
        """
        model = request_data.get("model", "gpt-3.5-turbo")
        resolved_model = resolve_model(model)
        
        # Detect or use forced provider
        provider = force_provider or detect_provider(resolved_model)
        config = get_provider_config(provider, api_key)
        
        # Update model in request if alias was used
        if resolved_model != model:
            request_data = {**request_data, "model": resolved_model}
        
        start_time = time.perf_counter()
        
        async with httpx.AsyncClient(
            base_url=config.base_url,
            timeout=httpx.Timeout(self.timeout),
            headers=self._get_headers(config),
        ) as client:
            response = await client.post("/v1/chat/completions", json=request_data)
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            
            if response.status_code != 200:
                logger.error(f"{provider.value} error: {response.status_code} - {response.text}")
                raise MultiProviderError(response.status_code, response.text, provider.value)
            
            result = response.json()
            
            logger.info(
                f"Chat completion: provider={provider.value}, model={resolved_model}, "
                f"run_id={run_id}, tokens={result.get('usage', {}).get('total_tokens', 0)}, "
                f"latency={elapsed_ms:.1f}ms"
            )
            
            # Add provider info to response
            result["_agentwall_provider"] = provider.value
            
            return result
    
    async def chat_completion_stream(
        self,
        request_data: dict,
        run_id: str,
        api_key: Optional[str] = None,
        force_provider: Optional[Provider] = None,
    ) -> Tuple[AsyncIterator[bytes], StreamMetrics]:
        """
        Streaming chat completion with auto provider routing
        """
        model = request_data.get("model", "gpt-3.5-turbo")
        resolved_model = resolve_model(model)
        
        provider = force_provider or detect_provider(resolved_model)
        config = get_provider_config(provider, api_key)
        
        if resolved_model != model:
            request_data = {**request_data, "model": resolved_model}
        
        metrics = StreamMetrics(run_id=run_id, provider=provider.value, model=resolved_model)
        start_time = time.perf_counter()
        
        client = httpx.AsyncClient(
            base_url=config.base_url,
            timeout=httpx.Timeout(None, connect=10.0),
            headers=self._get_headers(config),
        )
        
        try:
            response = await client.send(
                client.build_request("POST", "/v1/chat/completions", json=request_data),
                stream=True
            )
            
            if response.status_code != 200:
                error_body = await response.aread()
                await client.aclose()
                raise MultiProviderError(response.status_code, error_body.decode(), provider.value)
            
            async def stream_generator() -> AsyncIterator[bytes]:
                nonlocal metrics
                first_chunk = True
                
                try:
                    async for line in response.aiter_lines():
                        if not line:
                            continue
                        
                        if first_chunk:
                            metrics.first_chunk_ms = (time.perf_counter() - start_time) * 1000
                            first_chunk = False
                        
                        metrics.chunk_count += 1
                        
                        if line.startswith("data: "):
                            data_str = line[6:]
                            
                            if data_str.strip() == "[DONE]":
                                yield b"data: [DONE]\n\n"
                                break
                            
                            try:
                                data = json.loads(data_str)
                                if "choices" in data and data["choices"]:
                                    delta = data["choices"][0].get("delta", {})
                                    content = delta.get("content", "")
                                    if content:
                                        metrics.total_chars += len(content)
                            except json.JSONDecodeError:
                                pass
                            
                            yield f"data: {data_str}\n\n".encode()
                
                finally:
                    metrics.total_ms = (time.perf_counter() - start_time) * 1000
                    await response.aclose()
                    await client.aclose()
                    
                    logger.info(
                        f"Stream completed: provider={provider.value}, model={resolved_model}, "
                        f"run_id={run_id}, chunks={metrics.chunk_count}, ttfb={metrics.first_chunk_ms:.1f}ms"
                    )
            
            return stream_generator(), metrics
            
        except Exception as e:
            await client.aclose()
            raise


# Singleton instance
multi_provider_proxy = MultiProviderProxy()
