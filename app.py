import math
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def dashboard():
    # 1. Active Slate Processing
    live_slate = {
        "game": "Atlanta Falcons @ New Orleans Saints",
        "live_clock": "38.0 MINS",
        "score_string": "ATL 14 - 24 NO",
        "closing_line": 47.5,
        "sim_total": 60,
        "pacing_status": "Pacing 💥 OVER"
    }
    
    # 2. Player Data Stream Target Matrix
    player_data_stream = [
        {
            "name": "Alvin Kamara",
            "position": "RB",
            "target": "Over 4.5 Live Receptions Floor",
            "is_floor": True
        },
        {
            "name": "Chris Olave",
            "position": "WR",
            "target": "Under 6.5 Live Receptions Ceiling",
            "is_floor": False
        }
    ]
    
    # 3. Morale Deficit Stream AWS Trajectory Engagements
    morale_deficit_stream = [
        {
            "unit": "Saints O-Line",
            "status": "WARN",
            "alert_text": "AWS Next Gen: High pocket pressure collapse trajectory active."
        }
    ]
    
    return render_template(
        "dashboard.html", 
        slate=live_slate, 
        players=player_data_stream, 
        morale=morale_deficit_stream
    )

if __name__ == '__main__':
    app.run(debug=True)
