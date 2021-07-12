
""" Handle api calls """
from os import environ
import traceback
import logging
import urllib.parse
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
import requests as rq
from requests.auth import HTTPBasicAuth

app = Flask(__name__)
CORS(app)

try:
    load_dotenv(find_dotenv())
except Exception as exception:
    pass


API_URL = environ.get('API_URL', 'http://localhost:3000') 
API_AUTH_PATH = environ.get('API_AUTH_PATH', '/path/to/auth')
MAX_TIMEOUT= environ.get("TIMEOUT", 2000)

def preAuth(credentials):
    resp = rq.post(
    API_URL + '/kernel/security/Token',
    json={'dsCredentials': credentials})
    token = resp.json()
    return token['nmToken']

@app.route('/proxy/<path:path>', methods=['GET', 'POST'])
def parse_api_get(path):
    """
    Parse every get method from the API
    """

    try:
        url = urllib.parse.urljoin(API_URL, path)
        credentials = request.headers.get('Authorization')
        token = preAuth(credentials)
        data = request.data
        verb = request.method
        cookies = { 'crmAuthToken': token }
        headers = {
            'Content-Type': 'application/json'
        }
        response = rq.request(
            verb,
            headers=headers,
            url=url,
            data=data,
            cookies=cookies,
            timeout=MAX_TIMEOUT)
        return jsonify(response.json()), response.status_code
    except rq.exceptions.Timeout:
        print("Timeout Error")
        abort(500, "Timeout on try request proxy")
    except rq.exceptions.RequestException as e:
        print("Error: {}".format(e))
        abort(500, "Error on try request proxy")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
