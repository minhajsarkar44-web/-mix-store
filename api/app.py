import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client

app = Flask(__name__)
CORS(app)

# --- Supabase Config (Vercel Settings থেকে আসবে) ---
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# সুপাবেস কানেকশন চেক
if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        response = supabase.table("store_data").select("content").eq("id", 1).execute()
        if response.data:
            return jsonify(response.data[0]['content'])
        return jsonify({"error": "Database is empty"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# OTP Send
@app.route('/api/proxy/send', methods=['GET'])
def send_otp():
    email = request.args.get('email')
    if not email: return "Email required", 400
    try:
        url = f"https://otp-script.vercel.app/api/send?email={email}&key=0011"
        res = requests.get(url, headers=HEADERS, timeout=10)
        return (res.text, res.status_code)
    except:
        return "Server Timeout", 504

# OTP Verify
@app.route('/api/proxy/verify', methods=['GET'])
def verify_otp():
    email = request.args.get('email')
    otp = request.args.get('otp')
    try:
        url = f"https://otp-script.vercel.app/api/verify?email={email}&key=0001&otp={otp}"
        res = requests.get(url, headers=HEADERS, timeout=10)
        return (res.text, res.status_code)
    except:
        return "Verification Failed", 504

if __name__ == "__main__":
    app.run()
