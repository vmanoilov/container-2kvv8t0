import redis
import json
import logging
import subprocess
from ..parsers.nikto_parser import parse_nikto_output

logger = logging.getLogger(__name__)

def main():
    r = redis.Redis(host='redis', port=6379, decode_responses=True)
    logger.info("Vuln worker started")

    while True:
        try:
            job_data = r.blpop('jobs', timeout=0)
            if job_data:
                job = json.loads(job_data[1])
                if job.get('stage') == 'vuln':
                    logger.info(f"Processing vuln job {job['job_id']} for {job['target']}")

                    # Nikto
                    try:
                        cmd = ['nikto', '-host', f'http://{job["target"]}', '-Format', 'json']
                        result = subprocess.run(
                            cmd,
                            capture_output=True,
                            text=True,
                            timeout=120
                        )
                        output = result.stdout + result.stderr
                        findings = parse_nikto_output(output)
                    except subprocess.TimeoutExpired:
                        logger.warning(f"Nikto timed out for {job['target']}")
                        findings = []
                    except Exception as e:
                        logger.warning(f"Nikto failed: {e}")
                        findings = []

                    # Push result
                    result = {
                        'job_id': job['job_id'],
                        'stage': 'vuln',
                        'findings': [f.to_dict() for f in findings]
                    }
                    r.rpush('results', json.dumps(result))
                    logger.info(f"Vuln job {job['job_id']} completed")
        except Exception as e:
            logger.error(f"Error in vuln worker: {e}")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()