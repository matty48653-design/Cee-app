import os
import json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# JSON persistence storage configuration tracking map
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), 'slate_settings.json')

def load_slate_order():
    """Reads the stored matrix order parameters safely from disk."""
    if not os.path.exists(SETTINGS_FILE):
        return {}
    try:
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {}

def save_slate_order(order_map):
    """Saves the layout priority dictionary configuration file securely."""
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(order_map, f, indent=4)
        return True
    except Exception:
        return False

def fetch_active_matrix_data():
    """
    Mock data engine matching your data schema.
    Replace this helper function body with your live scraping / API scraper loop.
    """
    return [
        {
            "id": "nfl_game_1",
            "sport": "NFL",
            "away_team": "Atlanta Falcons",
            "home_team": "New Orleans Saints",
            "time": "8:15 PM ET",
            "market_alert": "Saints -1.5 (Trap Flagged 🚨)",
            "players": [
                {"name": "Bijan Robinson (RB)", "milestone": "Over 50.5 Rush Yds", "integrity": "PREMIUM FLOOR"},
                {"name": "Michael Penix Jr. (QB)", "milestone": "Over 200.5 Pass Yds", "integrity": "SHARP INTEGRITY"}
            ],
            "morale_deficits": [
                {"name": "Kaden Elliss (LB)", "status": "OUT", "impact": "Front-Seven Depth Core Collapse"},
                {"name": "Carl Granderson (DE)", "status": "OUT", "impact": "Pass Rush Containment Void"}
            ]
        },
        {
            "id": "nhl_game_1",
            "sport": "NHL",
            "away_team": "Philadelphia Flyers",
            "home_team": "Tampa Bay Lightning",
            "time": "7:00 PM ET",
            "market_alert": "Money Line / Totals Only (Puck Line Blocked)",
            "scan_status": "Scanning Money Flow..."
        }
    ]

@app.route('/')
def main_dashboard():
    """Renders data matrix items organized by custom ordering profiles."""
    active_matchups = fetch_active_matrix_data()
    order_map = load_slate_order()
    
    # Sort items sequentially. Elements missing weights append to fallback priority rows.
    active_matchups.sort(key=lambda x: order_map.get(str(x.get('id')), 999))
    
    return render_template('dashboard.html', matchups=active_matchups)

@app.route('/api/slate/reorder', methods=['POST'])
def save_slate_sequence():
    """Receives sequence array data from client views and dumps updates into storage files."""
    data = request.get_json() or {}
    ordered_ids = data.get('ordered_ids', [])
    
    if not ordered_ids:
        return jsonify({"status": "error", "message": "Missing ID tracking array parameter"}), 400
        
    # Map matching array items to an integer-keyed priority dictionary
    order_map = {str(item_id): index for index, item_id in enumerate(ordered_ids)}
    
    if save_slate_order(order_map):
        return jsonify({"status": "success", "message": "JSON Matrix persistence sync completed"})
    return jsonify({"status": "error", "message": "Failed writing state settings map to workspace storage disk"}), 500

if __name__ == '__main__':
    app.run(debug=True)
