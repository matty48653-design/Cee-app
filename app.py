from flask import Flask, render_template, jsonify
import httpx
import os

app = Flask(__name__)

# Core source endpoints matching our v9.2 feed filters
CFB_FEED = "https://espn.com"
NHL_FEED = "https://espn.com"

def fetch_live_game_data():
    games_list = []
    
    with httpx.Client(timeout=10.0) as client:
        # 1. Gather live College Football board parameters
        try:
            cfb_res = client.get(CFB_FEED).json()
            for event in cfb_res.get('events', []):
                # Target the matching matchup constraint
                if "Southern Miss" in event['name'] or "Troy" in event['name']:
                    competitor = event['competitions'][0]
                    home = competitor['competitors'][0]
                    away = competitor['competitors'][1]
                    games_list.append({
                        "league": "CFB",
                        "matchup": f"{away['team']['displayName']} @ {home['team']['displayName']}",
                        "weather": competitor.get('venue', {}).get('address', {}).get('city', 'Outdoor Stadium') + " • Climate Preserved",
                        "score": f"{away['score']} - {home['score']}",
                        "status": event['status']['type']['detail'].upper()
                    })
        except Exception:
            pass

        # 2. Gather live NHL board parameters
        try:
            nhl_res = client.get(NHL_FEED).json()
            for event in nhl_res.get('events', []):
                # Target the matching matchup constraint
                if "Senators" in event['name'] or "Red Wings" in event['name']:
                    competitor = event['competitions'][0]
                    home = competitor['competitors'][0]
                    away = competitor['competitors'][1]
                    games_list.append({
                        "league": "NHL",
                        "matchup": f"{away['team']['displayName']} @ {home['team']['displayName']}",
                        "weather": "Indoor Arena • Controlled Climate",
                        "score": f"{away['score']} - {home['score']}",
                        "status": event['status']['type']['detail'].upper()
                    })
        except Exception:
            pass

    # Fallback to display the baseline slots if feeds are empty or matching targets haven't hit the board yet
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
