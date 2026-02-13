from dataclasses import dataclass, asdict
from typing import Dict, List, Any
import uuid
import json
from datetime import datetime

@dataclass
class Job:
    job_id: str
    target: str
    profile: str  # quick|standard|deep
    stage: str  # recon|web|vuln|complete
    status: str  # pending|running|recon_done|web_done|vuln_done|complete|error
    created_at: datetime
    updated_at: datetime
    results: Dict[str, Any]  # structured results

    @classmethod
    def new(cls, target: str, profile: str) -> 'Job':
        now = datetime.utcnow()
        return cls(
            job_id=str(uuid.uuid4()),
            target=target,
            profile=profile,
            stage='recon',
            status='pending',
            created_at=now,
            updated_at=now,
            results={}
        )

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['created_at'] = self.created_at.isoformat()
        d['updated_at'] = self.updated_at.isoformat()
        return d

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'Job':
        d['created_at'] = datetime.fromisoformat(d['created_at'])
        d['updated_at'] = datetime.fromisoformat(d['updated_at'])
        return cls(**d)

@dataclass
class Finding:
    type: str  # port, endpoint, vuln
    data: Dict[str, Any]
    severity: str  # low|medium|high
    confidence: float  # 0-1

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)