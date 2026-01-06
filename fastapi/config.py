"""
AgentGuard Configuration
Pydantic Settings for type-safe configuration
"""

from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application
    APP_NAME: str = "AgentWall Proxy Engine"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # OpenAI
    OPENAI_API_KEY: str = ""  # Required for proxy functionality
    OPENAI_BASE_URL: str = "https://api.openai.com"
    OPENAI_TIMEOUT: int = 120  # seconds
    
    # Multi-Provider Support
    # OpenRouter - 100+ models via single API
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api"
    
    # Groq - Ultra fast inference (LPU)
    GROQ_API_KEY: str = ""
    GROQ_BASE_URL: str = "https://api.groq.com/openai"
    
    # DeepSeek - Cheapest option
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com"
    
    # Mistral AI - European provider
    MISTRAL_API_KEY: str = ""
    MISTRAL_BASE_URL: str = "https://api.mistral.ai"
    
    # Ollama - Local development
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    
    # Alibaba Qwen - Global access
    QWEN_API_KEY: str = ""
    QWEN_BASE_URL: str = "https://dashscope-intl.aliyuncs.com/compatible-mode"
    
    # Provider routing: "openai", "openrouter", "groq", "deepseek", "mistral", "ollama", "auto"
    DEFAULT_PROVIDER: str = "auto"
    
    # ClickHouse
    CLICKHOUSE_HOST: str = "localhost"
    CLICKHOUSE_PORT: int = 9000
    CLICKHOUSE_USER: str = "default"
    CLICKHOUSE_PASSWORD: str = ""
    CLICKHOUSE_DATABASE: str = "agentwall"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_MAX_CONNECTIONS: int = 50
    
    # Laravel Integration
    LARAVEL_URL: str = "http://localhost:8080"
    INTERNAL_SECRET: str = "change-me-in-production"  # Shared secret for internal API calls
    
    # Agent Firewall Settings
    MAX_STEPS: int = 30  # Maximum steps per run
    MAX_TOOL_CALLS: int = 10  # Maximum same tool calls per run
    TIMEOUT_SECONDS: int = 120  # Maximum run duration
    
    # Loop Detection
    SIMILARITY_THRESHOLD: float = 0.95  # Cosine similarity threshold
    SIMILARITY_MODEL: str = "all-MiniLM-L6-v2"  # Sentence transformer model
    
    # DLP Settings
    DLP_MODE: Literal["block", "mask", "shadow_log"] = "mask"
    DLP_ENABLED: bool = True
    
    # Performance
    LOG_BATCH_SIZE: int = 100  # ClickHouse batch insert size
    LOG_FLUSH_INTERVAL: float = 5.0  # seconds
    
    # Monitoring
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
