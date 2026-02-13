import subprocess
import logging

logger = logging.getLogger(__name__)

def run_tool(command: list[str], timeout: int = 60) -> str:
    logger.info(f"Running tool: {' '.join(command)}")
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode == 0:
            return result.stdout
        else:
            error_msg = f"Command failed with return code {result.returncode}: {result.stderr}"
            logger.error(error_msg)
            return error_msg
    except subprocess.TimeoutExpired:
        error_msg = f"Command timed out after {timeout} seconds"
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        return error_msg