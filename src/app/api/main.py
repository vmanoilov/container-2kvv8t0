from flask import Flask, request, jsonify
import logging
from ..coordinator.dispatcher import Dispatcher
from ..coordinator.state import StateManager
from ..shared.utils import validate_target

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_dispatcher():
    if not hasattr(app, 'dispatcher'):
        app.dispatcher = Dispatcher()
    return app.dispatcher

def get_state():
    if not hasattr(app, 'state'):
        app.state = StateManager()
    return app.state

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    if not data or 'target' not in data:
        return jsonify({"error": "Missing 'target'"}), 400

    target = data['target']
    profile = data.get('profile', 'standard')

    if not validate_target(target):
        return jsonify({"error": "Invalid target"}), 400

    if profile not in ['quick', 'standard', 'deep']:
        return jsonify({"error": "Invalid profile"}), 400

    try:
        job_id = get_dispatcher().start_scan(target, profile)
        return jsonify({"job_id": job_id}), 201
    except Exception as e:
        logger.error(f"Error starting scan: {e}")
        return jsonify({"error": "Internal error"}), 500

@app.route('/job/<job_id>', methods=['GET'])
def get_job(job_id: str):
    job = get_state().get_job(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    return jsonify(job.to_dict())

@app.route('/report/<job_id>', methods=['GET'])
def get_report(job_id: str):
    job = get_state().get_job(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    if job.status != 'complete':
        return jsonify({"error": "Report not ready"}), 202

    return jsonify(job.to_dict())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)