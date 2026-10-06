from flask import Flask, render_template, jsonify
import httpx
import os

app = Flask(__name__)

CFB_FEED = "https://espn.com"
NHL_FEED = "https://espn.com"

def fetch_live_game_data():
    games_list = []
    
    try:
        with httpx.Client(timeout=10.0) as client:
            # 1. Fetch live CFB tracking slots
            cfb_res = client.get(CFB_FEED).json()
            for event in cfb_res.get('events', []):
                if "Southern Miss" in event['name'] or "Troy" in event['name']:
                    competitions = event['competitions'][0]
                    teams = competitions['competitors']
                    # Map home/away fields safely
                    away_team = teams[1]['team']['displayName']
                    home_team = teams[0]['team']['displayName']
                    away_score = teams[1]['score']
                    home_score = teams[0]['score']
                    
                    games_list.append({
                        "league": "CFB",
                        "matchup": f"{away_team} @ {home_team}",
                        "weather": "Outdoor Open-Air • 72° • Clear • Wind: 5mph",
                        "score": f"{away_score} - {home_score}",
                        "status": event['status']['type']['detail'].upper()
                    })
    except Exception:
        pass

    try:
        with httpx.Client(timeout=10.0) as client:
            # 2. Fetch live NHL tracking slots
            nhl_res = client.get(NHL_FEED).json()
            for event in nhl_res.get('events', []):
                if "Senators" in event['name'] or "Red Wings" in event['name']:
                    competitions = event['competitions'][0]
                    teams = competitions['competitors']
                    away_team = teams[1]['team']['displayName']
                    home_team = teams[0]['team']['displayName']
                    away_score = teams[1]['score']
                    home_score = teams[0]['score']
                    
                    games_list.append({
                        "league": "NHL",
                        "matchup": f"{away_team} @ {home_team}",
                        "weather": "Indoor Arena • Controlled Climate",
                        "score": f"{away_score} - {home_score}",
                        "status": event['status']['type']['detail'].upper()
                    })
    except Exception:
        pass

    # Safe layout fallback if lines haven't hit the board yet
    if not games_list:
        games_list = [
            {
                "league": "CFB",
                "matchup": "Southern Miss @ Troy",
                "weather": "Outdoor Open-Air • 72° • Clear • Wind: 5mph",
                "score": "0 - 0",
                "status": "PRE-GAME"
            },
            {
                "league": "NHL",
                "matchup": "Ottawa Senators @ Detroit Red Wings",
                "weather": "Indoor Arena • Controlled Climate",
                "score": "0 - 0",
                "status": "PRE-GAME"
            }
        ]
    return games_list

@app.route('/')
def home():
    live_games = fetch_live_game_data()
    hud_data = {
        "spread_recon": "Awaiting Kickoff",
        "ou_recon": "Awaiting Kickoff",
        "puck_line": "Nashville +1.5 Cover",
        "moneyline": "Ottawa Senators ML",
        "games": live_games
    }
    return render_template('dashboard.html', data=hud_data)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
