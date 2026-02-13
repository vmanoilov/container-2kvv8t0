import json
from typing import List, Dict, Any
from ..shared.models import Finding
from ..shared.utils import safe_json_loads

def parse_nikto_output(output: str) -> List[Finding]:
    findings = []
    try:
        data = safe_json_loads(output)
        if isinstance(data, list):
            for item in data:
                if 'msg' in item and 'url' in item:
                    finding = Finding(
                        type='vuln',
                        data={'message': item['msg'], 'url': item['url'], 'tool': 'nikto'},
                        severity='medium',  # nikto findings are often medium
                        confidence=0.8
                    )
                    findings.append(finding)
    except Exception:
        pass
    return findings