import os
import json
import subprocess
import threading
from flask import Flask, jsonify, render_template, render_template_string

app = Flask(__name__)

def run_live_feed_bridge():
    """Wakes up the CEE inbound data gate scraper on complete autopilot."""
    try:
        bridge_path = os.path.join(os.path.dirname(__file__), "feed_bridge.py")
        if os.path.exists(bridge_path):
            subprocess.Popen(["python", bridge_path])
    except Exception:
        pass

def load_live_feed_cache():
    """Pure live cache reader pulling real tracking percentages onto your screen."""
    json_path = os.path.join(os.path.dirname(__file__), "sports_data.json")
    if os.path.exists(json_path):
        try:
            with open(json_path, "r") as f:
                data = json.load(f)
                if "slates" in data:
                    return data
        except Exception:
            pass
    return {"slates": []}

@app.route("/")
def index():
    # Automatically fire the background scraper loop on every single view refresh
    threading.Thread(target=run_live_feed_bridge, daemon=True).start()
    
    cache_data = load_live_feed_cache()
    try:
        return render_template("dashboard.html", cache=cache_data)
    except Exception:
        return "<html><body><h1>CEE Matrix Active - Processing Inbound Data Gate...</h1></body></html>"

@app.route("/api/v5/engine/cache", methods=["GET"])
def get_engine_cache():
    return jsonify(load_live_feed_cache())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
