import os
import json
import requests

API_URL = 'https://xxxx/api'


def get_data():
    try:
        response = requests.get(API_URL)
        if response.ok:
            return json.loads(response.json())
        else:
            return None
    
    except Exception as e:
        raise e


def get_data(id):
    try:
        params = {'id': id}
        response = requests.get(API_URL, params=params)
        if response.ok:
            return json.loads(response.json())
        else:
            return None
    
    except Exception as e:
        raise e


def post_data(data):
    try:
        response = requests.post(API_URL, json=json.dumps(data))
        return response
        
    except Exception as e:
       raise e


def put_data(data):
    try:
        id = json.loads(data)['id']
        response = requests.put(f"{API_URL}/{id}", json=json.dumps(data))
        return response.text
    
    except Exception as e:
       raise e


def delete_data(id):
    try:
        id = json.loads(data)['id']
        response = requests.delete(f"{API_URL}/{id}")
        return response.text
    
    except Exception as e:
       raise e
