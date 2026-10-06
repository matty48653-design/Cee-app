import os
from flask import Flask, render_template

app = Flask(__name__)

# THE UNIFIED MULTI-SPORT STRATEGY ENGINE POOL (ALL CURRENT WEEK MATRICES)
COMPLETE_DASHBOARD_SLATES = [
    # 🏒 TONIGHT'S NHL MARQUEE TRACKING SLATES (OCTOBER 6)
    {
        "sport_tag": "🏒 ACTIVE HOCKEY SLATE",
        "game": "New York Islanders @ New York Rangers",
        "live_clock": "TONIGHT - 7:30 PM ET",
        "score_string": "PRE-GAME",
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
        "score_string": "PRE-GAME",
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
        "score_string": "PRE-GAME",
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
    # 🏈 WEEK 5 NFL STRATEGY PORTFOLIO BOARDS (OCTOBER 8 - 12)
    {
        "sport_tag": "🏈 CONTRARIAN FOOTBALL SLATE",
        "game": "Tampa Bay Buccaneers @ Dallas Cowboys",
        "live_clock": "THU - 8:15 PM ET",
        "score_string": "PRE-GAME",
        "closing_line": "O/U 47.5",
        "sim_total": "CEE Projected: 49",
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
        "sport_tag": "🏈 CONTRARIAN FOOTBALL SLATE",
        "game": "Chicago Bears @ Green Bay Packers",
        "live_clock": "SUN - 1:00 PM ET",
        "score_string": "PRE-GAME",
        "closing_line": "O/U 44.5",
        "sim_total": "CEE Projected: 41",
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
        "sport_tag": "🏈 CONTRARIAN FOOTBALL SLATE",
        "game": "Minnesota Vikings @ New Orleans Saints",
        "live_clock": "SUN - 1:00 PM ET",
        "score_string": "PRE-GAME",
        "closing_line": "O/U 41.5",
        "sim_total": "CEE Projected: 46",
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
            {"unit": "Cardinals Secondary", "status": "WARN", "alert_text": "Contrarian Edge Engine: Heavy public money fade opportunity. Volume is high."}
        ]
    }
]

@app.route('/')
def dashboard():
    return render_template("dashboard.html", slates=COMPLETE_DASHBOARD_SLATES)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
