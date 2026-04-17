from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# এই অবজেক্টটি আপনার অ্যাডমিন প্যানেল থেকে কন্ট্রোল হবে
mix_store_db = {
    "store_config": {
        "app_name": "MiX Store",
        "section_title": "Featured Premium Apps",
        "sub_title": "Download the latest Mod and Security tools",
        "footer_text": "© 2026 MiX Store | Powered by Minhaz Security"
    },
    "maintenance": {
        "is_active": False,
        "message": "We are upgrading our servers for better speed!"
    },
    "apps": [] # এখান থেকে অ্যাপের সব ডেটা আসবে
}

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(mix_store_db)

@app.route('/api/admin/update', methods=['POST'])
def update_data():
    global mix_store_db
    auth = request.headers.get("Authorization")
    if auth != "MIX_ADMIN_786":
        return jsonify({"error": "Wrong Key"}), 401
    
    # অ্যাডমিন প্যানেল থেকে আসা পুরো নতুন ডেটা এখানে সেভ হবে
    mix_store_db = request.json
    return jsonify({"status": "success", "message": "MiX Store Updated!"})

if __name__ == '__main__':
    app.run()
