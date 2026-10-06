import os
import httpx
import asyncio
import threading
from datetime import datetime
from flask import Flask, jsonify, render_template

app = Flask(__name__)

# ==========================================
# CEE v5.3 PRODUCTION ENGINE CACHE
# ==========================================
engine_cache = {
    "framework_version": "5.3-Clean-Table-Matrix",
    "last_sync_timestamp": "10-06-2026 09:08 AM",
    "global_rules": {
        "block_volatile_micro_lines": True,
        "enforce_milestone_slider_floors": True,
        "block_puck_lines": True,
        "block_mlb_feed": True
    },
    "metrics_config": {
        "game_script_panic_threshold": 0.72,  # Captures extreme line variance
        "morale_deficit_penalty": 0.15       # Adjusts psychological performance impact
    },
    "nhl_slate": {
        "status": "locked",
        "games": [
            {
                "matchup": "Red Wings @ Panthers",
                "ou": 6.5,
                "status": "waiting_puck_drop",
                "contrarian_edge": "SHARP_MONEY_SPLIT"
            },
            {
                "matchup": "Panthers @ Kings",
                "ou": 6.0,
                "status": "waiting_puck_drop",
                "contrarian_edge": "LINE_FREEZE"
            }
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

# Thread-safety lock for cache mutations
cache_lock = threading.Lock()

# ==========================================
# ASYNCHRONOUS CONCURRENCY DAEMON
# ==========================================
async def fetch_external_feed():
    """
    Background worker listening to live data feeds.
    Safely enforces v5.3 backend rules (rejects puck lines/MLB).
    """
    FEED_URL = os.getenv("CONTRARIAN_DATA_FEED_URL", "https://external-odds-sync.local")
    headers = {"Authorization": f"Bearer {os.getenv('FEED_AUTH_TOKEN', 'default_secure_token')}"}
    
    async with httpx.AsyncClient(timeout=8.0) as client:
        try:
            response = await client.get(FEED_URL, headers=headers)
            if response.status_code == 200:
                raw_data = response.json()
                process_and_cache_feed(raw_data)
            else:
                with cache_lock:
                    engine_cache["external_sync"]["sync_errors"] += 1
        except Exception:
            with cache_lock:
                engine_cache["external_sync"]["sync_errors"] += 1

def process_and_cache_feed(data):
    """
    Parses live data streams, mapping exclusively to valid money lines,
    over/unders, and passing/rushing player prop milestones.
    """
    with cache_lock:
        if "games" in data:
            updated_list = []
            for g in data["games"]:
                # STRICTOR FILTERING: Enforce backend blocks
                sport = g.get("sport", "").upper()
                if sport == "MLB" or g.get("is_puck_line", False):
                    continue  # Explicitly drop blocked data streams
                
                # Check line movements against your Game-Script Panic Threshold
                if g.get("deviation_score", 0.0) >= engine_cache["metrics_config"]["game_script_panic_threshold"]:
                    updated_list.append({
                        "game": g.get("game_name"),
                        "public_money_pct": g.get("public_pct"),
                        "line_movement": g.get("movement"),
                        "alert": "PANIC_THRESHOLD_TRIGGERED"
                    })
            
            engine_cache["nhl_slate"]["external_updates"] = updated_list
            
        engine_cache["external_sync"]["status"] = "synced"
        engine_cache["external_sync"]["last_updated"] = datetime.now().strftime("%m-%d-%Y %I:%M %p")

def start_sync_worker(loop):
    """Daemon thread loop execution context."""
    asyncio.set_event_loop(loop)
    loop.run_until_complete(fetch_external_feed())

# ==========================================
# FLASK INTERFACE LAYER
# ==========================================
@app.route("/")
def index():
    """Serves the flat compact dashboard interface without a score ticker."""
    with cache_lock:
        return render_template("dashboard.html", cache=engine_cache)

@app.route("/api/v5/engine/cache", methods=["GET"])
def get_engine_cache():
    """Secure endpoint for checking your internal matrix metrics on the fly."""
    with cache_lock:
        return jsonify(engine_cache)

@app.route("/api/v5/engine/sync", methods=["POST"])
def trigger_manual_sync():
    """Triggers background data pull securely without blocking Render web traffic."""
    worker_loop = asyncio.new_event_loop()
    t = threading.Thread(target=start_sync_worker, args=(worker_loop,), daemon=True)
    t.start()
    return jsonify({
        "status": "sync_sequence_pushed_to_background",
        "engine_state": "listening"
    })

if __name__ == "__main__":
    # Runs the application engine securely matching container environments
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
