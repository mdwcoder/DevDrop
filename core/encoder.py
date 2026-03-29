import json
import base64
from typing import Any

def encode_payload(data: dict[str, Any]) -> str:
    """Encodes a dictionary to JSON and then Base64 string."""
    json_str = json.dumps(data)
    return base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
