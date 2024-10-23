from flask import Flask, jsonify
import requests
import socket

app = Flask(__name__)


@app.route('/connect-b', methods=['GET'])
def connect_to_b():
    response = requests.get('https://app-b-service/pod-ip',
                            verify='/path/to/ca.crt')  # TLS communication
    return jsonify({"pod_ip_of_b": response.json()['pod_ip']}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
