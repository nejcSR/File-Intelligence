import json
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

EXTRACTION_PROMPT = """
You are a document analysis AI. Analyze the following document text and extract structured information.

Return ONLY a valid JSON object with no extra text, no markdown, no backticks. Just raw JSON.

The JSON must follow this exact structure:
{{
    "document_type": "invoice|contract|resume|unknown",
    "key_fields": {{
        "date": null,
        "parties_involved": [],
        "total_amount": null,
        "currency": null,
        "key_terms": [],
        "important_dates": []
    }},
    "summary": "2-3 sentence summary of the document",
    "anomalies": [],
    "confidence": "high|medium|low"
}}

Rules:
- document_type: identify what kind of document this is
- key_fields: extract whatever is relevant for the document type
- anomalies: list anything suspicious, missing, or inconsistent
- confidence: how confident you are in the extraction
- If a field is not applicable, use null or empty list

Document text:
{text}
"""

def extract_document(text: str) -> dict:
    if not text or len(text.strip()) == 0:
        return {
            "document_type": "unknown",
            "key_fields": {},
            "summary": "No text could be extracted from this document.",
            "anomalies": ["Document appears to be empty or unreadable"],
            "confidence": "low"
        }

    # Truncate if too long for context window
    max_chars = 6000
    if len(text) > max_chars:
        text = text[:max_chars] + "\n... [document truncated]"

    prompt = EXTRACTION_PROMPT.format(text=text)

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=1000
        )

        raw = response.choices[0].message.content.strip()

        # Strip markdown fences if model adds them anyway
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        result = json.loads(raw)
        return result

    except json.JSONDecodeError:
        return {
            "document_type": "unknown",
            "key_fields": {},
            "summary": "AI returned an unparseable response.",
            "anomalies": ["Extraction failed — could not parse AI response"],
            "confidence": "low"
        }
    except Exception as e:
        return {
            "document_type": "unknown",
            "key_fields": {},
            "summary": f"Extraction error: {str(e)}",
            "anomalies": [f"System error: {str(e)}"],
            "confidence": "low"
        }