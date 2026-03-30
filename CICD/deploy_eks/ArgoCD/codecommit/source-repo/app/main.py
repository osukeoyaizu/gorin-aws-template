import json
import boto3
from flask import Flask, render_template, request, jsonify
import service
import logging
import os

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    response = service.get_data()
    return jsonify({'result':response}), 200


@app.route('/test', methods=['GET'])
def test():
    return jsonify({'result':'test'}), 200


@app.route('/health', methods=['GET'])
def health():
    return "Hello, world!"

if __name__ == '__main__':  

    app.run(host='0.0.0.0', port=8080, threaded=True)
