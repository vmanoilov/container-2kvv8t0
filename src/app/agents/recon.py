import redis
import json
import logging
import subprocess
from ..parsers.nmap_parser import parse_nmap_output

logger = logging.getLogger(__name__)

def main():
    r = redis.Redis(host='redis', port=6379, decode_responses=True)
    logger.info("Recon worker started")

    while True:
        try:
            # Block for job
            job_data = r.blpop('jobs', timeout=0)
            if job_data:
                job = json.loads(job_data[1])
                if job.get('stage') == 'recon':
                    logger.info(f"Processing recon job {job['job_id']} for {job['target']}")

                    # Run nmap
                    cmd = ['nmap', '-sV', '-T4', '--top-ports', '200', job['target']]
                    try:
                        result = subprocess.run(
                            cmd,
                            capture_output=True,
                            text=True,
                            timeout=120
                        )
                        output = result.stdout + result.stderr
                        findings = parse_nmap_output(output)
                    except subprocess.TimeoutExpired:
                        logger.error(f"Nmap timed out for {job['target']}")
                        findings = []
                    except Exception as e:
                        logger.error(f"Error running nmap: {e}")
                        findings = []

                    # Push result
                    result = {
                        'job_id': job['job_id'],
                        'stage': 'recon',
                        'findings': [f.to_dict() for f in findings]
                    }
                    r.rpush('results', json.dumps(result))
                    logger.info(f"Recon job {job['job_id']} completed")
        except Exception as e:
            logger.error(f"Error in recon worker: {e}")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()