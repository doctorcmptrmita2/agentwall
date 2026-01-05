"""
Loop Detection Service

Detects when an agent is stuck in a loop:
1. Exact repetition (same prompt/response)
2. Semantic similarity (similar meaning)
3. Pattern detection (oscillating between states)

MVP: Start with exact + simple similarity
Future: Add embedding-based semantic similarity
"""

import hashlib
import logging
from typing import Optional
from dataclasses import dataclass

from config import settings

logger = logging.getLogger(__name__)


@dataclass
class LoopCheckResult:
    """Result of loop detection check"""
    is_loop: bool = False
    confidence: float = 0.0
    loop_type: str = ""  # exact, similar, pattern
    message: str = ""


class LoopDetector:
    """
    Detects repetitive patterns in agent behavior
    
    MVP Implementation:
    - Exact match detection (hash comparison)
    - Simple text similarity (Jaccard)
    
    Future (v2):
    - Embedding-based similarity (sentence-transformers)
    - Pattern detection (state machine analysis)
    """
    
    def __init__(self):
        self.similarity_threshold = settings.SIMILARITY_THRESHOLD
    
    def check_loop(
        self,
        current_prompt: str,
        current_response: str,
        recent_prompts: list[str],
        recent_responses: list[str],
    ) -> LoopCheckResult:
        """
        Check if current interaction indicates a loop
        
        Args:
            current_prompt: The prompt being sent
            current_response: The response received (empty for pre-check)
            recent_prompts: Last N prompts in this run
            recent_responses: Last N responses in this run
        
        Returns:
            LoopCheckResult with detection details
        """
        result = LoopCheckResult()
        
        if not recent_prompts:
            return result
        
        # Check 1: Exact prompt repetition
        current_hash = self._hash_text(current_prompt)
        for i, prev_prompt in enumerate(recent_prompts):
            if self._hash_text(prev_prompt) == current_hash:
                result.is_loop = True
                result.confidence = 1.0
                result.loop_type = "exact_prompt"
                result.message = f"Exact prompt repetition detected (matches step -{len(recent_prompts)-i})"
                logger.warning(f"Loop detected: exact prompt match")
                return result
        
        # Check 2: Exact response repetition (if we have response)
        if current_response and recent_responses:
            response_hash = self._hash_text(current_response)
            for i, prev_response in enumerate(recent_responses):
                if self._hash_text(prev_response) == response_hash:
                    result.is_loop = True
                    result.confidence = 1.0
                    result.loop_type = "exact_response"
                    result.message = f"Exact response repetition detected"
                    logger.warning(f"Loop detected: exact response match")
                    return result
        
        # Check 3: High similarity (Jaccard)
        for prev_prompt in recent_prompts[-3:]:  # Check last 3
            similarity = self._jaccard_similarity(current_prompt, prev_prompt)
            if similarity >= self.similarity_threshold:
                result.is_loop = True
                result.confidence = similarity
                result.loop_type = "similar_prompt"
                result.message = f"Similar prompt detected (similarity: {similarity:.2%})"
                logger.warning(f"Loop detected: similar prompt ({similarity:.2%})")
                return result
        
        # Check 4: Oscillation pattern (A->B->A->B)
        if len(recent_prompts) >= 3:
            if self._detect_oscillation(recent_prompts + [current_prompt]):
                result.is_loop = True
                result.confidence = 0.9
                result.loop_type = "oscillation"
                result.message = "Oscillation pattern detected (A->B->A->B)"
                logger.warning("Loop detected: oscillation pattern")
                return result
        
        return result
    
    def _hash_text(self, text: str) -> str:
        """Create hash of normalized text"""
        normalized = text.lower().strip()
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def _jaccard_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate Jaccard similarity between two texts
        
        Simple but effective for detecting near-duplicates
        """
        # Tokenize (simple word split)
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union)
    
    def _detect_oscillation(self, prompts: list[str]) -> bool:
        """
        Detect A->B->A->B pattern
        
        Returns True if last 4 prompts show oscillation
        """
        if len(prompts) < 4:
            return False
        
        last_4 = prompts[-4:]
        hashes = [self._hash_text(p) for p in last_4]
        
        # Check if pattern is A-B-A-B
        if hashes[0] == hashes[2] and hashes[1] == hashes[3] and hashes[0] != hashes[1]:
            return True
        
        return False


# Singleton instance
loop_detector = LoopDetector()
