import os
from flask import Flask, jsonify, render_template, render_template_string

app = Flask(__name__)

# ==========================================
# CEE v5.3 CLEAN-TABLE-MATRIX CONFIG
# ==========================================
engine_cache = {
    "framework_version": "5.3-Clean-Table-Matrix",
    "last_sync_timestamp": "10-06-2026 10:30 AM",
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
            {"player": "LeBron James", "team": "LAL", "matchup": "@ GSW", "metric": "NBA Pre Min Floor", "house_line": 18.5, "safety_floor": 14.0, "edge_status": "REST_RESTRICTION_FLOOR"},
            {"player": "Jared Goff", "team": "DET", "matchup": "@ DAL", "metric": "Passing Yards", "house_line": 264.5, "safety_floor": 225.0, "edge_status": "SHARP_VOLUME_EDGE"},
            {"player": "Jahmyr Gibbs", "team": "DET", "matchup": "@ DAL", "metric": "Rushing Yards", "house_line": 62.5, "safety_floor": 55.0, "edge_status": "VOLUME_ADVANTAGE"},
            {"player": "Jaxson Dart", "team": "OLE", "matchup": "CFB Slate", "metric": "Passing Yards", "house_line": 284.5, "safety_floor": 250.0, "edge_status": "CONTRARIAN_BLOWOUT"}
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
            {"matchup": "NMSU @ FIU (CFB)", "target": "FIU Spread -5.5", "tickets": "34%", "cash": "76%", "state": "SHARP_LINE_PUSH"},
            {"matchup": "Islanders @ Rangers", "target": "Under 5.5", "tickets": "58%", "cash": "64%", "state": "CONTRARIAN_EDGE"},
            {"matchup": "Predators @ Maple Leafs", "target": "Under 6.0", "tickets": "52%", "cash": "71%", "state": "OVERLOOKED"}
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
