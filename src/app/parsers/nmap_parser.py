import re
from typing import List, Dict, Any
from ..shared.models import Finding

def parse_nmap_output(output: str) -> List[Finding]:
    findings = []
    lines = output.split('\n')
    for line in lines:
        # Match lines like: 80/tcp open  http
        match = re.match(r'(\d+)/tcp\s+open\s+(\w+)', line.strip())
        if match:
            port = int(match.group(1))
            service = match.group(2)
            finding = Finding(
                type='port',
                data={'port': port, 'service': service},
                severity='low',  # default, will be reassigned by validator
                confidence=0.9
            )
            findings.append(finding)
    return findings