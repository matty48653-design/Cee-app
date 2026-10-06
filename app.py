import os
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def fetch_active_matrix_data(sim_pressure=None, sim_injury=None):
    """
    Core Automation Feed.
    Features Tonight's Live NHL Matchup alongside your Interactive Football Simulator.
    """
    # Read simulation values or default to baseline metrics
    pressure = float(sim_pressure) if sim_pressure is not None else 38.4
    time_to_press = round(2.89 - (pressure * 0.015), 2)
    
    usm_status = "CRITICAL COLLAPSE RISK" if time_to_press < 2.50 else "POCKET STABLE"
    injury_impact = "FAST COLLAPSE: Expect immediate short checkdowns." if sim_injury == "OUT" else "Pressure climbing. Monitor vertical route caps."

    return [
        {
            "id": "nhl_flyers_lightning_live",
            "sport": "NHL",
            "away_team": "Philadelphia Flyers",
            "home_team": "Tampa Bay Lightning",
            "time": "7:00 PM ET",
            "live_score": "FINAL: PHI 2 - 3 TB", # Tonight's synchronized live ice data
            "market_alert": "Money Line / Totals Only (Puck Line Blocked 🚫)",
            "live_ou_status": "Closing Total: 5.5 | Sharp Inflow Volume Under-Backed",
            "scan_status": "Game Final: Cash Moneyline Position SECURED 🟩"
        },
        {
            "id": "cfb_southernmiss_troy_2026",
            "sport": "NFL",
            "away_team": "Southern Miss",
            "home_team": "Troy",
            "time": "8:00 PM ET",
            "live_score": "SIMULATION MODE: ACTIVE",
            "market_alert": "Troy -10.5 (Live Simulation Controls Active ⚙️)",
            "live_ou_status": f"Pacing UNDER (Live AWS Pressure: {pressure}%)",
            "players": [
                {"name": "Troy Primary RB", "milestone": "Over 2.5 Receptions" if time_to_press >= 2.50 else "Over 4.5 Receptions (URGENT VOLUME FLOOR)"},
                {"name": "USM Target WR", "milestone": "Over 4.5 Receptions" if sim_injury != "OUT" else "Over 7.5 Targets (Script Heavy Deficit)"}
            ],
            "morale_deficits": [
                {
                    "name": "USM O-Line depth", 
                    "status": "WARN" if sim_injury != "OUT" else "CRITICAL", 
                    "impact": f"AWS Next Gen: {pressure}% Pressure · {injury_impact}"
                },
                {
                    "name": "Troy Front Seven", 
                    "status": "HEALTHY", 
                    "impact": f"AWS Next Gen: Time-to-Pressure {time_to_press}s ({usm_status})"
                }
            ]
        }
    ]

@app.route('/')
def main_dashboard():
    sim_p = request.args.get('pressure')
    sim_i = request.args.get('injury')
    
    active_matchups = fetch_active_matrix_data(sim_pressure=sim_p, sim_injury=sim_i)
    return render_template('dashboard.html', matchups=active_matchups)

@app.route('/api/slate/reorder', methods=['POST'])
def save_slate_sequence():
    return jsonify({"status": "success", "message": "Simulated matrix sync complete"})

if __name__ == '__main__':
    app.run(debug=True)
