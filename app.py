import os
from flask import Flask, render_template

app = Flask(__name__)

# Reverting directly back to your working v5.3 core matrix data blocks
WEEK_5_CEE_MATRIX = [
    {
        "game": "Tampa Bay Buccaneers @ Dallas Cowboys",
        "live_clock": "THU - 8:15 PM ET",
        "score_string": "PRE-GAME",
        "closing_line": 47.5,
        "sim_total": 49,
        "pacing_status": "Pacing 🔥 STABLE",
        "players": [
            {"name": "Dak Prescott", "position": "QB", "target": "Over 258.5 Passing Yards Floor", "is_floor": True},
            {"name": "CeeDee Lamb", "position": "WR", "target": "Under 7.5 Receptions Ceiling", "is_floor": False}
        ],
        "morale": [
            {"unit": "Buccaneers Front 7", "status": "WARN", "alert_text": "AWS Pass-Rush Score: Deficit tracked. Dak passing yard floor highly insulated."}
        ]
    },
    {
        "game": "Chicago Bears @ Green Bay Packers",
        "live_clock": "SUN - 1:00 PM ET",
        "score_string": "PRE-GAME",
        "closing_line": 44.5,
        "sim_total": 41,
        "pacing_status": "Pacing 📉 UNDER",
        "players": [
            {"name": "D'Andre Swift", "position": "RB", "target": "Over 62.5 Rushing Yards Floor", "is_floor": True},
            {"name": "DJ Moore", "position": "WR", "target": "Under 5.5 Receptions Ceiling", "is_floor": False}
        ],
        "morale": [
            {"unit": "Packers Run Def", "status": "WARN", "alert_text": "Morale Deficit Flag engaged. Explosive public favorite trap bias active."}
        ]
    },
    {
        "game": "Minnesota Vikings @ New Orleans Saints",
        "live_clock": "SUN - 1:00 PM ET",
        "score_string": "PRE-GAME",
        "closing_line": 41.5,
        "sim_total": 46,
        "pacing_status": "Pacing 🔥 OVER",
        "players": [
            {"name": "Alvin Kamara", "position": "RB", "target": "Over 4.5 Live Receptions Floor", "is_floor": True},
            {"name": "Chris Olave", "position": "WR", "target": "Under 6.5 Live Receptions Ceiling", "is_floor": False}
        ],
        "morale": [
            {"unit": "Saints O-Line", "status": "WARN", "alert_text": "Game-Script Panic Threshold: High pocket pressure collapse trajectory expected."}
        ]
    },
    {
        "game": "Detroit Lions @ Arizona Cardinals",
        "live_clock": "SUN - 4:25 PM ET",
        "score_string": "PRE-GAME",
        "closing_line": 52.5,
        "sim_total": 57,
        "pacing_status": "Pacing 💥 OVER",
        "players": [
            {"name": "Jared Goff", "position": "QB", "target": "Over 248.5 Passing Yards Floor", "is_floor": True},
            {"name": "Amon-Ra St. Brown", "position": "WR", "target": "Under 7.5 Receptions Ceiling", "is_floor": False}
        ],
        "morale": [
            {"unit": "Cardinals Secondary", "status": "WARN", "alert_text": "Contrarian Edge Engine: Heavy public money fade opportunity. Volume is high."}
        ]
    }
]

@app.route('/')
def dashboard():
    return render_template("dashboard.html", slates=WEEK_5_CEE_MATRIX)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
