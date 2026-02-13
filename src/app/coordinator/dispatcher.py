import redis
import json
import threading
import logging
from .state import StateManager
from .planner import Planner
from ..agents.validator import ValidatorAgent
from ..shared.models import Job

logger = logging.getLogger(__name__)

class Dispatcher:
    def __init__(self):
        self.redis = redis.Redis(host='redis', port=6379, decode_responses=True)
        self.state = StateManager()
        self.validator = ValidatorAgent()
        self.listener_thread = threading.Thread(target=self.result_listener, daemon=True)
        self.listener_thread.start()

    def enqueue_job(self, job: Job):
        job_data = {
            'job_id': job.job_id,
            'target': job.target,
            'profile': job.profile,
            'stage': job.stage
        }
        self.redis.rpush('jobs', json.dumps(job_data))
        logger.info(f"Enqueued job {job.job_id} for stage {job.stage}")

    def result_listener(self):
        logger.info("Result listener started")
        while True:
            try:
                result_data = self.redis.blpop('results', timeout=0)
                if result_data:
                    result = json.loads(result_data[1])
                    job_id = result['job_id']
                    stage = result['stage']
                    findings = result.get('findings', [])

                    job = self.state.get_job(job_id)
                    if job:
                        # Store findings
                        job.results[stage] = findings
                        job.status = f"{stage}_done"
                        job.updated_at = job.updated_at  # or update to now

                        # Check next stage
                        next_stage = Planner.get_next_stage(stage, job.profile)
                        if next_stage == 'complete':
                            # Run validator
                            all_findings = []
                            for s in ['recon', 'web', 'vuln']:
                                if s in job.results:
                                    all_findings.extend(job.results[s])
                            validated = self.validator.validate(all_findings)
                            job.results['validated'] = [f.to_dict() for f in validated]
                            job.status = 'complete'
                            job.stage = 'complete'
                        else:
                            job.stage = next_stage
                            self.enqueue_job(job)

                        self.state.save_job(job)
                        logger.info(f"Processed result for job {job_id}, next stage: {next_stage}")
            except Exception as e:
                logger.error(f"Error in result listener: {e}")

    def start_scan(self, target: str, profile: str) -> str:
        job = Job.new(target, profile)
        self.state.save_job(job)
        self.enqueue_job(job)
        return job.job_id