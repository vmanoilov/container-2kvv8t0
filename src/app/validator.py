import re
import logging

logger = logging.getLogger(__name__)

class Validator:
    def validate(self, raw_output: str) -> dict:
        logger.info("Validating raw output")
        open_ports = []

        # Simple parsing of nmap output
        # Look for lines like: 80/tcp open  http
        lines = raw_output.split('\n')
        for line in lines:
            match = re.match(r'(\d+)/tcp\s+open\s+(\w+)', line.strip())
            if match:
                port = int(match.group(1))
                service = match.group(2)
                open_ports.append({"port": port, "service": service})

        logger.info(f"Found {len(open_ports)} open ports")
        return {"open_ports": open_ports}