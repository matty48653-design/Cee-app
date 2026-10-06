import os
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Single state engine variable pool
CURRENT_GAME_STATE = {
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

@app.route('/')
def dashboard():
    # Renders the current state directly so updates show on screen
    return render_template(
        "dashboard.html", 
        slate=CURRENT_GAME_STATE["slate"], 
        players=CURRENT_GAME_STATE["players"], 
        morale=CURRENT_GAME_STATE["morale"]
    )

@app.route('/api/update-feed', methods=['POST'])
def update_feed():
    global CURRENT_GAME_STATE
    incoming_data = request.get_json()
    
    if not incoming_data:
        return jsonify({"status": "failed", "message": "No JSON payload found"}), 400
        
    CURRENT_GAME_STATE = incoming_data
    return jsonify({"status": "success", "message": "Live CEE Matrix Updated"}), 200

# NEW JSON ENDPOINT FOR ACCURATE BACKGROUND POLLS
@app.route('/api/live-state', methods=['GET'])
def get_live_state():
    return jsonify(CURRENT_GAME_STATE)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
