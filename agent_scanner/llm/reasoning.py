import os
import json
from groq import Groq
from pydantic import BaseModel
from typing import Optional


client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class LLMResponse(BaseModel):
    attack_simulation: str
    impact: str
    secure_fix: str
    severity: str


def generate_reasoning(finding: dict) -> Optional[LLMResponse]:
    prompt = f"""
You are a senior security engineer.

Analyze this vulnerability:

Type: {finding['type']}
File: {finding['file']}
Line: {finding['line']}
Code: {finding['code']}

Respond ONLY in valid JSON:

{{
  "attack_simulation": "...",
  "impact": "...",
  "secure_fix": "...",
  "severity": "HIGH/MEDIUM/LOW"
}}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a senior security engineer."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )

        text = response.choices[0].message.content.strip()

        # Remove markdown wrapping if present
        if text.startswith("```"):
            text = text.split("```")[1].strip()

        data = json.loads(text)
        return LLMResponse(**data)

    except Exception as e:
        print(f"LLM error: {e}")
        return None
