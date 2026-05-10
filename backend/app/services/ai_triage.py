import anthropic
import json
from ..core.config import settings

client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

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

Format the response as a valid JSON object with keys: "criticality", "threat_type", "summary", "action_item", "confidence".

Content:
{content}
"""

async def triage_content(content: str):
    prompt = AI_TRIAGE_PROMPT.format(content=content)
    try:
        response = await client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        raw_text = response.content[0].text
        try:
            parsed = json.loads(raw_text)
            return parsed
        except json.JSONDecodeError:
            return {
                "criticality": "Medium",
                "threat_type": "Other",
                "summary": raw_text[:200],
                "action_item": "Review manually - AI response not in JSON format",
                "confidence": 0.6
            }
    except Exception as e:
        return {
            "criticality": "Low",
            "threat_type": "Other",
            "summary": f"Error during triage: {str(e)}",
            "action_item": "Check AI service connectivity",
            "confidence": 0.0
        }
