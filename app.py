import os
import httpx
import asyncio
import threading
from datetime import datetime
from flask import Flask, jsonify, render_template, render_template_string

app = Flask(__name__)

# ==========================================
# CEE v5.3 CLEAN-TABLE-MATRIX CONFIG
# ==========================================
engine_cache = {
    "framework_version": "5.3-Clean-Table-Matrix",
    "last_sync_timestamp": "10-06-2026 09:25 AM",
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
    "nhl_slate": {
        "status": "locked",
        "games": [
            {"matchup": "Red Wings @ Panthers", "ou": 6.5, "status": "waiting_puck_drop", "contrarian_edge": "SHARP_MONEY_SPLIT"},
            {"matchup": "Panthers @ Kings", "ou": 6.0, "status": "waiting_puck_drop", "contrarian_edge": "LINE_FREEZE"}
        ],
        "external_updates": []
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
    },
    "external_sync": {
        "status": "initialized",
        "last_updated": None,
        "sync_errors": 0
    }
}

cache_lock = threading.Lock()

# Safe backup interface if templates/dashboard.html is missing
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
        <p><b>Bias:</b> {{ cache.trap_analysis_models.active_cards.historical_trap_01.public_bias }}</p>
    </div>
    <div class="card">
        <h3>NHL TONIGHT</h3>
        {% for game in cache.nhl_slate.games %}
            <p>• {{ game.matchup }} (O/U: {{ game.ou }}) - <span class="green">{{ game.contrarian_edge }}</span></p>
        {% endfor %}
    </div>
</body>
</html>
"""

async def fetch_external_feed():
    FEED_URL = os.getenv("CONTRARIAN_DATA_FEED_URL", "https://external-odds-sync.local")
    headers = {"Authorization": f"Bearer {os.getenv('FEED_AUTH_TOKEN', 'default_secure_token')}"}
    async with httpx.AsyncClient(timeout=8.0) as client:
        try:
            response = await client.get(FEED_URL, headers=headers)
            if response.status_code == 200:
                process_and_cache_feed(response.json())
            else:
                with cache_lock: engine_cache["external_sync"]["sync_errors"] += 1
        except Exception:
            with cache_lock: engine_cache["external_sync"]["sync_errors"] += 1

def process_and_cache_feed(data):
    with cache_lock:
        if "games" in data:
            updated_list = []
            for g in data["games"]:
                sport = g.get("sport", "").upper()
                if sport == "MLB" or g.get("is_puck_line", False): continue
                if g.get("deviation_score", 0.0) >= engine_cache["metrics_config"]["game_script_panic_threshold"]:
                    updated_list.append({
                        "game": g.get("game_name"), "public_money_pct": g.get("public_pct"),
                        "line_movement": g.get("movement"), "alert": "PANIC_THRESHOLD_TRIGGERED"
                    })
            engine_cache["nhl_slate"]["external_updates"] = updated_list
        engine_cache["external_sync"]["status"] = "synced"
        engine_cache["external_sync"]["last_updated"] = datetime.now().strftime("%m-%d-%Y %I:%M %p")

def start_sync_worker(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(fetch_external_feed())

@app.route("/")
def index():
    with cache_lock:
        try:
            # Try loading the template file if it exists
            return render_template("dashboard.html", cache=engine_cache)
        except Exception:
            # Safe layout fallback to prevent status 1 startup crashes
            return render_template_string(FALLBACK_HTML, cache=engine_cache)

@app.route("/api/v5/engine/cache", methods=["GET"])
def get_engine_cache():
    with cache_lock: return jsonify(engine_cache)

@app.route("/api/v5/engine/sync", methods=["POST"])
def trigger_manual_sync():
    worker_loop = asyncio.new_event_loop()
    t = threading.Thread(target=start_sync_worker, args=(worker_loop,), daemon=True)
    t.start()
    return jsonify({"status": "sync_sequence_pushed_to_background", "engine_state": "listening"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
