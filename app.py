import os
from flask import Flask, jsonify, render_template, render_template_string

app = Flask(__name__)

# ==========================================
# CEE v5.3 CLEAN-TABLE-MATRIX CONFIG
# ==========================================
engine_cache = {
    "framework_version": "5.3-Clean-Table-Matrix",
    "last_sync_timestamp": "10-06-2026 10:10 AM",
    "global_rules": {
        "block_volatile_micro_lines": True,
        "enforce_milestone_slider_floors": True,
        "block_puck_lines": True,
        "block_mlb_feed": True
    },
    "metrics_config": {
        "game_script_panic_threshold": 0.72,
        "morale_deficit_penalty": 0.15
    },
    "nfl_player_props": {
        "status": "active_monitoring",
        "milestones": [
            {"player": "Jared Goff", "team": "DET", "matchup": "@ DAL", "metric": "Passing Yards", "house_line": 264.5, "safety_floor": 225.0, "edge_status": "SHARP_VOLUME_EDGE"},
            {"player": "Jahmyr Gibbs", "team": "DET", "matchup": "@ DAL", "metric": "Rushing Yards", "house_line": 62.5, "safety_floor": 55.0, "edge_status": "VOLUME_ADVANTAGE"},
            {"player": "Josh Allen", "team": "BUF", "matchup": "@ NYJ", "metric": "Passing Yards", "house_line": 242.5, "safety_floor": 215.0, "edge_status": "WEATHER_PROTECTED"},
            {"player": "Patrick Mahomes", "team": "KC", "matchup": "@ SF", "metric": "Passing Yards", "house_line": 254.5, "safety_floor": 220.0, "edge_status": "ALGORITHM_TRAP"}
        ]
    },
    "nhl_slate": {
        "status": "active",
        "games": [
            {"matchup": "Islanders @ Rangers", "ou": 5.5, "status": "waiting_puck_drop", "contrarian_edge": "PUBLIC_FAVORITE_TRAP"},
            {"matchup": "Predators @ Maple Leafs", "ou": 6.0, "status": "waiting_puck_drop", "contrarian_edge": "SHARP_MONEY_SPLIT"},
            {"matchup": "Senators @ Red Wings", "ou": 6.5, "status": "waiting_puck_drop", "contrarian_edge": "CONTRARIAN_UNDER_EDGE"},
            {"matchup": "Panthers @ Kings", "ou": 6.0, "status": "waiting_puck_drop", "contrarian_edge": "LINE_FREEZE"}
        ]
    },
    "low_volume_splits": {
        "status": "active",
        "games": [
            {"matchup": "Islanders @ Rangers", "target": "Under 5.5", "tickets": "78%", "cash": "64%", "state": "LOW"},
            {"matchup": "Predators @ Maple Leafs", "target": "Under 6.0", "tickets": "82%", "cash": "71%", "state": "OVERLOOKED"},
            {"matchup": "Senators @ Red Wings", "target": "Under 6.5", "tickets": "71%", "cash": "59%", "state": "LOW"}
        ]
    }
}

FALLBACK_HTML = "<html><body><h1>CEE Matrix Fallback Active</h1></body></html>"

@app.route("/")
def index():
    try:
        return render_template("dashboard.html", cache=engine_cache)
    except Exception:
        return render_template_string(FALLBACK_HTML, cache=engine_cache)

@app.route("/api/v5/engine/cache", methods=["GET"])
def get_engine_cache():
    return jsonify(engine_cache)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
