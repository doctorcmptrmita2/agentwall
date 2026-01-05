"""
OpenAI Proxy Service
Handles communication with OpenAI API with streaming support

Critical: <10ms overhead requirement
"""

import httpx
import json
import time
import logging
from typing import AsyncIterator, Optional, Tuple
from dataclasses import dataclass

from config import settings

logger = logging.getLogger(__name__)


@dataclass
class StreamMetrics:
    """Metrics collected during streaming"""
    run_id: str
    chunk_count: int = 0
    total_chars: int = 0
    first_chunk_ms: float = 0
    total_ms: float = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0


class OpenAIProxyService:
    """
    OpenAI API Proxy with streaming support
    
    Design decisions:
    - Use httpx for async HTTP (faster than aiohttp for this use case)
    - Stream chunks directly without buffering (zero-copy where possible)
    - Collect metrics asynchronously
    """
    
    def __init__(self):
        self.base_url = settings.OPENAI_BASE_URL
        self.api_key = settings.OPENAI_API_KEY
        self.timeout = settings.OPENAI_TIMEOUT
        
    def _get_headers(self, api_key: Optional[str] = None) -> dict:
        """Get headers for OpenAI request"""
        return {
            "Authorization": f"Bearer {api_key or self.api_key}",
            "Content-Type": "application/json",
        }
    
    async def create_client(self) -> httpx.AsyncClient:
        """Create async HTTP client"""
        return httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(self.timeout, connect=10.0),
            headers=self._get_headers(),
            http2=True,  # Enable HTTP/2 for better performance
        )
    
    async def chat_completion(
        self,
        request_data: dict,
        run_id: str,
        api_key: Optional[str] = None
    ) -> dict:
        """
        Non-streaming chat completion
        
        Returns: OpenAI response dict
        """
        start_time = time.perf_counter()
        
        async with httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(self.timeout),
            headers=self._get_headers(api_key),
        ) as client:
            response = await client.post(
                "/v1/chat/completions",
                json=request_data
            )
            
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            
            if response.status_code != 200:
                logger.error(f"OpenAI error: {response.status_code} - {response.text}")
                raise OpenAIError(response.status_code, response.text)
            
            result = response.json()
            
            logger.info(
                f"Chat completion: run_id={run_id}, "
                f"model={request_data.get('model')}, "
                f"tokens={result.get('usage', {}).get('total_tokens', 0)}, "
                f"latency={elapsed_ms:.1f}ms"
            )
            
            return result
    
    async def chat_completion_stream(
        self,
        request_data: dict,
        run_id: str,
        api_key: Optional[str] = None
    ) -> Tuple[AsyncIterator[bytes], StreamMetrics]:
        """
        Streaming chat completion with SSE
        
        Returns: (async iterator of SSE bytes, metrics object)
        
        Critical: This must add <1ms overhead per chunk
        """
        metrics = StreamMetrics(run_id=run_id)
        start_time = time.perf_counter()
        
        client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(None, connect=10.0),  # No read timeout for streaming
            headers=self._get_headers(api_key),
        )
        
        try:
            response = await client.send(
                client.build_request(
                    "POST",
                    "/v1/chat/completions",
                    json=request_data
                ),
                stream=True
            )
            
            if response.status_code != 200:
                error_body = await response.aread()
                await client.aclose()
                raise OpenAIError(response.status_code, error_body.decode())
            
            async def stream_generator() -> AsyncIterator[bytes]:
                """Generate SSE chunks with minimal overhead"""
                nonlocal metrics
                first_chunk = True
                
                try:
                    async for line in response.aiter_lines():
                        if not line:
                            continue
                        
                        # Track first chunk latency (TTFB)
                        if first_chunk:
                            metrics.first_chunk_ms = (time.perf_counter() - start_time) * 1000
                            first_chunk = False
                        
                        metrics.chunk_count += 1
                        
                        # Pass through SSE format directly
                        if line.startswith("data: "):
                            data_str = line[6:]
                            
                            if data_str.strip() == "[DONE]":
                                yield b"data: [DONE]\n\n"
                                break
                            
                            try:
                                data = json.loads(data_str)
                                
                                # Extract content for metrics
                                if "choices" in data and data["choices"]:
                                    delta = data["choices"][0].get("delta", {})
                                    content = delta.get("content", "")
                                    if content:
                                        metrics.total_chars += len(content)
                                
                                # Extract usage if present (final chunk)
                                if "usage" in data:
                                    metrics.prompt_tokens = data["usage"].get("prompt_tokens", 0)
                                    metrics.completion_tokens = data["usage"].get("completion_tokens", 0)
                                
                            except json.JSONDecodeError:
                                pass
                            
                            # Yield original line (minimal processing)
                            yield f"data: {data_str}\n\n".encode()
                
                finally:
                    metrics.total_ms = (time.perf_counter() - start_time) * 1000
                    await response.aclose()
                    await client.aclose()
                    
                    logger.info(
                        f"Stream completed: run_id={run_id}, "
                        f"chunks={metrics.chunk_count}, "
                        f"chars={metrics.total_chars}, "
                        f"ttfb={metrics.first_chunk_ms:.1f}ms, "
                        f"total={metrics.total_ms:.1f}ms"
                    )
            
            return stream_generator(), metrics
            
        except Exception as e:
            await client.aclose()
            raise


class OpenAIError(Exception):
    """OpenAI API error"""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"OpenAI API error {status_code}: {message}")


# Singleton instance
openai_proxy = OpenAIProxyService()
