"""
Jailbreak Detection Module

Detects prompt injection and jailbreak attempts using pattern matching
and machine learning techniques.
"""

import re
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class JailbreakResult:
    """Result from jailbreak detection"""
    is_jailbreak: bool
    confidence: float
    risk_level: str  # low, medium, high
    matched_patterns: List[str]
    explanation: str


class JailbreakDetector:
    """
    Detects jailbreak attempts including:
    - Prompt injection
    - Role-play attempts  
    - Instruction override
    - Hypothetical scenarios
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.threshold = self.config.get('threshold', 0.7)
        
        # Jailbreak patterns
        self.jailbreak_patterns = {
            'instruction_injection': [
                r'ignore.*previous.*instruction',
                r'forget.*everything.*above',
                r'new.*instruction',
                r'system.*message',
            ],
            'roleplay': [
                r'pretend.*you.*are',
                r'act.*as.*if',
                r'roleplay.*as',
                r'imagine.*you.*are',
            ],
            'hypothetical': [
                r'in.*a.*world.*where',
                r'hypothetically',
                r'what.*if.*there.*were.*no.*rules',
            ],
            'developer_mode': [
                r'developer.*mode',
                r'debug.*mode',
                r'admin.*mode',
            ]
        }
        
        # Confidence weights
        self.pattern_weights = {
            'instruction_injection': 0.9,
            'developer_mode': 0.85,
            'roleplay': 0.6,
            'hypothetical': 0.4,
        }
    
    def detect(self, text: str) -> JailbreakResult:
        """Detect jailbreak attempts in text"""
        text_lower = text.lower()
        matched_patterns = []
        confidence_scores = []
        
        # Pattern matching
        for category, patterns in self.jailbreak_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    matched_patterns.append(f"{category}: {pattern}")
                    confidence_scores.append(self.pattern_weights.get(category, 0.5))
        
        # Calculate confidence
        confidence = max(confidence_scores) if confidence_scores else 0.0
        is_jailbreak = confidence >= self.threshold
        
        # Risk level
        if confidence >= 0.8:
            risk_level = "high"
        elif confidence >= 0.5:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        # Explanation
        if is_jailbreak:
            explanation = f"Jailbreak detected (confidence: {confidence:.2f})"
        else:
            explanation = "No jailbreak patterns detected"
        
        return JailbreakResult(
            is_jailbreak=is_jailbreak,
            confidence=confidence,
            risk_level=risk_level,
            matched_patterns=matched_patterns,
            explanation=explanation
        )
