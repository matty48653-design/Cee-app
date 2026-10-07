from flask import Flask, render_template_string, jsonify
import requests

app = Flask(__name__)

# THE CONTRARIAN EDGE ENGINE (CEE) v5.6 - COMPLETE REBUILD
# Fully overwritten to implement the verified NHL v2 data pipeline.
# Keeps app tracking logic strictly isolated from personal variables.

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CEE Engine HUD</title>
    <style>
        body {
            background-color: #0d0e12;
            color: #e2e8f0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
        }
        .hud-container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .hud-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #1e293b;
            padding-bottom: 15px;
            margin-bottom: 25px;
        }
        .hud-title {
            font-size: 1.8rem;
            font-weight: bold;
            letter-spacing: 1px;
            color: #38bdf8;
        }
        .pipeline-badge {
            background-color: rgba(56, 189, 248, 0.1);
            border: 1px solid #38bdf8;
            color: #38bdf8;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 0.85rem;
            font-weight: bold;
        }
        .grid-layout {
            display: grid;
            grid-template-columns: 1fr;
            gap: 20px;
        }
        @media (min-width: 768px) {
            .grid-layout { grid-template-columns: 1fr 1fr; }
        }
        .card {
            background-color: #151821;
            border: 1px solid #27272a;
            border-radius: 8px;
            padding: 20px;
        }
        .card-header {
            font-size: 1.1rem;
            font-weight: bold;
            color: #ff9100;
            margin-bottom: 15px;
            border-bottom: 1px solid #27272a;
            padding-bottom: 8px;
        }
        .metric-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            font-size: 0.95rem;
        }
        .label { color: #94a3b8; }
        .value { font-weight: 600; }
        .value.highlight { color: #4ade80; }
        .game-box {
            border-left: 3px solid #ff9100;
            background: rgba(255, 145, 0, 0.05);
            padding: 10px;
            margin-top: 10px;
            border-radius: 0 4px 4px 0;
        }
    </style>
    <script>
        // Automatic 10-second polling background routine
        async function fetchLiveScores() {
            try {
                const response = await fetch('/api/live-board');
                const data = await response.json();
                const container = document.getElementById('live-matchups-container');
                container.innerHTML = '';
                
                if (data.games.length === 0) {
                    container.innerHTML = '<div class="metric-row"><span class="label">No live or scheduled games found right now.</span></div>';
                    return;
                }

                data.games.forEach(game => {
                    const div = document.createElement('div');
                    div.className = 'game-box';
                    div.innerHTML = `
                        <div class="metric-row">
                            <span class="value">[${game.league}] ${game.away_team} @ ${game.home_team}</span>
                            <span class="value highlight">${game.away_score} - ${game.home_score}</span>
                        </div>
                        <div class="metric-row" style="font-size: 0.8rem; margin-bottom: 0;">
                            <span class="label">Status: ${game.clock}</span>
                        </div>
                    `;
                    container.appendChild(div);
                });
            } catch (err) {
                console.error("Telemetry update error:", err);
            }
        }
        setInterval(fetchLiveScores, 10000);
        window.onload = fetchLiveScores;
    </script>
</head>
<body>
    <div class="hud-container">
        <div class="hud-header">
            <div class="hud-title">CEE ENGINE HUD</div>
            <div class="pipeline-badge">v5.6 LIVE RECON</div>
        </div>
        
        <div class="grid-layout">
            <!-- STRATEGIC DIRECTIVES PANEL -->
            <div class="card">
                <div class="card-header">STRATEGIC DIRECTIVES CORE</div>
                <div class="metric-row">
                    <span class="label">Target Tracking:</span>
                    <span class="value">Alternate Milestone Sliders Active</span>
                </div>
                <div class="metric-row">
                    <span class="label">Data Filter Matrix:</span>
                    <span class="value">NFL / CFB / NHL Integrated</span>
                </div>
                <div class="metric-row">
                    <span class="label">Excluded Noise:</span>
                    <span class="value">MLB / Fixed House Lines Blocked</span>
                </div>
            </div>

            <!-- LIVE SLATE TRACKER -->
            <div class="card">
                <div class="card-header">LIVE BOARD SCANNER</div>
                <div id="live-matchups-container">
                    <div class="metric-row">
                        <span class="label">Telemetry Feed Status:</span>
                        <span class="value highlight">Connecting Data Pipeline...</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/live-board')
def get_live_board():
    # FIXED: Swapped NHL branch from site.api to endpoints.v2 to capture hockey data correctly
    endpoints = {
        "NFL": "https://espn.com",
        "CFB": "https://espn.com",
        "NHL": "https://espn.com"
    }
    
    parsed_games = []
    
    for league, url in endpoints.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                for event in data.get('events', []):
                    competition = event.get('competitions', [{}])[0]
                    status_type = event.get('status', {}).get('type', {})
                    status = status_type.get('detail', 'Scheduled')
                    
                    competitors = competition.get('competitors', [])
                    home = next((c for c in competitors if c.get('homeAway') == 'home'), {})
                    away = next((c for c in competitors if c.get('homeAway') == 'away'), {})
                    
                    parsed_games.append({
                        "league": league,
                        "home_team": home.get('team', {}).get('shortDisplayName', 'UNK'),
                        "away_team": away.get('team', {}).get('shortDisplayName', 'UNK'),
                        "home_score": home.get('score', '0'),
                        "away_score": away.get('score', '0'),
                        "clock": status
                    })
        except Exception as e:
            continue
            
    return jsonify({"games": parsed_games})

if __name__ == '__main__':
    app.run(debug=True)
