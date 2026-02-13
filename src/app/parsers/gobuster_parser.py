import re
from typing import List, Dict, Any
from ..shared.models import Finding

def parse_gobuster_output(output: str) -> List[Finding]:
    findings = []
    lines = output.split('\n')
    for line in lines:
        # Gobuster output: /admin (Status: 200)
        match = re.match(r'/(\S+)\s+\(Status:\s+(\d+)\)', line.strip())
        if match:
            path = match.group(1)
            status = int(match.group(2))
            finding = Finding(
                type='endpoint',
                data={'path': path, 'status': status, 'tool': 'gobuster'},
                severity='low',
                confidence=0.8
            )
            findings.append(finding)
    return findings