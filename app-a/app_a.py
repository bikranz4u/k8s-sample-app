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
    app.run(host="0.0.0.0", port=5000)

# from flask import Flask, jsonify
# import requests
# import socket

# app = Flask(__name__)


# @app.route('/connect-b', methods=['GET'])
# def connect_to_b():
#     response = requests.get('https://app-b-service/pod-ip',
#                             verify='/path/to/ca.crt')  # TLS communication
#     return jsonify({"pod_ip_of_b": response.json()['pod_ip']}), 200


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
