import math
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Global variable to store incoming live game feed state
CURRENT_GAME_STATE = {}

@app.route('/')
def dashboard():
    # Fallback to test simulation data if live webhook hasn't sent data yet
    slate = CURRENT_GAME_STATE.get("slate", {
        "game": "Atlanta Falcons @ New Orleans Saints",
        "live_clock": "38.0 MINS",
        "score_string": "ATL 14 - 24 NO",
        "closing_line": 47.5,
        "sim_total": 60,
        "pacing_status": "Pacing 💥 OVER"
    })
    
    players = CURRENT_GAME_STATE.get("players", [
        {"name": "Alvin Kamara", "position": "RB", "target": "Over 4.5 Live Receptions Floor", "is_floor": True},
        {"name": "Chris Olave", "position": "WR", "target": "Under 6.5 Live Receptions Ceiling", "is_floor": False}
    ])
    
    morale = CURRENT_GAME_STATE.get("morale", [
        {"unit": "Saints O-Line", "status": "WARN", "alert_text": "AWS Next Gen: High pocket pressure collapse trajectory active."}
    ])
    
    return render_template("dashboard.html", slate=slate, players=players, morale=morale)

# NEW WEBHOOK ENDPOINT: This receives the actual live feed data arrays
@app.route('/api/update-feed', methods=['POST'])
def update_feed():
    global CURRENT_GAME_STATE
    incoming_data = request.get_json()
    
    if incoming_data:
        CURRENT_GAME_STATE = incoming_data
        return jsonify({"status": "success", "message": "Live CEE Matrix Updated"}), 200
    return jsonify({"status": "failed", "message": "No data received"}), 400

if __name__ == '__main__':
    app.run(debug=True)
