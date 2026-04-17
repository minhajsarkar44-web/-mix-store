import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client

app = Flask(__name__)
CORS(app)

# Supabase Credentials (Vercel Settings থেকে আসবে)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# সুপাবেস ক্লায়েন্ট সেটআপ
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# এপিআই ব্লক এড়াতে প্রিমিয়াম ইউজার এজেন্ট
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
}

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        response = supabase.table("store_data").select("content").eq("id", 1).execute()
        if response.data:
            return jsonify(response.data[0]['content'])
        return jsonify({"error": "No database data found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/proxy/send', methods=['GET'])
def send_otp():
    email = request.args.get('email')
    url = f"https://otp-script.vercel.app/api/send?email={email}&key=0011"
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        return (res.text, res.status_code)
    except:
        return "API Timeout", 504

@app.route('/api/proxy/verify', methods=['GET'])
def verify_otp():
    email = request.args.get('email')
    otp = request.args.get('otp')
    url = f"https://otp-script.vercel.app/api/verify?email={email}&key=0001&otp={otp}"
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        return (res.text, res.status_code)
    except:
        return "Verification Failed", 504

if __name__ == "__main__":
    app.run()
