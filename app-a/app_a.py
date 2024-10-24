from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello from Application A!"


@app.route('/connect-b')
def connect_b():
    try:
        # Call Application B and return its pod IP
        response = requests.get('http://app-b:5000')
        return jsonify({"message": "Connected to Application B", "app_b_response": response.json()})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route('/pod-ip')
def pod_ip():
    return jsonify({"pod_ip": os.getenv("POD_IP", "Unknown")})


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
