import os
import json
import time
import datetime
import requests
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'sports_data.json')

# 🐋 CEE Syndicate Implied Probability Value Algorithm
def calculate_whale_probability_edge(american_odds, real_world_probability):
    if american_odds > 0:
        implied_prob = 100 / (american_odds + 100)
    else:
        implied_prob = abs(american_odds) / (abs(american_odds) + 100)
        
    edge_gap = real_world_probability - implied_prob
    
    if edge_gap >= 0.05:
        system_status = "🐋 ALPHA WHALE SIGNAL: HEAVY MISPRICING EXPOSED"
    elif edge_gap > 0:
        system_status = "📊 MARGINAL VALUE ATTAINED"
    else:
        system_status = "🪤 PUBLIC TRAP LINE: DEFENSIVE OVER-JUICING"
        
    return {
        "bookmaker_implied_prob_pct": round(implied_prob * 100, 2),
        "true_volume_probability_pct": round(real_world_probability * 100, 2),
        "extracted_edge_pct": round(edge_gap * 100, 2),
        "cee_matrix_signal": system_status
    }

# Core API Ingestion Function
def get_live_matrix_feeds():
    api_key = os.environ.get("SPORTS_DATA_KEY")
    
    if not api_key:
        return [
            {
                "id": "game_1",
                "sport": "CFB",
                "matchup": "Sam Houston @ Liberty",
                "venue": "Williams Stadium",
                "time_label": "THU 7:00 PM • UPCOMING",
                "spread_line": "Liberty -13.5",
                "ou_line": "O/U 52.5",
                "trajectory": "1,220 Miles East • Severe Fatigue Threshold Cross",
                "crowd_env": "Lynchburg Hostile • Decibel Index: High (Cap Playbook Comm)",
                "injury_notes": "Sam Houston WR1 (Questionable - Hamstring) • Limits deep vertical options",
                "morale_notes": "High Volatility • Body language from coaching staff brushing late-game defensive lapse"
            },
            {
                "id": "game_2",
                "sport": "CFB",
                "matchup": "South Florida @ UTSA",
                "venue": "Alamodome",
                "time_label": "THU 7:30 PM • UPCOMING",
                "spread_line": "UTSA -4.5",
                "ou_line": "O/U 58.5",
                "trajectory": "1,140 Miles West • 2 Time Zone Shift Effect",
                "crowd_env": "Dome Enclosure Noise Multiplier • Favors Ground Cadence",
                "injury_notes": "USF Starting Right Tackle (OUT - Ankle) • Weakens front edge protection",
                "morale_notes": "Stable Core • Focused on heavy trench script to offset line injuries"
            },
            {
                "id": "game_3",
                "sport": "NHL",
                "matchup": "Montreal Canadiens @ Boston Bruins",
                "venue": "TD Garden • Arena Main Track",
                "time_label": "THU 7:00 PM • UPCOMING",
                "spread_line": "Bruins Moneyline",
                "ou_line": "O/U 6.0",
                "trajectory": "310 Miles South • Minimal Rest Restriction Impact",
                "crowd_env": "TD Garden High Intensity • Amplifies Early Period Whistles",
                "injury_notes": "Boston Clear • Montreal Defenceman (Day-to-Day - Upper Body)",
                "morale_notes": "Rivalry Peak Intensity"
            }
        ]
    
    url = "https://api-sports.io"
    headers = {"x-apisports-key": api_key}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response.json().get("results", [])
    except Exception:
        return []

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_data(data):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving data: {e}")

@app.route('/')
def index():
    matrix_data = load_data()
    game_feeds = get_live_matrix_feeds()
    return render_template('index.html', whale_data=matrix_data, feeds=game_feeds)

@app.route('/api/matrix/update', methods=['POST'])
def update_matrix_data():
    try:
        payload = request.get_json()
        if not payload:
            return jsonify({"error": "No data provided"}), 400
        
        save_data(payload)
        return jsonify({"status": "success", "message": "Whale tracking matrix updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
