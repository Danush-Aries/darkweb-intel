import re
from typing import Dict

def calculate_threat_score(content: str) -> float:
    """
    God-Tier Threat Scoring Algorithm
    Uses weighted regex patterns and density analysis to prevent false positives.
    """
    if not content:
        return 0.0

    score = 0.0

    # High-confidence patterns (Critical)
    critical_indicators = {
        r"(?i)credit\s*card|cvv|expiry\s*date": 40,
        r"(?i)password\s*list|combo\s*list|leak\s*db": 35,
        r"(?i)0day|zero-day|rce\s*exploit": 35,
    }

    # Medium-confidence patterns (Warning)
    warning_indicators = {
        r"(?i)admin\s*login|root\s*access": 20,
        r"(?i)ransomware|lockbit|clop|blackcat": 20,
        r"(?i)payload|shellcode|backdoor": 15,
        r"(?i)pii|social\s*security|passport": 15,
    }

    # Low-confidence/General patterns (Noise)
    noise_indicators = {
        r"(?i)email|phone|contact": 5,
        r"(?i)darkweb|onion|torrent": 2,
    }

    content_lower = content.lower()

    # Calculate weighted sum
    for pattern, weight in critical_indicators.items():
        if re.search(pattern, content_lower):
            score += weight

    for pattern, weight in warning_indicators.items():
        if re.search(pattern, content_lower):
            score += weight

    for pattern, weight in noise_indicators.items():
        if re.search(pattern, content_lower):
            score += weight

    # Density Penalty: If the content is too short to be a meaningful leak, penalize score
    if len(content) < 100:
        score *= 0.5

    # Normalize score to 0-100
    return float(min(100.0, score))
