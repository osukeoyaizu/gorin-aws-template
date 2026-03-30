import json
import boto3
from flask import Flask, render_template, request, jsonify
import service
import logging
import os

app = Flask(__name__)

@app.route('/api/item/<id>', methods=['GET'])
def get_item_byid(id):
    print(id)
    print(type(id))
    data = service.get_data_byid(id)
    if data:
        return jsonify({'response':data}), 200
    else:
        return jsonify({'response':'Not Found'}), 404


@app.route('/api/item', methods=['POST'])
def post_order():   

    ## JSON 形式の取得
    data = request.get_json()

    response = service.post_data(data)   
    return jsonify({'message': 'created'}), 201

if __name__ == '__main__':
    app.run(debug=True)
