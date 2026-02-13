import json
from typing import List, Dict, Any
from ..shared.models import Finding
from ..shared.utils import safe_json_loads

def parse_ffuf_output(output: str) -> List[Finding]:
    findings = []
    try:
        data = safe_json_loads(output)
        if 'results' in data:
            for result in data['results']:
                path = result.get('url', '').split('/')[-1]  # FUZZ part
                status = result.get('status')
                if path and status:
                    finding = Finding(
                        type='endpoint',
                        data={'path': path, 'status': status, 'tool': 'ffuf'},
                        severity='low',
                        confidence=0.7
                    )
                    findings.append(finding)
    except Exception:
        pass  # If not JSON, skip
    return findings