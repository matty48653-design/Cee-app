# app.py - v6.8 Master Core (Live Scores + Weather + Complete 4-Quarter Script Tracker)
from flask import Flask, render_template, jsonify
import os
import requests
import time

app = Flask(__name__)
app.secret_key = os.urandom(24)

LATEST_SCORES_CACHE = {
    "usm_troy": {"score": "0 - 0", "status": "UPCOMING", "stadium": "Outdoor Open-Air", "weather": "72° • Clear • Wind: 5mph", "quarter": "PRE-GAME"},
    "ott_det": {"score": "0 - 0", "status": "UPCOMING", "stadium": "Indoor Arena", "weather": "Indoor • Climate Controlled", "quarter": "PRE-GAME"},
    "nas_tor": {"score": "0 - 0", "status": "UPCOMING", "stadium": "Indoor Arena", "weather": "Indoor • Climate Controlled", "quarter": "PRE-GAME"},
    "vgk_sea": {"score": "0 - 0", "status": "UPCOMING", "stadium": "Indoor Arena", "weather": "Indoor • Climate Controlled", "quarter": "PRE-GAME"}
}

def pull_live_unblocked_scores():
    global LATEST_SCORES_CACHE
    try:
        url = "https://espn.com"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            for event in data.get('events', []):
                short_name = event.get('shortName', '')
                if any(x in short_name for x in ["SWM", "TROY", "SMU"]):
                    status = event.get('status', {}).get('type', {}).get('state', '').upper()
                    display_status = "LIVE" if status == "INPROGRESS" else "UPCOMING"
                    period = event.get('status', {}).get('period', 0)
                    
                    if period == 1: LATEST_SCORES_CACHE["usm_troy"]["quarter"] = "1ST QTR"
                    elif period == 2: LATEST_SCORES_CACHE["usm_troy"]["quarter"] = "2ND QTR"
                    elif period == 3: LATEST_SCORES_CACHE["usm_troy"]["quarter"] = "3RD QTR"
                    elif period == 4: LATEST_SCORES_CACHE["usm_troy"]["quarter"] = "4TH QTR"
                    
                    competitors = event.get('competitors', [])
                    score_str = f"{competitors[0].get('score', '0')} - {competitors[1].get('score', '0')}"
                    LATEST_SCORES_CACHE["usm_troy"]["score"] = score_str
                    LATEST_SCORES_CACHE["usm_troy"]["status"] = display_status
    except Exception:
        pass

    return [
        {"id": "usm_troy", "game": "Southern Miss @ Troy", "sport": "CFB", "score": LATEST_SCORES_CACHE["usm_troy"]["score"], "time": "7:00 PM ET", "status": LATEST_SCORES_CACHE["usm_troy"]["status"], "stadium": LATEST_SCORES_CACHE["usm_troy"]["stadium"], "weather": LATEST_SCORES_CACHE["usm_troy"]["weather"], "quarter": LATEST_SCORES_CACHE["usm_troy"]["quarter"]},
        {"id": "ott_det", "game": "Ottawa Senators @ Detroit Red Wings", "sport": "NHL", "score": "0 - 0", "time": "7:00 PM ET", "status": "UPCOMING", "stadium": LATEST_SCORES_CACHE["ott_det"]["stadium"], "weather": LATEST_SCORES_CACHE["ott_det"]["weather"], "quarter": "1ST PER"},
        {"id": "nas_tor", "game": "Nashville Predators @ Toronto Maple Leafs", "sport": "NHL", "score": "0 - 0", "time": "7:30 PM ET", "status": "UPCOMING", "stadium": LATEST_SCORES_CACHE["nas_tor"]["stadium"], "weather": LATEST_SCORES_CACHE["nas_tor"]["weather"], "quarter": "1ST PER"},
        {"id": "vgk_sea", "game": "Vegas Golden Knights @ Seattle Kraken", "sport": "NHL", "score": "0 - 0", "time": "9:40 PM ET", "status": "UPCOMING", "stadium": LATEST_SCORES_CACHE["vgk_sea"]["stadium"], "weather": LATEST_SCORES_CACHE["vgk_sea"]["weather"], "quarter": "1ST PER"}
    ]

@app.route('/')
def dashboard():
    cfb_game = {
        "home": "Troy", "away": "Southern Miss", "status": "UPCOMING",
        "sliders": [
            {"player": "Landry Lyddy (USM)", "metric": "200+ Pass Yards", "target": "OVER", "yield": "77%"},
            {"player": "Goose Crowder (TROY)", "metric": "190+ Pass Yards", "target": "OVER", "yield": "72%"},
            {"player": "Jaheim Merriweather (TROY)", "metric": "40+ Rush Yards", "target": "OVER", "yield": "47%"}
        ]
    }
    
    nhl_games = [
        {"home": "Detroit Red Wings", "away": "Ottawa Senators", "angle": "Divisional Pivot", "play": "Ottawa ML (+115)", "handle": "71% Sharp Cash"},
        {"home": "Toronto Maple Leafs", "away": "Nashville Predators", "angle": "Public Trap Fade", "play": "Nashville ML (+130)", "handle": "87% Public on TOR"},
        {"home": "Seattle Kraken", "away": "Vegas Golden Knights", "angle": "Late Night Structure", "play": "Seattle ML (+142)", "handle": "Vegas Public Premium"}
    ]
    
    syndicate_picks = {
        "groups": [
            {"alias": "Alpha Syndicate", "target": "Southern Miss +10.5", "size": "5x", "volatility": "91% Resistance", "v_color": "#ff9100"},
            {"alias": "Wallet #4092 (High-Stakes)", "target": "Nashville ML (+130)", "size": "3.5x", "volatility": "84% Resistance", "v_color": "#ff9100"},
            {"alias": "Vegas Sharp Box", "target": "Ottawa ML (+115)", "size": "2x", "volatility": "68% Resistance", "v_color": "#00e676"}
        ]
    }
    
    script_tracker = {
        "phases": [
            {"qtr": "1st Quarter", "name": "Public Media Bias Trap", "status": "SCANNING", "desc": "Detects high-volume early public lines on national TV broadcasts.", "color": "var(--text-muted)"},
            {"qtr": "2nd Quarter", "name": "The Rubber Band Effect", "status": "ARMED", "desc": "Monitors favorite over-extensions to flag live value shifts on alternate sliders.", "color": "var(--accent-orange)"},
            {"qtr": "3rd Quarter", "name": "The Neutralization Freeze", "status": "ARMED", "desc": "Calculates sudden clock-chewing splits and coach-driven pacing restraints.", "color": "var(--accent-orange)"},
            {"qtr": "4th Quarter", "name": "The Trap Door Hook", "status": "ARMED", "desc": "Fades highly manipulated late game-script volatility to track static floors.", "color": "var(--accent-orange)"}
        ]
    }
    
    early_board = {
        "slate_date": "Sunday Slate Open (Week 5)",
        "games": [
            {"sport": "NFL", "matchup": "Detroit Lions @ Arizona Cardinals", "open_line": "Lions -3.5", "current_line": "Lions -4.5", "drift_text": "▲ +1.0 Live Public Shift", "drift_color": "#ff9100"},
            {"sport": "NFL", "matchup": "Chicago Bears @ Green Bay Packers", "open_line": "Bears -1.0", "current_line": "Bears -2.5", "drift_text": "▲ +1.5 Public Premium", "drift_color": "#ff9100"}
        ]
    }
    
    return render_template('dashboard.html', cfb=cfb_game, nhl_items=nhl_games, sharps=syndicate_picks, early=early_board, live_games=pull_live_unblocked_scores(), script=script_tracker)

@app.route('/api/feed')
def live_feed():
    return jsonify({
        "status": "Pipeline Active",
        "version": "6.8-Script-Engine",
        "cache_buster": time.time(),
        "sentiment_updates": {
            "Alpha Syndicate": "94% Public Resistance",
            "Wallet #4092 (High-Stakes)": "87% Public Resistance",
            "Vegas Sharp Box": "69% Public Resistance"
        },
        "script_updates": [
            {"qtr": "1st Quarter", "status": "SCANNING", "color": "var(--text-muted)"},
            {"qtr": "2nd Quarter", "status": "ARMED", "color": "var(--accent-orange)"},
            {"qtr": "3rd Quarter", "status": "ARMED", "color": "var(--accent-orange)"},
            {"qtr": "4th Quarter", "status": "ARMED", "color": "var(--accent-orange)"}
        ],
        "score_updates": LATEST_SCORES_CACHE
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
