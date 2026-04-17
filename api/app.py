from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Default Database Structure
mix_store_db = {
    "store_config": {
        "app_name": "MiX Store",
        "section_title": "MODDED & PREMIUM APPS",
        "sub_title": "Fast, Safe and Verified by Minhaz Security",
        "footer_text": "© 2026 MiX Store | All Rights Reserved"
    },
    "maintenance": {
        "is_active": False,
        "message": "Updating servers, please wait!"
    },
    "apps": [] 
}

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(mix_store_db)

@app.route('/api/admin/update', methods=['POST'])
def update_data():
    global mix_store_db
    auth = request.headers.get("Authorization")
    if auth != "MIX_ADMIN_786":
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    mix_store_db = data
    return jsonify({"status": "success", "message": "Updated!"})

# Vercel needs this to find the app
if __name__ == "__main__":
    app.run()