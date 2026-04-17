import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client

app = Flask(__name__)
CORS(app)

# Supabase Setup (Environment Variables থেকে নেবে)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ওটিপি এপিআই কল করার সময় ব্লক এড়াতে এই হেডার ব্যবহার হবে
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        response = supabase.table("store_data").select("content").eq("id", 1).execute()
        return jsonify(response.data[0]['content']) if response.data else jsonify({"error": "No data"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# OTP Send Proxy
@app.route('/api/proxy/send', methods=['GET'])
def send_otp():
    email = request.args.get('email')
    url = f"https://otp-script.vercel.app/api/send?email={email}&key=0011"
    res = requests.get(url, headers=HEADERS)
    return (res.text, res.status_code)

# OTP Verify Proxy
@app.route('/api/proxy/verify', methods=['GET'])
def verify_otp():
    email = request.args.get('email')
    otp = request.args.get('otp')
    url = f"https://otp-script.vercel.app/api/verify?email={email}&key=0001&otp={otp}"
    res = requests.get(url, headers=HEADERS)
    return (res.text, res.status_code)

@app.route('/api/admin/update', methods=['POST'])
def update_data():
    if request.headers.get("Authorization") != "MIX_ADMIN_786":
        return jsonify({"error": "Unauthorized"}), 401
    new_content = request.json
    supabase.table("store_data").upsert({"id": 1, "content": new_content}).execute()
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run()
