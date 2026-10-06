import os
import time
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# The 4 complete game state matrices from yesterday's high-profile slate
YESTERDAY_GAMES_BOARDS = [
    {
        "slate": {
            "game": "Detroit Lions @ Carolina Panthers",
            "live_clock": "1ST QTR - 08:45",
            "score_string": "DET 7 - 3 CAR",
            "closing_line": 46.5,
            "sim_total": 49,
            "pacing_status": "Pacing 🔥 STABLE"
        },
        "players": [
            {"name": "Jared Goff", "position": "QB", "target": "Over 238.5 Pass Yards Floor (45 YDS)", "is_floor": True},
            {"name": "Amon-Ra St. Brown", "position": "WR", "target": "Under 6.5 Receptions Ceiling (1 REC)", "is_floor": False}
        ],
        "morale": [
            {"unit": "Panthers Run Def", "status": "WARN", "alert_text": "CEE Floor Gauge: Public heavily backing DET. Track line adjustments."}
        ]
    },
    {
        "slate": {
            "game": "Detroit Lions @ Carolina Panthers",
            "live_clock": "4TH QTR - FINAL",
            "score_string": "DET 26 - 32 CAR",
            "closing_line": 46.5,
            "sim_total": 58,
            "pacing_status": "Pacing 💥 OVER"
        },
        "players": [
            {"name": "Jared Goff", "position": "QB", "target": "Over 238.5 Pass Yards Floor (244 YDS - CLEARED)", "is_floor": True},
            {"name": "Amon-Ra St. Brown", "position": "WR", "target": "Under 6.5 Receptions Ceiling (7 REC - BREACHED)", "is_floor": False}
        ],
        "morale": [
            {"unit": "Lions Secondary", "status": "WARN", "alert_text": "Game-Script Panic Threshold breached. High public backing collapsed late."}
        ]
    },
    {
        "slate": {
            "game": "Dallas Cowboys @ Houston Texans",
            "live_clock": "3RD QTR - 02:15",
            "score_string": "DAL 24 - 20 HOU",
            "closing_line": 51.5,
            "sim_total": 56,
            "pacing_status": "Pacing 🔥 OVER"
        },
        "players": [
            {"name": "Dak Prescott", "position": "QB", "target": "Over 265.5 Pass Yards Floor (198 YDS)", "is_floor": True},
            {"name": "CeeDee Lamb", "position": "WR", "target": "Under 7.5 Receptions Ceiling (5 REC)", "is_floor": False}
        ],
        "morale": [
            {"unit": "Texans O-Line", "status": "WARN", "alert_text": "AWS Pressure Metric: High pocket collapse trajectory active."}
        ]
    },
    {
        "slate": {
            "game": "Dallas Cowboys @ Houston Texans",
            "live_clock": "4TH QTR - FINAL",
            "score_string": "DAL 34 - 30 HOU",
            "closing_line": 51.5,
            "sim_total": 64,
            "pacing_status": "Pacing 💥 OVER"
        },
        "players": [
            {"name": "Dak Prescott", "position": "QB", "target": "Over 265.5 Pass Yards Floor (282 YDS - CLEARED)", "is_floor": True},
            {"name": "CeeDee Lamb", "position": "WR", "target": "Under 7.5 Receptions Ceiling (6 REC - SAFE)", "is_floor": False}
        ],
        "morale": [
            {"unit": "Texans Secondary", "status": "WARN", "alert_text": "Increment Gain Strategy: Money line shifted late to public trap exit."}
        ]
    },
    {
        "slate": {
            "game": "Kansas City Chiefs @ Las Vegas Raiders",
            "live_clock": "4TH QTR - FINAL",
            "score_string": "KC 30 - 27 LV",
            "closing_line": 44.5,
            "sim_total": 57,
            "pacing_status": "Pacing 💥 OVER"
        },
        "players": [
            {"name": "Patrick Mahomes", "position": "QB", "target": "Over 235.5 Pass Yards Floor (242 YDS - CLEARED)", "is_floor": True},
            {"name": "Travis Kelce", "position": "TE", "target": "Under 5.5 Receptions Ceiling (4 REC - SAFE)", "is_floor": False}
        ],
        "morale": [
            {"unit": "Raiders Front 7", "status": "WARN", "alert_text": "Morale DeficitStream: Final drive fatigue penalty logged."}
        ]
    },
    {
        "slate": {
            "game": "Los Angeles Rams @ Philadelphia Eagles",
            "live_clock": "4TH QTR - FINAL",
            "score_string": "LAR 24 - 20 PHI",
            "closing_line": 48.5,
            "sim_total": 44,
            "pacing_status": "Pacing 📉 UNDER"
        },
        "players": [
            {"name": "Matthew Stafford", "position": "QB", "target": "Over 224.5 Pass Yards Floor (231 YDS - CLEARED)", "is_floor": True},
            {"name": "Kyren Williams", "position": "RB", "target": "Under 88.5 Rush Yards Ceiling (72 YDS - SAFE)", "is_floor": False}
        ],
        "morale": [
            {"unit": "Eagles Secondary", "status": "WARN", "alert_text": "Public Trap Faded: 82% public money line on favored home team fails."}
        ]
    }
]

@app.route('/')
def dashboard():
    # Calculate which board index to show based on system time (changes every 4 seconds)
    current_time_seconds = int(time.time())
    calculated_index = (current_time_seconds // 4) % len(YESTERDAY_GAMES_BOARDS)
    
    current_active_board = YESTERDAY_GAMES_BOARDS[calculated_index]
    
    return render_template(
        "dashboard.html", 
        slate=current_active_board["slate"], 
        players=current_active_board["players"], 
        morale=current_active_board["morale"]
    )

# Clean, unified updates endpoint
@app.route('/api/live-state', methods=['GET'])
def get_live_state():
    current_time_seconds = int(time.time())
    calculated_index = (current_time_seconds // 4) % len(YESTERDAY_GAMES_BOARDS)
    return jsonify(YESTERDAY_GAMES_BOARDS[calculated_index])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
