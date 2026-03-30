import os
import json
import requests

API_URL = 'https://xxxx/api'


def get_data():
    try:
        response = requests.get(API_URL)
        if response.ok:
            return response.json()
        else:
            return None
    
    except Exception as e:
        raise e


def post_data(data):
    try:
        response = requests.post(API_URL, json=data)
        return response
        
    except Exception as e:
       raise e


def put_data(data):
    try:
        id = json.loads(data)['id']
        response = requests.put(f"{API_URL}/{id}", json=data)
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