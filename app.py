import os
import json
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

CACHE_FILE = "cee_live_cache.json"

# Safe initialization baseline matching your actual DraftKings slip
INITIAL_SLATES = [
    {
        "sport_tag": "🏒 ACTIVE HOCKEY SLATE",
        "game": "New York Islanders @ New York Rangers",
        "live_clock": "TONIGHT - 7:30 PM ET",
        "score_string": "0 - 0",
        "closing_line": "O/U 5.5",
        "sim_total": "Sim Total: 6.0",
        "pacing_status": "Pacing 🔥 EVALUATING",
        "players": [
            {"name": "Artemi Panarin", "position": "LW", "target": "Over 2.5 Shots on Goal Floor", "is_floor": True},
            {"name": "Bo Horvat", "position": "C", "target": "Under 3.5 Shots on Goal Ceiling", "is_floor": False}
        ],
        "morale": [
            {"unit": "Islanders Blue Line", "status": "WARN", "alert_text": "AWS Depth Metric: High expected defensive zone pressure. Ranger SOG floor highly insulated."}
        ]
    },
    {
        "sport_tag": "🏒 ACTIVE HOCKEY SLATE",
        "game": "Ottawa Senators @ Detroit Red Wings",
        "live_clock": "TONIGHT - 7:00 PM ET",
        "score_string": "0 - 0",
        "closing_line": "O/U 6.5",
        "sim_total": "Sim Total: 5.5",
        "pacing_status": "Pacing 📉 UNDER",
        "players": [
            {"name": "Dylan Larkin", "position": "C", "target": "Over 3.5 Shots on Goal Floor", "is_floor": True},
            {"name": "Tim Stützle", "position": "C", "target": "Under 2.5 Shots on Goal Ceiling", "is_floor": False}
        ],
        "morale": [
            {"unit": "Sens Front 6 Pacing", "status": "WARN", "alert_text": "Morale Deficit Stream: Early season physical fatigue penalty flagged on transition defense."}
        ]
    },
    {
        "sport_tag": "🏒 ACTIVE HOCKEY SLATE",
        "game": "Florida Panthers @ Los Angeles Kings",
        "live_clock": "TONIGHT - 10:00 PM ET",
        "score_string": "0 - 0",
        "closing_line": "O/U 6.0",
        "sim_total": "Sim Total: 7.0",
        "pacing_status": "Pacing 💥 OVER",
        "players": [
            {"name": "Matthew Tkachuk", "position": "RW", "target": "Over 3.5 Shots on Goal Floor", "is_floor": True},
            {"name": "Anze Kopitar", "position": "C", "target": "Under 2.5 Shots on Goal Ceiling", "is_floor": False}
        ],
        "morale": [
            {"unit": "Kings Netminder Group", "status": "WARN", "alert_text": "Public Favorite Trap: High volume public backing exposure. High risk variance alert."}
        ]
    },
    {
        "sport_tag": "🏈 CONTRARIAN FOOTBALL SLATE",
        "game": "Detroit Lions @ Arizona Cardinals",
        "live_clock": "SUN - 4:25 PM ET",
        "score_string": "PRE-GAME",
        "closing_line": "O/U 52.5",
        "sim_total": "CEE Projected: 57",
        "pacing_status": "Pacing 💥 OVER",
        "players": [
            {"name": "Jared Goff", "position": "QB", "target": "Over 248.5 Passing Yards Floor", "is_floor": True},
            {"name": "Amon-Ra St. Brown", "position": "WR", "target": "Under 7.5 Receptions Ceiling", "is_floor": False}
        ],
        "morale": [
            {"unit": "Cardinals Secondary", "status": "WARN", "alert_text": "Game-Script Panic Threshold: Public heavily backing favorite. Line fade premium active."}
        ]
    }
]

def load_live_matrix():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except:
            return INITIAL_SLATES
    return INITIAL_SLATES

@app.route('/')
def dashboard():
    return render_template("dashboard.html", slates=load_live_matrix())

# 🟢 THE INBOUND DATA GATE: Receives unblocked updates from your home computer
@app.route('/api/gate', methods=['POST'])
def data_gate_receiver():
    incoming_payload = request.get_json()
    if not incoming_payload or "slates" not in incoming_payload:
        return jsonify({"status": "error", "message": "Invalid format"}), 400
        
    with open(CACHE_FILE, "w") as f:
        json.dump(incoming_payload["slates"], f)
        
    return jsonify({"status": "success", "message": "Render live cache updated via gate channel"}), 200

# Endpoint that your browser queries smoothly in the background
@app.route('/api/state-json', methods=['GET'])
def state_json():
    return jsonify({"slates": load_live_matrix()})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
