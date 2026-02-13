from typing import List, Dict, Any
from ..shared.models import Finding

class ValidatorAgent:
    @staticmethod
    def validate(findings: List[Finding]) -> List[Finding]:
        # Deduplicate
        seen = set()
        unique_findings = []
        for f in findings:
            key = (f.type, str(f.data))
            if key not in seen:
                seen.add(key)
                unique_findings.append(f)

        # Assign severity
        for f in unique_findings:
            if f.type == 'port':
                port = f.data.get('port')
                if port in [22, 3389]:  # SSH, RDP
                    f.severity = 'medium'
                elif port in [80, 443]:
                    f.severity = 'low'
                else:
                    f.severity = 'low'
            elif f.type == 'endpoint':
                path = f.data.get('path', '').lower()
                if any(word in path for word in ['admin', 'config', 'backup', 'db']):
                    f.severity = 'medium'
                else:
                    f.severity = 'low'
            elif f.type == 'vuln':
                msg = f.data.get('message', '').lower()
                if any(word in msg for word in ['default', 'weak', 'exposed', 'vulnerable']):
                    f.severity = 'high'
                else:
                    f.severity = 'medium'

        return unique_findings