import uuid
import logging
from collections import deque
from .agents.worker import Worker
from .validator import Validator

logger = logging.getLogger(__name__)

class Coordinator:
    def __init__(self):
        self.queue = deque()
        self.worker = Worker()
        self.validator = Validator()

    def dispatch(self, target: str) -> dict:
        job_id = str(uuid.uuid4())
        job = {"job_id": job_id, "target": target}

        # Enqueue job
        self.queue.append(job)
        logger.info(f"Enqueued job {job_id} for target {target}")

        # Synchronously execute
        try:
            raw_output = self.worker.execute(job)
            results = self.validator.validate(raw_output)
        except Exception as e:
            logger.error(f"Error processing job {job_id}: {e}")
            results = {"error": str(e)}

        # Dequeue
        self.queue.popleft()

        return {
            "job_id": job_id,
            "target": target,
            "results": results
        }