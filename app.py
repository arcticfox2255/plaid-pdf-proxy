from flask import Flask, request, Response, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/plaid-pdf', methods=['POST'])
def get_pdf():
    try:
        data = request.get_json()
        token = data.get("asset_report_token")
        if not token:
            return jsonify({"error": "Missing asset_report_token"}), 400

        plaid_res = requests.post(
            "https://sandbox.plaid.com/asset_report/pdf/get",
            headers={"Content-Type": "application/json"},
            json={
                "client_id": os.environ["PLAID_CLIENT_ID"],
                "secret": os.environ["PLAID_SECRET"],
                "asset_report_token": token
            }
        )

        if plaid_res.status_code != 200:
            return jsonify({"error": "Plaid returned error", "status": plaid_res.status_code}), plaid_res.status_code

        return Response(plaid_res.content, content_type="application/pdf")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Plaid PDF Proxy is up"
