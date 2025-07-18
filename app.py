from flask import Flask, request, Response, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Plaid PDF Proxy is running'

@app.route('/plaid-pdf', methods=['GET'])
def get_pdf():
    token = request.args.get("asset_report_token")
    if not token:
        return jsonify({"error": "Missing asset_report_token"}), 400

    # Request the real PDF from Plaid
    plaid_response = requests.post(
        "https://sandbox.plaid.com/asset_report/pdf/get",
        headers={"Content-Type": "application/json"},
        json={
            "client_id": os.environ["PLAID_CLIENT_ID"],
            "secret": os.environ["PLAID_SECRET"],
            "asset_report_token": token
        }
    )

    # Ensure successful response
    if plaid_response.status_code != 200:
        return jsonify({"error": "Plaid PDF request failed", "details": plaid_response.text}), plaid_response.status_code

    # Stream raw binary PDF back
    return Response(
        plaid_response.content,
        status=200,
        content_type="application/pdf",
        headers={
            "Content-Disposition": "inline; filename=plaid_asset_report.pdf"
        }
    )
