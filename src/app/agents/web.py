import redis
import json
import logging
import subprocess
from ..parsers.gobuster_parser import parse_gobuster_output
from ..parsers.ffuf_parser import parse_ffuf_output

logger = logging.getLogger(__name__)

def main():
    r = redis.Redis(host='redis', port=6379, decode_responses=True)
    logger.info("Web worker started")

    while True:
        try:
            job_data = r.blpop('jobs', timeout=0)
            if job_data:
                job = json.loads(job_data[1])
                if job.get('stage') == 'web':
                    logger.info(f"Processing web job {job['job_id']} for {job['target']}")

                    findings = []

                    # Gobuster
                    try:
                        cmd = ['gobuster', 'dir', '-u', f'http://{job["target"]}', '-w', '/app/wordlists/common.txt', '-q']
                        result = subprocess.run(
                            cmd,
                            capture_output=True,
                            text=True,
                            timeout=60
                        )
                        output = result.stdout + result.stderr
                        findings.extend(parse_gobuster_output(output))
                    except subprocess.TimeoutExpired:
                        logger.warning(f"Gobuster timed out for {job['target']}")
                    except Exception as e:
                        logger.warning(f"Gobuster failed: {e}")

                    # ffuf
                    try:
                        cmd = ['ffuf', '-u', f'http://{job["target"]}/FUZZ', '-w', '/app/wordlists/common.txt', '-mc', 'all', '-of', 'json']
                        result = subprocess.run(
                            cmd,
                            capture_output=True,
                            text=True,
                            timeout=60
                        )
                        output = result.stdout + result.stderr
                        findings.extend(parse_ffuf_output(output))
                    except subprocess.TimeoutExpired:
                        logger.warning(f"ffuf timed out for {job['target']}")
                    except Exception as e:
                        logger.warning(f"ffuf failed: {e}")

                    # Push result
                    result = {
                        'job_id': job['job_id'],
                        'stage': 'web',
                        'findings': [f.to_dict() for f in findings]
                    }
                    r.rpush('results', json.dumps(result))
                    logger.info(f"Web job {job['job_id']} completed")
        except Exception as e:
            logger.error(f"Error in web worker: {e}")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()