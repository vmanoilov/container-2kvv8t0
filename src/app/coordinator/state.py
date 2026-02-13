import sqlite3
import json
from typing import Optional, Dict, Any
from ..shared.models import Job

class StateManager:
    def __init__(self, db_path: str = '/app/jobs.db'):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY,
                    target TEXT,
                    profile TEXT,
                    stage TEXT,
                    status TEXT,
                    created_at TEXT,
                    updated_at TEXT,
                    results TEXT
                )
            ''')

    def save_job(self, job: Job):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO jobs
                (job_id, target, profile, stage, status, created_at, updated_at, results)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                job.job_id,
                job.target,
                job.profile,
                job.stage,
                job.status,
                job.created_at.isoformat(),
                job.updated_at.isoformat(),
                json.dumps(job.results)
            ))

    def get_job(self, job_id: str) -> Optional[Job]:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute('SELECT * FROM jobs WHERE job_id = ?', (job_id,)).fetchone()
            if row:
                data = {
                    'job_id': row[0],
                    'target': row[1],
                    'profile': row[2],
                    'stage': row[3],
                    'status': row[4],
                    'created_at': row[5],
                    'updated_at': row[6],
                    'results': json.loads(row[7])
                }
                return Job.from_dict(data)
        return None

    def update_job_results(self, job_id: str, stage: str, results: Dict[str, Any]):
        job = self.get_job(job_id)
        if job:
            job.results[stage] = results
            job.updated_at = job.updated_at  # keep same, or update to now
            self.save_job(job)