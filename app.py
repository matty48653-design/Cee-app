import os
import json
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Ensure the active directory matches the script path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'sports_data.json')

def load_live_matrix():
    """Reads real-time data directly from the live scraper output file."""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Matrix Read Error: {e}")
    
    # Clean baseline structure if file is momentarily locked or empty
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
    # Pull the freshest real-world data straight from the JSON cache on refresh
    live_cache = load_live_matrix()
    return render_template("dashboard.html", cache=live_cache)

@app.route("/api/v9/engine/cache", methods=["GET"])
def get_engine_cache():
    # API endpoint for client-side live polling if needed later
    return jsonify(load_live_matrix())

if __name__ == "__main__":
    # Bound specifically to production environment ports for Render deployment
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
