import os
import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# THE CORNERSTONE USER DATA MODEL MATRIX (WEEKLY POSITIONS HANDLERS)
USER_STRATEGY_MARKERS = {
    "New York Islanders @ New York Rangers": {
        "sport_tag": "🏒 ACTIVE HOCKEY SLATE", "line": "O/U 5.5", "total": "Sim Total: 6.0", "pacing": "Pacing 🔥 EVALUATING",
        "players": [{"name": "Artemi Panarin", "position": "LW", "target": "Over 2.5 Shots on Goal Floor", "is_floor": True}, {"name": "Bo Horvat", "position": "C", "target": "Under 3.5 Shots on Goal Ceiling", "is_floor": False}],
        "morale": [{"unit": "Islanders Blue Line", "status": "WARN", "alert_text": "AWS Depth Metric: High expected defensive zone pressure. Ranger SOG floor highly insulated."}]
    },
    "Ottawa Senators @ Detroit Red Wings": {
        "sport_tag": "🏒 ACTIVE HOCKEY SLATE", "line": "O/U 6.5", "total": "Sim Total: 5.5", "pacing": "Pacing 📉 UNDER",
        "players": [{"name": "Dylan Larkin", "position": "C", "target": "Over 3.5 Shots on Goal Floor", "is_floor": True}, {"name": "Tim Stützle", "position": "C", "target": "Under 2.5 Shots on Goal Ceiling", "is_floor": False}],
        "morale": [{"unit": "Sens Front 6 Pacing", "status": "WARN", "alert_text": "Morale Deficit Stream: Early season physical fatigue penalty flagged on transition defense."}]
    },
    "Florida Panthers @ Los Angeles Kings": {
        "sport_tag": "🏒 ACTIVE HOCKEY SLATE", "line": "O/U 6.0", "total": "Sim Total: 7.0", "pacing": "Pacing 💥 OVER",
        "players": [{"name": "Matthew Tkachuk", "position": "RW", "target": "Over 3.5 Shots on Goal Floor", "is_floor": True}, {"name": "Anze Kopitar", "position": "C", "target": "Under 2.5 Shots on Goal Ceiling", "is_floor": False}],
        "morale": [{"unit": "Kings Netminder Group", "status": "WARN", "alert_text": "Public Favorite Trap: High volume public backing exposure. High risk variance alert."}]
    },
    "Detroit Lions @ Arizona Cardinals": {
        "sport_tag": "🏈 CONTRARIAN FOOTBALL SLATE", "line": "O/U 52.5", "total": "CEE Projected: 57", "pacing": "Pacing 💥 OVER",
        "players": [{"name": "Jared Goff", "position": "QB", "target": "Over 248.5 Passing Yards Floor", "is_floor": True}, {"name": "Amon-Ra St. Brown", "position": "WR", "target": "Under 7.5 Receptions Ceiling", "is_floor": False}],
        "morale": [{"unit": "Cardinals Secondary", "status": "WARN", "alert_text": "Game-Script Panic Threshold: Public heavily backing favorite. Line fade premium active."}]
    }
}

def pull_unblocked_live_feeds():
    # Direct Public JSON channels from ESPN - fully unblocked on cloud hosts
    nhl_api = "https://espn.com"
    nfl_api = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    
    live_slates = []
    found_games = set()
    
    # Process both feed layers consecutively
    for url in [nhl_api, nfl_api]:
        try:
            res = requests.get(url, timeout=6).json()
            for event in res.get("events", []):
                game_name = event.get("name", "").replace(" at ", " @ ")
                
                # Check if this scraped game name matches our track portfolio keys
                if game_name in USER_STRATEGY_MARKERS:
                    found_games.add(game_name)
                    config = USER_STRATEGY_MARKERS[game_name]
                    
                    # Extract live game clock/period status details safely
                    detail = event.get("status", {}).get("type", {}).get("detail", "PRE-GAME")
                    
                    # Extract real-time scoreboard matrix numbers directly
                    scores = ["0", "0"]
                    competitors = event.get("competitions", [{}])[0].get("competitors", [])
                    if len(competitors) >= 2:
                        # ESPN JSON Array Positions: Index 0 is Home, Index 1 is Away
                        scores = [competitors[1].get("score", "0"), competitors[0].get("score", "0")]
                    score_str = f"{scores[0]} - {scores[1]}"
                    
                    live_slates.append({
                        "sport_tag": config["sport_tag"],
                        "game": game_name,
                        "live_clock": detail.upper(),
                        "score_string": score_str,
                        "closing_line": config["line"],
                        "sim_total": config["total"],
                        "pacing_status": config["pacing"],
                        "players": config["players"],
                        "morale": config["morale"]
                    })
        except Exception as e:
            print(f"Feed error handle: {e}")

    # Fallback injector loop to keep dashboard data visible if a game hasn't loaded in the API feed yet
    for game_name, config in USER_STRATEGY_MARKERS.items():
        if game_name not in found_games:
            live_slates.append({
                "sport_tag": config["sport_tag"],
                "game": game_name,
                "live_clock": "PRE-GAME",
                "score_string": "0 - 0" if "O/U 5.5" in config["line"] or "O/U 6.5" in config["line"] or "O/U 6.0" in config["line"] else "PRE-GAME",
                "closing_line": config["line"],
                "sim_total": config["total"],
                "pacing_status": config["pacing"],
                "players": config["players"],
                "morale": config["morale"]
            })
            
    return live_slates

@app.route('/')
def dashboard():
    return render_template("dashboard.html", slates=pull_unblocked_live_feeds())

@app.route('/api/state-json', methods=['GET'])
def state_json():
    return jsonify({"slates": pull_unblocked_live_feeds()})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
