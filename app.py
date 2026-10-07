import os
import json
from flask import Flask, jsonify, render_template, render_template_string

app = Flask(__name__)

# Core emergency matrix in case json is loading
DEFAULT_MATRIX = {
    "framework_version": "5.3-Clean-Table-Matrix",
    "global_rules": {
        "block_volatile_micro_lines": True,
        "enforce_milestone_slider_floors": True,
        "block_puck_lines": True,
        "block_mlb_feed": True
    },
    "low_volume_splits": {
        "status": "active",
        "games": [
            {"matchup": "Islanders @ Rangers", "target": "Under 5.5", "tickets": "58%", "cash": "64%", "state": "NHL TONIGHT"},
            {"matchup": "Predators @ Maple Leafs", "target": "Under 6.0", "tickets": "52%", "cash": "71%", "state": "NHL TONIGHT"},
            {"matchup": "Kings @ Warriors", "target": "Under 222.5", "tickets": "51%", "cash": "43%", "state": "NBA TONIGHT"}
        ]
    },
    "nfl_player_props": {
        "status": "active_monitoring",
        "milestones": [
            {"player": "Jared Goff", "team": "DET", "matchup": "@ DAL", "metric": "Passing Yards", "house_line": 264.5, "safety_floor": 225.0, "edge_status": "SHARP_VOLUME_EDGE"},
            {"player": "Jahmyr Gibbs", "team": "DET", "matchup": "@ DAL", "metric": "Rushing Yards", "house_line": 62.5, "safety_floor": 55.0, "edge_status": "VOLUME_ADVANTAGE"}
        ]
    },
    "nhl_slate": {
        "status": "active",
        "games": [
            {"matchup": "Islanders @ Rangers", "ou": 5.5, "contrarian_edge": "PUBLIC_FAVORITE_TRAP"},
            {"matchup": "Predators @ Maple Leafs", "ou": 6.0, "contrarian_edge": "SHARP_MONEY_SPLIT"},
            {"matchup": "Senators @ Red Wings", "ou": 6.5, "contrarian_edge": "CONTRARIAN_UNDER_EDGE"}
        ]
    }
}

def load_live_feed_cache():
    """Reads live metadata straight from your background bridge data file."""
    json_path = os.path.join(os.path.dirname(__file__), "sports_data.json")
    if os.path.exists(json_path):
        try:
            with open(json_path, "r") as f:
                data = json.load(f)
                if "low_volume_splits" in data:
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
        return "<html><body><h1>CEE Matrix Active - Connecting Live Handles</h1></body></html>"

@app.route("/api/v5/engine/cache", methods=["GET"])
def get_engine_cache():
    return jsonify(load_live_feed_cache())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
