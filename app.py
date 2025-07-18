from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

@app.route('/plaid-pdf', methods=['POST'])
def get_plaid_pdf():
    data = request.get_json()
    token = data.get('asset_report_token')

    plaid_res = requests.post(
        'https://sandbox.plaid.com/asset_report/pdf/get',
        headers={'Content-Type': 'application/json'},
        json={
            'client_id': os.environ.get('686fe4ffcac8430024336bcf'),
            'secret': os.environ.get('6071675b66d4cec6653e37d5cb48b4'),
            'asset_report_token': token
        }
    )

    return Response(plaid_res.content, content_type='application/pdf')

@app.route('/')
def hello():
    return "Plaid PDF Proxy is running."
