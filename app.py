import os
from flask import Flask, jsonify, render_template, render_template_string

app = Flask(__name__)

# ==========================================
# CEE v9.2 PRODUCTION DATA CORE
# ==========================================
engine_cache = {
    "framework_version": "9.2-Production-Matrix",
    "global_rules": {
        "block_volatile_micro_lines": True,
        "enforce_milestone_slider_floors": True,
        "block_puck_lines": True,
        "block_mlb_feed": True
    },
    "nhl_slate": {
        "status": "active",
        "games": [
            {"matchup": "Colorado @ Winnipeg", "ou": 6.5, "contrarian_edge": "SHARP_UNDER_SPLIT"},
            {"matchup": "Pittsburgh @ Washington", "ou": 6.0, "contrarian_edge": "LINE_FREEZE_EDGE"},
            {"matchup": "Edmonton @ Anaheim", "ou": 6.5, "contrarian_edge": "PUBLIC_OVER_BAIT"}
        ]
    },
    "nfl_player_props": {
        "status": "active_monitoring",
        "milestones": [
            {"player": "Jared Goff", "team": "DET", "matchup": "@ DAL", "metric": "Passing Yards", "house_line": 264.5, "safety_floor": 225.0, "edge_status": "SHARP_VOLUME_EDGE"},
            {"player": "Jahmyr Gibbs", "team": "DET", "matchup": "@ DAL", "metric": "Rushing Yards", "house_line": 62.5, "safety_floor": 55.0, "edge_status": "VOLUME_ADVANTAGE"}
        ]
    }
}

FALLBACK_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>CEE v9.2 Matrix</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #0f111a; color: #a6accd; font-family: monospace; padding: 20px; }
        h1 { color: #ff5370; border-bottom: 2px solid #ff5370; padding-bottom: 5px; }
        .green { color: #c3e88d; }
    </style>
</head>
<body>
    <h1>CONTRARIAN EDGE ENGINE v9.2</h1>
    <p>Status: <span class="green">CORE_MATRIX_INITIALIZED</span></p>
    <p>System online. Ready for interface linking.</p>
</body>
</html>
"""

@app.route("/")
def index():
    try:
        return render_template("dashboard.html", cache=engine_cache)
    except Exception:
        return render_template_string(FALLBACK_HTML, cache=engine_cache)

@app.route("/api/v9/engine/cache", methods=["GET"])
def get_engine_cache():
    return jsonify(engine_cache)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
