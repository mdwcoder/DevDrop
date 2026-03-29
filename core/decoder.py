import json
import base64
from typing import Any

def decode_payload(payload_b64: str) -> dict[str, Any]:
    """Decodes a Base64 string to JSON dictionary."""
    try:
        json_bytes = base64.b64decode(payload_b64.encode('utf-8'))
        json_str = json_bytes.decode('utf-8')
        return json.loads(json_str)
    except Exception as e:
        raise ValueError(f"Failed to decode payload: {e}")
