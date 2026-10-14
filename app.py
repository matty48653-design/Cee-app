from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = "sports_data.json"

def load_matrix_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

@app.route('/')
def home():
    games_data = load_matrix_data()
    return render_template("dashboard.html", games=games_data)

@app.route('/update', methods=['POST'])
def update_matrix():
    try:
        incoming_payload = request.get_json()
        if not incoming_payload:
            return jsonify({"status": "error", "message": "Missing matrix payload"}), 400
            
        with open(DATA_FILE, "w") as f:
            json.dump(incoming_payload, f, indent=4)
            
        return jsonify({"status": "success", "message": "Matrix values synced successfully!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
