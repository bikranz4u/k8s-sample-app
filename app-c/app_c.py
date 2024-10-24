from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({"message": "Hello from Application C !", "pod_ip": os.getenv("POD_IP", "Unknown")})

@app.route('/pod-ip')
def pod_ip():
    return jsonify({"pod_ip": os.getenv("POD_IP", "Unknown")})


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)