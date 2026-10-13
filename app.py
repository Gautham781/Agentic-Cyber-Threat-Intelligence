
from flask import Flask, request, jsonify
from flask_cors import CORS
from orchestrator import investigate_ip

app = Flask(__name__)
CORS(app)


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "CTI API is running"})


@app.route("/api/investigate", methods=["POST"])
def investigate():
    data = request.get_json(silent=True) or {}
    ip = data.get("ip", "").strip()
    behavior = data.get("behavior", "").strip()

    if not ip:
        return jsonify({"error": "Please provide an IP address."}), 400

    try:
        result = investigate_ip(ip, behavior or None)
        return jsonify(result)
    except Exception as e:
        app.logger.exception("Investigation failed")
        return jsonify({"error": "Investigation failed. Check the backend terminal."}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
