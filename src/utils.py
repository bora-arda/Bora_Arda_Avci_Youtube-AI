import hashlib
import json


def safe_json_parse(text):
    """
    Ensures album/song lists returned by LLM parse safely.
    Strips markdown, extra whitespace, and forces valid JSON extraction.
    """
    try:
        # Remove markdown code blocks if present
        text = text.strip()
        if text.startswith("```"):
            # Remove first line with ```json or ```
            lines = text.split("\n")
            text = "\n".join(lines[1:])
        if text.endswith("```"):
            text = text[:-3]
        
        # Find JSON object
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1:
            raise ValueError("No JSON object found")
        
        cleaned = text[start:end+1]
        return json.loads(cleaned)
    except Exception as e:
        raise ValueError(f"Failed to parse JSON from LLM response: {str(e)}")


def md5_hash(text: str) -> str:
    """
    Compute MD5 hash of a given string.
    """
    return hashlib.md5(text.encode("utf-8")).hexdigest()
