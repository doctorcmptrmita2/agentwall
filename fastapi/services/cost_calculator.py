"""
Cost Calculator Service

Calculates cost based on model and token usage.
Prices are per 1M tokens (OpenAI pricing as of Jan 2025).

This enables:
- Run-level budget tracking
- Cost alerts
- Usage analytics
"""

from decimal import Decimal
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Pricing per 1M tokens (input/output)
# Source: https://openai.com/pricing
MODEL_PRICING: dict[str, dict[str, Decimal]] = {
    # GPT-4o
    "gpt-4o": {"input": Decimal("2.50"), "output": Decimal("10.00")},
    "gpt-4o-2024-11-20": {"input": Decimal("2.50"), "output": Decimal("10.00")},
    "gpt-4o-2024-08-06": {"input": Decimal("2.50"), "output": Decimal("10.00")},
    
    # GPT-4o mini
    "gpt-4o-mini": {"input": Decimal("0.15"), "output": Decimal("0.60")},
    "gpt-4o-mini-2024-07-18": {"input": Decimal("0.15"), "output": Decimal("0.60")},
    
    # GPT-4 Turbo
    "gpt-4-turbo": {"input": Decimal("10.00"), "output": Decimal("30.00")},
    "gpt-4-turbo-preview": {"input": Decimal("10.00"), "output": Decimal("30.00")},
    "gpt-4-1106-preview": {"input": Decimal("10.00"), "output": Decimal("30.00")},
    
    # GPT-4
    "gpt-4": {"input": Decimal("30.00"), "output": Decimal("60.00")},
    "gpt-4-32k": {"input": Decimal("60.00"), "output": Decimal("120.00")},
    
    # GPT-3.5 Turbo
    "gpt-3.5-turbo": {"input": Decimal("0.50"), "output": Decimal("1.50")},
    "gpt-3.5-turbo-0125": {"input": Decimal("0.50"), "output": Decimal("1.50")},
    "gpt-3.5-turbo-1106": {"input": Decimal("1.00"), "output": Decimal("2.00")},
    
    # o1 models (reasoning)
    "o1": {"input": Decimal("15.00"), "output": Decimal("60.00")},
    "o1-preview": {"input": Decimal("15.00"), "output": Decimal("60.00")},
    "o1-mini": {"input": Decimal("3.00"), "output": Decimal("12.00")},
    
    # Claude models (Anthropic via OpenAI-compatible API)
    "claude-3-5-sonnet-20241022": {"input": Decimal("3.00"), "output": Decimal("15.00")},
    "claude-3-5-haiku-20241022": {"input": Decimal("0.80"), "output": Decimal("4.00")},
    "claude-3-opus-20240229": {"input": Decimal("15.00"), "output": Decimal("75.00")},
    
    # Default fallback
    "_default": {"input": Decimal("1.00"), "output": Decimal("3.00")},
}


def calculate_cost(
    model: str,
    prompt_tokens: int,
    completion_tokens: int,
) -> Decimal:
    """
    Calculate cost for a request
    
    Args:
        model: Model name (e.g., "gpt-4o-mini")
        prompt_tokens: Number of input tokens
        completion_tokens: Number of output tokens
    
    Returns:
        Cost in USD (Decimal for precision)
    """
    # Get pricing for model (or default)
    pricing = MODEL_PRICING.get(model, MODEL_PRICING["_default"])
    
    # Calculate cost (price is per 1M tokens)
    input_cost = (Decimal(prompt_tokens) / Decimal("1000000")) * pricing["input"]
    output_cost = (Decimal(completion_tokens) / Decimal("1000000")) * pricing["output"]
    
    total = input_cost + output_cost
    
    logger.debug(
        f"Cost calculation: model={model}, "
        f"prompt={prompt_tokens}, completion={completion_tokens}, "
        f"cost=${total:.6f}"
    )
    
    return total


def estimate_cost(
    model: str,
    estimated_tokens: int,
) -> Decimal:
    """
    Estimate cost before request (for budget checks)
    
    Assumes 50/50 split between input/output
    """
    pricing = MODEL_PRICING.get(model, MODEL_PRICING["_default"])
    avg_price = (pricing["input"] + pricing["output"]) / 2
    
    return (Decimal(estimated_tokens) / Decimal("1000000")) * avg_price


def get_model_pricing(model: str) -> dict[str, Decimal]:
    """Get pricing info for a model"""
    return MODEL_PRICING.get(model, MODEL_PRICING["_default"])
