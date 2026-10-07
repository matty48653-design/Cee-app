import os
import json
import subprocess
import threading
from flask import Flask, jsonify, render_template, render_template_string

app = Flask(__name__)

def run_live_feed_bridge():
    """Triggers your background feed bridge script to scrape live real-world lines."""
    try:
        bridge_path = os.path.join(os.path.dirname(__file__), "feed_bridge.py")
        if os.path.exists(bridge_path):
            subprocess.Popen(["python", bridge_path])
    except Exception:
        pass

def load_live_feed_cache():
    """Reads strictly from your sports_data.json live scraper file."""
    json_path = os.path.join(os.path.dirname(__file__), "sports_data.json")
    if os.path.exists(json_path):
        try:
            with open(json_path, "r") as f:
                return json.load(f)
        except Exception:
            pass
    # Empty fallback structure so the HTML framework doesn't throw a server error 500 crash
    return {"low_volume_splits": {"games": []}, "nfl_player_props": {"milestones": []}, "nhl_slate": {"games": []}}

@app.route("/")
def index():
    # Asynchronously launch the feed bridge script on every refresh to pull real lines
    threading.Thread(target=run_live_feed_bridge, daemon=True).start()
    
    cache_data = load_live_feed_cache()
    try:
        return render_template("dashboard.html", cache=cache_data)
    except Exception:
        return "<html><body><h1>CEE Matrix Active - Processing Real-World Feed Lines</h1></body></html>"

@app.route("/api/v5/engine/cache", methods=["GET"])
def get_engine_cache():
    return jsonify(load_live_feed_cache())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
