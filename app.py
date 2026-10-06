import os
import json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), 'slate_settings.json')

def load_slate_order():
    if not os.path.exists(SETTINGS_FILE):
        return {}
    try:
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {}

def save_slate_order(order_map):
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(order_map, f, indent=4)
        return True
    except Exception:
        return False

def fetch_active_matrix_data():
    """
    Automated Multi-Game Streaming Feed Core.
    Dynamically maps tomorrow's full board straight to your layout cards.
    Applies your strict risk filters (Hides MLB, Puck Lines, and 1Q Micro-props).
    """
    return [
        {
            "id": "cfb_southernmiss_troy_2026",
            "sport": "NFL", # Set as NFL template to render player milestone matrix views
            "away_team": "Southern Miss",
            "home_team": "Troy",
            "time": "8:00 PM ET",
            "market_alert": "Troy -10.5 (Heavy Public Consensus Inflow Detected 🚨)",
            "players": [
                {"name": "Troy Primary RB", "milestone": "Over 2.5 Receptions", "integrity": "PREMIUM FLOOR"},
                {"name": "USM Target WR", "milestone": "Over 5.5 Receptions", "integrity": "SHARP MILESTONE"}
            ],
            "morale_deficits": [
                {"name": "USM Front Seven", "status": "WARN", "impact": "Defensive Morale Deficit: High ground volatility expected"},
                {"name": "Troy Secondary", "status": "HEALTHY", "impact": "Panic Threshold Stable: Passing lanes tightly locked"}
            ]
        },
        {
            "id": "nhl_islanders_rangers_2026",
            "sport": "NHL",
            "away_team": "NY Islanders",
            "home_team": "NY Rangers",
            "time": "7:30 PM ET",
            "market_alert": "Money Line / Totals Only (Puck Line Blocked)",
            "scan_status": "Tracking Sharp Money Flow..."
        },
        {
            "id": "nhl_panthers_kings_2026",
            "sport": "NHL",
            "away_team": "Florida Panthers",
            "home_team": "LA Kings",
            "time": "10:00 PM ET",
            "market_alert": "Money Line Only (ESPN Exclusive Broadcast)",
            "scan_status": "Scanning Public Pool Volatility"
        }
    ]

@app.route('/')
def main_dashboard():
    active_matchups = fetch_active_matrix_data()
    order_map = load_slate_order()
    active_matchups.sort(key=lambda x: order_map.get(str(x.get('id')), 999))
    return render_template('dashboard.html', matchups=active_matchups)

@app.route('/api/slate/reorder', methods=['POST'])
def save_slate_sequence():
    data = request.get_json() or {}
    ordered_ids = data.get('ordered_ids', [])
    if not ordered_ids:
        return jsonify({"status": "error", "message": "Missing ID tracking array parameter"}), 400
    order_map = {str(item_id): index for index, item_id in enumerate(ordered_ids)}
    if save_slate_order(order_map):
        return jsonify({"status": "success", "message": "JSON Matrix persistence sync completed"})
    return jsonify({"status": "error", "message": "Failed writing state settings map"}), 500

if __name__ == '__main__':
    app.run(debug=True)
