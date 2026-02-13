from flask import Flask, request, jsonify
import logging
from .coordinator import Coordinator

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

coordinator = Coordinator()

@app.route('/health', methods=['GET'])
def health():
    logger.info("Health check requested")
    return jsonify({"status": "OK"}), 200

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    if not data or 'target' not in data:
        return jsonify({"error": "Missing 'target' in request body"}), 400

    target = data['target']
    logger.info(f"Scan requested for target: {target}")

    try:
        result = coordinator.dispatch(target)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error during scan: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)