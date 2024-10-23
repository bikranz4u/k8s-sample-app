from flask import Flask, jsonify
import socket

app = Flask(__name__)


@app.route('/pod-ip', methods=['GET'])
def get_pod_ip():
    pod_ip = socket.gethostbyname(socket.gethostname())
    return jsonify({"pod_ip": pod_ip}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
