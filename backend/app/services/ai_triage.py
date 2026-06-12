"""
AI triage service for dark web intelligence reports.

Uses the Anthropic Claude API to produce structured threat assessments.
Falls back gracefully when ANTHROPIC_API_KEY is not configured or the
API call fails (e.g., in CI/dev without a real key).
"""

import json
import os
from typing import Optional

import anthropic

from ..core.config import settings

# Lazy client — only instantiate once the first call is made so that the
# app can start even if ANTHROPIC_API_KEY is a placeholder.
_client: Optional[anthropic.AsyncAnthropic] = None


def _get_client() -> "anthropic.AsyncAnthropic":
    global _client
    if _client is None:
        _client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
    return _client


AI_TRIAGE_PROMPT = """
You are a Senior Dark Web Intelligence Analyst. Analyze the following content found on a hidden service.
Your goal is to provide a high-fidelity triage report for an executive security dashboard.

REQUIRED ANALYSIS:
1. Criticality: (Critical, High, Medium, Low)
   - Critical: Confirmed active zero-day exploits, current government/corporate credentials, or massive PII leaks.
   - High: Targeted threats against specific organizations, ransomware payment portals.
   - Medium: General dark web forums, generic data leaks.
   - Low: Noise, scams, expired content.
2. Threat Category: (Data Leak, Ransomware, APT Activity, Financial Fraud, Zero-Day, Other)
3. Technical Summary: A precise 2-sentence summary. Avoid fluff.
4. Mitigation: Concrete, actionable steps for a CISO.
5. Confidence Score: (0.0 to 1.0) based on the clarity of the evidence.

Edge Case Handling:
- If the content is encrypted or corrupted, mark Criticality as 'Low' and state 'Encrypted/Corrupted content' in the Summary.
- If the content is a known scam (e.g., 'get rich quick' onion sites), mark Criticality as 'Low'.

Format the response as a valid JSON object with keys:
  "criticality", "threat_type", "summary", "action_item", "confidence"

Content:
{content}
"""


async def triage_content(content: str) -> dict:
    """
    Send content to Claude for threat triage.

    Returns a structured dict on success.  On any failure (no API key, network
    error, malformed response) returns a safe fallback dict so callers never
    receive an exception.
    """
    # Guard: if the key is still the placeholder, skip the API call.
    api_key = settings.ANTHROPIC_API_KEY
    if not api_key or api_key in ("your-api-key-here", ""):
        return _fallback("ANTHROPIC_API_KEY not configured", confidence=0.0)

    prompt = AI_TRIAGE_PROMPT.format(content=content[:4000])  # cap to avoid token explosion

    try:
        client = _get_client()
        response = await client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        raw_text = response.content[0].text.strip()

        # Strip markdown code fences if present
        if raw_text.startswith("```"):
            raw_text = raw_text.split("```")[1]
            if raw_text.startswith("json"):
                raw_text = raw_text[4:]

        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            return {
                "criticality": "Medium",
                "threat_type": "Other",
                "summary": raw_text[:300],
                "action_item": "Review manually — AI response was not valid JSON",
                "confidence": 0.5,
            }

    except anthropic.AuthenticationError:
        return _fallback("Invalid Anthropic API key", confidence=0.0)
    except Exception as exc:
        return _fallback(f"Error during triage: {exc}", confidence=0.0)


def _fallback(reason: str, confidence: float = 0.0) -> dict:
    return {
        "criticality": "Low",
        "threat_type": "Other",
        "summary": reason,
        "action_item": "Check AI service configuration and connectivity",
        "confidence": confidence,
    }
