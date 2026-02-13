import subprocess
import logging
from .tools import run_tool

logger = logging.getLogger(__name__)

class Worker:
    def execute(self, job: dict) -> str:
        target = job['target']
        logger.info(f"Executing scan on {target}")

        command = ['nmap', '-sV', target]
        try:
            output = run_tool(command, timeout=60)
            logger.info(f"Scan completed for {target}")
            return output
        except Exception as e:
            logger.error(f"Error executing scan on {target}: {e}")
            return f"Error: {str(e)}"