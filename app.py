from flask import Flask, request, Response, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    return 'Plaid PDF Proxy is running'

@app.route('/plaid-pdf', methods=['GET'])
def get_pdf():
    token = request.args.get("asset_report_token")
    if not token:
        return jsonify({"error": "Missing asset_report_token"}), 400

    response = requests.post(
        "https://sandbox.plaid.com/asset_report/pdf/get",
        headers={"Content-Type": "application/json"},
        json={
            "client_id": os.environ["PLAID_CLIENT_ID"],
            "secret": os.environ["PLAID_SECRET"],
            "asset_report_token": token
        }
    )

    return Response(response.content, content_type="application/pdf")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
