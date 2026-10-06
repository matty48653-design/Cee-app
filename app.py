import os
import json
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

CACHE_FILE = "cee_state.json"

# Absolute baseline fallback data block
DEFAULT_STATE = {
    "slate": {
        "game": "Detroit Lions @ Green Bay Packers",
        "live_clock": "2ND QTR - 04:12",
        "score_string": "DET 24 - 10 GB",
        "closing_line": 49.5,
        "sim_total": 58,
        "pacing_status": "Pacing 💥 OVER"
    },
    "players": [
        {"name": "Jared Goff", "position": "QB", "target": "Over 242.5 Passing Yards Floor (165 YDS - ACTIVE)", "is_floor": True},
        {"name": "Amon-Ra St. Brown", "position": "WR", "target": "Under 6.5 Live Receptions Ceiling (2 REC - ACTIVE)", "is_floor": False}
    ],
    "morale": [
        {"unit": "Packers Secondary", "status": "WARN", "alert_text": "Morale Deficit Penalty engaged. Game-Script Panic Threshold breached."}
    ]
}

def load_cached_matrix():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except:
            return DEFAULT_STATE
    return DEFAULT_STATE

def save_cached_matrix(data):
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f)

@app.route('/')
def dashboard():
    state = load_cached_matrix()
    return render_template(
        "dashboard.html", 
        slate=state["slate"], 
        players=state["players"], 
        morale=state["morale"]
    )

@app.route('/api/update-feed', methods=['POST'])
def update_feed():
    incoming_data = request.get_json()
    if not incoming_data:
        return jsonify({"status": "failed", "message": "No JSON payload found"}), 400
        
    # Write directly to the hard disk file cache
    save_cached_matrix(incoming_data)
    return jsonify({"status": "success", "message": "Live CEE Matrix File Synchronized"}), 200

@app.route('/api/live-state', methods=['GET'])
def get_live_state():
    return jsonify(load_cached_matrix())

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
