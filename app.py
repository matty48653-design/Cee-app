import os
import json
from flask import Flask, render_template, jsonify

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'sports_data.json')

def load_live_matrix():
    """Dynamically reads real-time market data from the live JSON file."""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Matrix Read Error: {e}")
    
    # Pure fallback matrix structure to keep templates alive if file is reading
    return {
        "framework_version": "9.5-Quantum-Core",
        "global_rules": {
            "block_volatile_micro_lines": True,
            "enforce_milestone_slider_floors": True
        },
        "nfl_player_props": {"status": "offline", "milestones": []},
        "cfb_slate": {"status": "offline", "games": []},
        "nhl_slate": {"status": "offline", "games": []}
    }

@app.route("/")
def index():
    # Pulls fresh real-world data straight from the JSON file on every page reload
    live_cache = load_live_matrix()
    return render_template("dashboard.html", cache=live_cache)

@app.route("/api/v9/engine/cache", methods=["GET"])
def get_engine_cache():
    return jsonify(load_live_matrix())

@app.route("/update-matrix")
def trigger_feed_bridge():
    """Hidden web route that triggers your scraper to fetch fresh data on click."""
    try:
        import feed_bridge
        import importlib
        
        # This forces Python to run the scraper fresh instead of reading old cache
        importlib.reload(feed_bridge)
        feed_bridge.fetch_network_feeds()
        
        return "<h1>Matrix Cache Successfully Updated! Go check your dashboard.</h1>"
    except Exception as e:
        return f"<h1>Update Failed: {str(e)}</h1>", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
