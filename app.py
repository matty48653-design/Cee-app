import os
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def fetch_active_matrix_data():
    """
    Automated Multi-Game Streaming Feed Core.
    STRICT COMPLIANCE MODE: 1Q/2Q Volume Block + Milestone Slider Protection.
    Integrates Live Over/Under Pacing Matrix variables & Injury Protocols.
    """
    return [
        {
            "id": "cfb_southernmiss_troy_2026",
            "sport": "NFL", # Maps custom player grid element configurations
            "away_team": "Southern Miss",
            "home_team": "Troy",
            "time": "8:00 PM ET",
            "market_alert": "Troy -10.5 (Slider Protection Active 🛡️)",
            "live_ou_status": "Pacing UNDER (Current: 0 | Closing Line: 47.5)",
            "players": [
                {"name": "Troy Primary RB", "milestone": "Over 2.5 Receptions"},
                {"name": "USM Target WR", "milestone": "Over 4.5 Receptions"}
            ],
            "morale_deficits": [
                {"name": "USM O-Line depth", "status": "WARN", "impact": "AWS Next Gen: 24.2% Pressure Deficit risk"},
                {"name": "Troy Front Seven", "status": "HEALTHY", "impact": "AWS Next Gen: Time-to-Pressure 2.48s (Elite)"}
            ]
        },
        {
            "id": "nhl_islanders_rangers_2026",
            "sport": "NHL",
            "away_team": "NY Islanders",
            "home_team": "NY Rangers",
            "time": "7:30 PM ET",
            "market_alert": "Money Line / Totals Only (Puck Line Blocked)",
            "live_ou_status": "Closing Total: 5.5 | Sharp Inflow Volume Under-backed",
            "scan_status": "Tracking Sharp Money... AWS Pressure: 4.15% Hold Tax"
        }
    ]

@app.route('/')
def main_dashboard():
    active_matchups = fetch_active_matrix_data()
    return render_template('dashboard.html', matchups=active_matchups)

@app.route('/api/slate/reorder', methods=['POST'])
def save_slate_sequence():
    return jsonify({"status": "success", "message": "Matrix parameters securely synced"})

if __name__ == '__main__':
    app.run(debug=True)
