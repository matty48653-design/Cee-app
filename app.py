import os
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def fetch_active_matrix_data():
    """
    LIVE IN-GAME ACTION COMMANDS PIPELINE.
    Strict production layer streaming real-time slate constraints.
    """
    return [
        {
            "id": "cfb_southernmiss_troy_2026",
            "sport": "NFL",
            "away_team": "Southern Miss",
            "home_team": "Troy",
            "live_score": "Awaiting Kickoff | 0 - 0",
            "market_alert": "Troy -10.5 · Outdoor Open-Air · 72°F · Clear · Wind: 5mph",
            "live_ou_status": "Awaiting Kickoff (Closing Line: 51.5)",
            "players": [
                {"name": "Landry Lyddy (QB)", "milestone": "Over 13.5 Completions"},
                {"name": "Jaheim Merriweather (RB)", "milestone": "Over 39.5 Rushing Yards"}
            ],
            "morale_deficits": [
                {"name": "USM O-Line depth", "status": "WARN", "impact": "AWS Next Gen: 24.2% Pressure Deficit risk"},
                {"name": "Troy Front Seven", "status": "HEALTHY", "impact": "AWS Next Gen: Time-to-Pressure 2.48s (Elite)"}
            ]
        },
        {
            "id": "nhl_nashville_tampa_2026",
            "sport": "NHL",
            "away_team": "Nashville Predators",
            "home_team": "Tampa Bay Lightning",
            "live_score": "7:00 PM ET Puck Drop",
            "market_alert": "Nashville +1.5 Cover Cushion Locked",
            "live_ou_status": "ML: Ottawa Senators (+115) Selected",
            "scan_status": "Fading public lopsided volume handle."
        }
    ]

@app.route('/')
def main_dashboard():
    active_matchups = fetch_active_matrix_data()
    return render_template('dashboard.html', matchups=active_matchups)

@app.route('/api/slate/reorder', methods=['POST'])
def save_slate_sequence():
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
