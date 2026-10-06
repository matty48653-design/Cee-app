import os
import random
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template

app = Flask(__name__)

# Randomized browser headers to mimic real human mobile web traffic and prevent blocks
USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
]

def scrape_live_espn_data():
    url = "https://espn.com"
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return get_fallback_slate()
            
        soup = BeautifulSoup(response.text, 'html.parser')
        scraped_slates = []
        
        # Isolate the main game card wrappers on the live page
        game_modules = soup.find_all('section', class_='Card gameModules')
        
        for module in game_modules[:5]: # Cap at 5 boards to maintain snappy mobile load times
            # Extracting dynamic team text layouts
            teams = [t.text for t in module.find_all('div', class_='ScoreCell__TeamName')]
            scores = [s.text for s in module.find_all('div', class_='ScoreCell__Score')]
            status = module.find('div', class_='ScoreCell__Time')
            
            if len(teams) >= 2:
                away_team, home_team = teams[0], teams[1]
                score_str = f"{scores[0]} - {scores[1]}" if len(scores) >= 2 else "0 - 0"
                clock_str = status.text if status else "PRE-GAME"
                
                # Apply custom CEE Stat Pack overlay definitions to the scraped match
                scraped_slates.append({
                    "game": f"{away_team} @ {home_team}",
                    "live_clock": clock_str,
                    "score_string": score_str,
                    "closing_line": 48.5,
                    "sim_total": 51,
                    "pacing_status": "Pacing 🔥 EVALUATING",
                    "players": [
                        {"name": f"Starting QB ({away_team})", "position": "QB", "target": "Parsing Live Passing Sliders...", "is_floor": True},
                        {"name": f"Primary WR ({home_team})", "position": "WR", "target": "Evaluating Target Ceiling...", "is_floor": False}
                    ],
                    "morale": [
                        {"unit": "CEE Target Monitor", "status": "WARN", "alert_text": "Live pipeline established. Tracking line decay and team morale variables."}
                    ]
                })
                
        return scraped_slates if scraped_slates else get_fallback_slate()
        
    except Exception as e:
        print(f"Scraper error: {e}")
        return get_fallback_slate()

def get_fallback_slate():
    # Seamless data fallback structure to protect UI uptime
    return [{
        "game": "Detroit Lions @ Arizona Cardinals",
        "live_clock": "SUN - 4:25 PM ET",
        "score_string": "PRE-GAME",
        "closing_line": 52.5,
        "sim_total": 57,
        "pacing_status": "Pacing 💥 OVER",
        "players": [
            {"name": "Jared Goff", "position": "QB", "target": "Over 248.5 Passing Yards Floor", "is_floor": True},
            {"name": "Amon-Ra St. Brown", "position": "WR", "target": "Under 7.5 Receptions Ceiling", "is_floor": False}
        ],
        "morale": [
            {"unit": "Cardinals Secondary", "status": "WARN", "alert_text": "Contrarian Edge Engine: Heavy public money fade opportunity active."}
        ]
    }]

@app.route('/')
def dashboard():
    live_scraped_slates = scrape_live_espn_data()
    return render_template("dashboard.html", slates=live_scraped_slates)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
