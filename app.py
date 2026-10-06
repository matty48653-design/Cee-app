import os
from flask import Flask, jsonify, render_template, render_template_string

app = Flask(__name__)

# ==========================================
# CEE v5.3 CLEAN-TABLE-MATRIX CONFIG
# ==========================================
engine_cache = {
    "framework_version": "5.3-Clean-Table-Matrix",
    "last_sync_timestamp": "10-06-2026 09:52 AM",
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
            {
                "player": "Jared Goff",
                "team": "DET",
                "matchup": "@ ARI",
                "metric": "Passing Yards",
                "house_line": 258.5,
                "safety_floor": 225.0,
                "edge_status": "EXPOSED_ALGORITHM_TRAP"
            },
            {
                "player": "Jahmyr Gibbs",
                "team": "DET",
                "matchup": "@ ARI",
                "metric": "Rushing Yards",
                "house_line": 64.5,
                "safety_floor": 55.0,
                "edge_status": "SHARP_VOLUME_ADVANTAGE"
            }
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
    "trap_analysis_models": {
        "active_cards": {
            "historical_trap_01": {
                "matchup": "Falcons @ Saints",
                "type": "Historical Baseline Trap",
                "rules_applied": "v5.3_compact_isolation",
                "public_bias": "Heavy Public Under Bait Volume"
            }
        }
    }
}

FALLBACK_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>CEE v5.3 Matrix</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #0f111a; color: #a6accd; font-family: monospace; padding: 20px; }
        .card { background: #1a1c2a; padding: 15px; border-radius: 6px; border: 1px solid #ff5370; margin-bottom: 15px; }
        h1 { color: #ff5370; border-bottom: 2px solid #ff5370; padding-bottom: 5px; }
        .green { color: #c3e88d; }
    </style>
</head>
<body>
    <h1>CONTRARIAN EDGE ENGINE v5.3</h1>
    <p>Status: <span class="green">LIVE_EMBEDDED_MATRIX</span></p>
    <div class="card">
        <h3>NFL TRAP CHANNELS</h3>
        <p><b>Matchup:</b> {{ cache.trap_analysis_models.active_cards.historical_trap_01.matchup }}</p>
    </div>
</body>
</html>
"""

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
