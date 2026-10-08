import os
import json
import time
import threading
from flask import Flask, render_template, jsonify

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'sports_data.json')

def load_live_matrix():
    """Dynamically reads current market data states straight from the local cache file."""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Matrix Read Error: {e}")
    
    return {
        "framework_version": "9.5-Quantum-Core",
        "last_checked": "Scanning",
        "syndicate_tracking": [{"group": "Global Syndicate", "size": "Size: 1x", "wager": "Syncing System", "sentiment": "Neutral"}],
        "directive_sheet": [{"label": "MARKET MONITOR", "value": "Initial Scan", "desc": "Waking backend background loops."}],
        "live_slate_monitor": []
    }

def automated_background_timer_loop():
    """Background worker daemon thread that runs your scraper completely on autopilot."""
    print("🚀 Background Automation Daemon Successfully Armed...")
    while True:
        try:
            # Sleep first on cold server boot to allow server assignment
            time.sleep(600)  # Executes data scrape loops precisely every 10 minutes (600 seconds)
            print("🔄 Background Timer Triggered: Fetching fresh sportsbook lines...")
            
            import feed_bridge
            import importlib
            importlib.reload(feed_bridge)
            feed_bridge.fetch_network_feeds()
            
        except Exception as e:
            print(f"Background Daemon Worker Exception: {e}")

@app.route("/")
def index():
    live_cache = load_live_matrix()
    return render_template("dashboard.html", cache=live_cache)

@app.route("/api/v9/engine/cache", methods=["GET"])
def get_engine_cache():
    return jsonify(load_live_matrix())

@app.route("/update-matrix")
def trigger_feed_bridge():
    """Fallback route providing on-demand forced manual overrides whenever needed."""
    try:
        import feed_bridge
        import importlib
        importlib.reload(feed_bridge)
        feed_bridge.fetch_network_feeds()
        return "<h1>Matrix Cache Successfully Updated! Go check your dashboard.</h1>"
    except Exception as e:
        return f"<h1>Update Failed: {str(e)}</h1>", 500

if __name__ == "__main__":
    # Arm and initialize the parallel background execution layer
    daemon_thread = threading.Thread(target=automated_background_timer_loop)
    daemon_thread.daemon = True
    daemon_thread.start()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
