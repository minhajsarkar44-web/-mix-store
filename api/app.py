import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client

app = Flask(__name__)
CORS(app)

# এখানে আমরা ভেরিয়েবল ব্যবহার করছি, সরাসরি কী (key) দিচ্ছি না
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        response = supabase.table("store_data").select("content").eq("id", 1).execute()
        if response.data:
            return jsonify(response.data[0]['content'])
        return jsonify({"error": "No data found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/update', methods=['POST'])
def update_data():
    auth = request.headers.get("Authorization")
    if auth != "MIX_ADMIN_786":
        return jsonify({"error": "Unauthorized"}), 401
    new_content = request.json
    try:
        response = supabase.table("store_data").upsert({"id": 1, "content": new_content}).execute()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
