import os
import json
from flask import Flask, jsonify, render_template, render_template_string

app = Flask(__name__)

# ==========================================
# CEE v5.3 FIXED MATRIX DATA BACKUP
# ==========================================
DEFAULT_MATRIX = {
    "framework_version": "5.3-Clean-Table-Matrix",
    "low_volume_splits": {
        "status": "active",
        "games": [
            {"matchup": "Islanders @ Rangers", "target": "Under 5.5", "tickets": "58%", "cash": "64%", "state": "NHL TONIGHT"},
            {"matchup": "Predators @ Maple Leafs", "target": "Under 6.0", "tickets": "52%", "cash": "71%", "state": "NHL TONIGHT"},
            {"matchup": "Georgia @ Alabama", "target": "Georgia -3", "tickets": "74%", "cash": "51%", "state": "CFB WEEK 6"},
            {"matchup": "UCLA @ Oregon", "target": "Under 59.5", "tickets": "68%", "cash": "44%", "state": "CFB WEEK 6"},
            {"matchup": "Kings @ Warriors", "target": "Under 222.5", "tickets": "51%", "cash": "43%", "state": "NBA TONIGHT"}
        ]
    },
    "nfl_player_props": {
        "status": "active_monitoring",
        "milestones": [
            {"player": "De'Aaron Fox", "team": "SAC", "matchup": "@ GSW", "metric": "NBA Pre Points", "house_line": 21.5, "safety_floor": 17.0, "edge_status": "VOLUME_SAFETY_EDGE"},
            {"player": "Jared Goff", "team": "DET", "matchup": "@ DAL", "metric": "Passing Yards", "house_line": 264.5, "safety_floor": 225.0, "edge_status": "SHARP_VOLUME_EDGE"},
            {"player": "Jahmyr Gibbs", "team": "DET", "matchup": "@ DAL", "metric": "Rushing Yards", "house_line": 62.5, "safety_floor": 55.0, "edge_status": "VOLUME_ADVANTAGE"},
            {"player": "Nico Iamaleava", "team": "TENN", "matchup": "CFB Slate", "metric": "Passing Yards", "house_line": 238.5, "safety_floor": 195.0, "edge_status": "CONTRARIAN_VOLUME_EDGE"}
        ]
    },
    "nhl_slate": {
        "status": "active",
        "games": [
            {"matchup": "Islanders @ Rangers", "ou": 5.5, "contrarian_edge": "PUBLIC_FAVORITE_TRAP"},
            {"matchup": "Predators @ Maple Leafs", "ou": 6.0, "contrarian_edge": "SHARP_MONEY_SPLIT"},
            {"matchup": "Senators @ Red Wings", "ou": 6.5, "contrarian_edge": "CONTRARIAN_UNDER_EDGE"},
            {"matchup": "Panthers @ Kings", "ou": 6.0, "contrarian_edge": "LINE_FREEZE"}
        ]
    }
}

def load_live_feed_cache():
    """Reads live json cache if present, otherwise instantly falls back to defaults."""
    json_path = os.path.join(os.path.dirname(__file__), "sports_data.json")
    if os.path.exists(json_path):
        try:
            with open(json_path, "r") as f:
                data = json.load(f)
                # Only use the JSON if it actually has game rows inside it
                if "low_volume_splits" in data and len(data["low_volume_splits"]["games"]) > 0:
                    return data
        except Exception:
            pass
    return DEFAULT_MATRIX

@app.route("/")
def index():
    cache_data = load_live_feed_cache()
    try:
        return render_template("dashboard.html", cache=cache_data)
    except Exception:
        return "<html><body><h1>CEE Matrix Active - Re-linking Handles</h1></body></html>"

@app.route("/api/v5/engine/cache", methods=["GET"])
def get_engine_cache():
    return jsonify(load_live_feed_cache())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
