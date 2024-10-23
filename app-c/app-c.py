from flask import Flask, jsonify
import os

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello from Application C!"


@app.route('/pod-ip')
def pod_ip():
    return jsonify({"pod_ip": os.getenv("POD_IP", "Unknown")})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
