import json
from typing import Any, Dict

def validate_target(target: str) -> bool:
    """Basic validation for target (IP or domain)"""
    import re
    # Simple regex for IP or domain
    ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    domain_pattern = r'^[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$|^[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(ip_pattern, target) or re.match(domain_pattern, target))

def safe_json_loads(s: str) -> Dict[str, Any]:
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        return {}

def safe_json_dumps(obj: Any) -> str:
    try:
        return json.dumps(obj)
    except (TypeError, ValueError):
        return "{}"