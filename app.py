import os
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def fetch_active_matrix_data():
    return [
        {
            "id": "cfb_southernmiss_troy_2026",
            "sport": "NFL",
            "away_team": "Southern Miss",
            "home_team": "Troy",
            "time": "8:00 PM ET",
            "market_alert": "Troy -10.5 (Slider Protection Active 🛡️)",
            "players": [
                {"name": "Troy Primary RB", "milestone": "Over 2.5 Receptions"},
                {"name": "USM Target WR", "milestone": "Over 4.5 Receptions"}
            ],
            "morale_deficits": [
                {"name": "USM Front Seven", "status": "WARN", "impact": "High ground volatility"}
            ]
        },
        {
            "id": "nhl_islanders_rangers_2026",
            "sport": "NHL",
            "away_team": "NY Islanders",
            "home_team": "NY Rangers",
            "time": "7:30 PM ET",
            "market_alert": "Money Line / Totals Only",
            "scan_status": "Tracking Sharp Money..."
        }
    ]

@app.route('/')
def main_dashboard():
    active_matchups = fetch_active_matrix_data()
    return render_template('dashboard.html', matchups=active_matchups)

@app.route('/api/slate/reorder', methods=['POST'])
def save_slate_sequence():
    return jsonify({"status": "success", "message": "Sequence synced"})

if __name__ == '__main__':
    app.run(debug=True)
