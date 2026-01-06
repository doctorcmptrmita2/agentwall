"""
Cost Calculator Service
Calculates API costs for different models

Pricing (as of Jan 2026):
- GPT-4: $0.03/1K prompt, $0.06/1K completion
- GPT-3.5: $0.0005/1K prompt, $0.0015/1K completion
- Claude 3: $0.003/1K prompt, $0.015/1K completion
"""

from decimal import Decimal
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)


# Pricing table (USD per 1K tokens)
PRICING = {
    # OpenAI
    "gpt-4": {"prompt": Decimal("0.03"), "completion": Decimal("0.06")},
    "gpt-4-turbo": {"prompt": Decimal("0.01"), "completion": Decimal("0.03")},
    "gpt-4-turbo-preview": {"prompt": Decimal("0.01"), "completion": Decimal("0.03")},
    "gpt-3.5-turbo": {"prompt": Decimal("0.0005"), "completion": Decimal("0.0015")},
    "gpt-3.5-turbo-16k": {"prompt": Decimal("0.003"), "completion": Decimal("0.004")},
    
    # Anthropic Claude
    "claude-3-opus": {"prompt": Decimal("0.015"), "completion": Decimal("0.075")},
    "claude-3-sonnet": {"prompt": Decimal("0.003"), "completion": Decimal("0.015")},
    "claude-3-haiku": {"prompt": Decimal("0.00025"), "completion": Decimal("0.00125")},
    
    # Google Gemini
    "gemini-pro": {"prompt": Decimal("0.0005"), "completion": Decimal("0.0015")},
    
    # Default (fallback)
    "default": {"prompt": Decimal("0.001"), "completion": Decimal("0.002")},
}


def get_model_pricing(model: str) -> Dict[str, Decimal]:
    """
    Get pricing for a model
    
    Args:
        model: Model name (e.g., "gpt-4", "claude-3-opus")
    
    Returns:
        Dict with "prompt" and "completion" prices per 1K tokens
    """
    # Exact match
    if model in PRICING:
        return PRICING[model]
    
    # Fuzzy match (e.g., "gpt-4-0613" -> "gpt-4")
    for key in PRICING.keys():
        if key in model:
            logger.info(f"Fuzzy matched model '{model}' to '{key}'")
            return PRICING[key]
    
    # Default fallback
    logger.warning(f"Unknown model '{model}', using default pricing")
    return PRICING["default"]


def calculate_cost(
    model: str,
    prompt_tokens: int,
    completion_tokens: int
) -> Decimal:
    """
    Calculate cost for a request
    
    Args:
        model: Model name
        prompt_tokens: Number of prompt tokens
        completion_tokens: Number of completion tokens
    
    Returns:
        Cost in USD (Decimal for precision)
    """
    pricing = get_model_pricing(model)
    
    prompt_cost = (Decimal(prompt_tokens) * pricing["prompt"]) / Decimal(1000)
    completion_cost = (Decimal(completion_tokens) * pricing["completion"]) / Decimal(1000)
    
    total_cost = prompt_cost + completion_cost
    
    return total_cost


def estimate_tokens(text: str) -> int:
    """
    Rough estimate of tokens in text
    
    Rule of thumb: 1 token ≈ 4 characters or 0.75 words
    """
    # Simple heuristic: 1 token per 4 characters
    return max(1, len(text) // 4)


def format_cost(cost: Decimal) -> str:
    """Format cost for display"""
    return f"${float(cost):.6f}"


# Example usage
if __name__ == "__main__":
    # Test calculations
    print("Cost Calculations:")
    print("-" * 50)
    
    models = ["gpt-4", "gpt-3.5-turbo", "claude-3-opus"]
    
    for model in models:
        cost = calculate_cost(model, prompt_tokens=100, completion_tokens=50)
        print(f"{model:20} -> {format_cost(cost)}")
    
    print("\nLarge request:")
    cost = calculate_cost("gpt-4", prompt_tokens=10000, completion_tokens=5000)
    print(f"GPT-4 (10K+5K tokens) -> {format_cost(cost)}")
