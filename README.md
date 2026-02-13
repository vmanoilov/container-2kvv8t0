# MAPTA v2 - Multi-Agent Pentesting Framework

MAPTA v2 is a distributed, multi-container pentesting framework using Redis for job queuing and multiple specialized worker agents.

## Architecture

- **Coordinator**: Flask API server handling scan requests and result aggregation
- **Redis**: Message broker for job and result queues
- **Worker Agents**:
  - Recon: Nmap port scanning
  - Web: Gobuster and ffuf directory enumeration
  - Vuln: Nikto vulnerability scanning

## Quick Start

1. Clone the repository
2. Start the services: `docker-compose up`
3. API is available at http://localhost:5000

## API Usage

### Start a Scan
```bash
curl -X POST http://localhost:5000/scan \
  -H "Content-Type: application/json" \
  -d '{"target": "example.com", "profile": "standard"}'
```

Profiles:
- `quick`: Recon only
- `standard`: Recon + Web
- `deep`: Recon + Web + Vuln

Response:
```json
{"job_id": "uuid-here"}
```

### Check Job Status
```bash
curl http://localhost:5000/job/<job_id>
```

### Get Full Report
```bash
curl http://localhost:5000/report/<job_id>
```

## Local Development

1. Install dependencies: `pip install -r src/requirements.txt`
2. Run tests: `python -m pytest tests/`
3. Start services: `docker-compose up`

## Deployment

The framework is designed for containerized deployment with automatic CI/CD pipelines preserved.
If you make changes to `Dockerfile`, then you need to rebuild your container image. To rebuild the container image:
```
docker-compose build
# or 
docker-compose up --build
```

## Testing

Run unit tests:
```bash
python -m pytest tests/
```

## Security Features

- Input validation for targets and profiles
- Timeout enforcement on all tool executions
- Direct subprocess execution with proper error handling
- No shell=True usage
- Logging for monitoring and debugging

## Questions

- How was this built? [All code is here](https://github.com/KarmaComputing/container-hosting)
- How can I use a customized port number/change the port number listened on? You don't need to do this if you use the quickstarts. But if you do want to alter the port: Edit your `Dockerfile` and change `EXPOSE` to the port number you want your app to listen on. Understand that all apps go through the proxy (nginx) listening on port `80` and `443`, requests to your app get proxied (based on your hostname) to the port number you put after `EXPOSE` in your your `Dockerfile`. For example `EXPOSE 3000` means you want the Dokku nginx proxy to forward port `80` and `443` connections to port `3000`. You still need to make your application listen on your chosen port.
