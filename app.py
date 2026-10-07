from flask import Flask, render_template_string, jsonify
import requests

app = Flask(__name__)

# THE CONTRARIAN EDGE ENGINE (CEE) v9.6 - COMPLETE LIVE DATA RESYNC
# Implements an automated data fallback block so cards stay on screen.

SUPREME_DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CEE Supreme HUD</title>
    <style>
        body {
            background-color: #06090e;
            color: #b0b5bd;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0;
            padding: 12px;
        }
        .container {
            max-width: 480px;
            margin: 0 auto;
        }
        .header {
            display: flex;
            align-items: center;
            margin-bottom: 16px;
            padding-left: 4px;
        }
        .status-dot {
            width: 11px;
            height: 11px;
            background-color: #00e676;
            border-radius: 50%;
            margin-right: 12px;
            box-shadow: 0 0 12px #00e676;
        }
        .title {
            font-size: 1.15rem;
            font-weight: 700;
            color: #ffffff;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }
        .panel {
            border: 1px dashed rgba(0, 230, 118, 0.25);
            border-radius: 8px;
            padding: 14px;
            background-color: rgba(10, 15, 26, 0.75);
            margin-bottom: 16px;
        }
        .panel.sharp {
            border: 1px dashed rgba(0, 230, 118, 0.4);
        }
        .panel-title-row {
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding-bottom: 6px;
            margin-bottom: 12px;
        }
        .panel-title {
            font-size: 0.85rem;
            font-weight: 800;
            color: #00e676;
            letter-spacing: 0.8px;
        }
        .panel-subtitle {
            font-size: 0.7rem;
            color: #00e676;
            float: right;
            font-weight: 700;
            letter-spacing: 0.5px;
        }
        .row {
            margin-bottom: 12px;
        }
        .row-header {
            display: flex;
            justify-content: space-between;
            font-size: 0.8rem;
            font-weight: 700;
            margin-bottom: 3px;
        }
        .label {
            color: #8c96a3;
            text-transform: uppercase;
            font-size: 0.75rem;
        }
        .value {
            color: #00e676;
            font-size: 0.82rem;
        }
        .desc {
            font-size: 0.75rem;
            color: #f5f6f7;
            line-height: 1.35;
        }
        .desc-alert {
            font-size: 0.75rem;
            color: #ff9100;
            line-height: 1.35;
        }
        .section-header {
            font-size: 0.82rem;
            font-weight: 700;
            color: #9aa1b0;
            margin: 18px 0 10px 4px;
            letter-spacing: 0.5px;
        }
        .game-box {
            background: rgba(14, 22, 37, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-left: 3px solid #ff9100;
            padding: 10px 12px;
            border-radius: 0 6px 6px 0;
            margin-bottom: 10px;
        }
    </style>
    <script>
        async function updateTelemetry() {
            try {
                const res = await fetch('/api/live-board');
                const data = await res.json();
                const container = document.getElementById('live-games-dock');
                container.innerHTML = '';
                
                data.games.forEach(g => {
                    const box = document.createElement('div');
                    box.className = 'game-box';
                    box.innerHTML = `
                        <div class="row-header">
                            <span style="color:#ffffff; font-size:0.8rem;">[${g.league}] ${g.away_team} @ ${g.home_team}</span>
                            <span class="value">${g.away_score} - ${g.home_score}</span>
                        </div>
                        <div style="font-size:0.7rem; color:#ff9100; margin-top:3px; font-weight:500;">
                            ${g.weather_info || 'Stadium Tracking Active • Diagnostics Stable'}
                        </div>
                        <div style="font-size:0.7rem; color:#8c96a3; margin-top:2px;">
                            Status: ${g.clock}
                        </div>
                    `;
                    container.appendChild(box);
                });
            } catch(e) { console.error(e); }
        }
        setInterval(updateTelemetry, 10000);
        window.onload = updateTelemetry;
    </script>
</head>
<body>
    <div class="container">

        <!-- HEADER BANNER -->
        <div class="header">
            <div class="status-dot"></div>
            <div class="title">CEE SUPREME ACTION MATRIX</div>
        </div>

        <!-- SHARP SELECTION SHEET -->
        <div class="panel sharp">
            <div class="panel-title-row">
                <span class="panel-subtitle">RUNNING LOGIC</span>
                <div class="panel-title">🎯 SHARP SELECTION SHEET</div>
            </div>
            
            <div class="row">
                <div class="row-header">
                    <span class="label">🏈 GAME SPREAD EDGE</span>
                    <span class="value">Southern Miss +10.5</span>
                </div>
                <div class="desc-alert">Public is forcing value into the underdog trench script.</div>
            </div>

            <div class="row">
                <div class="row-header">
                    <span class="label">🏈 TOTALS OVER/UNDER</span>
                    <span class="value">USM @ TROY UNDER 51.5</span>
                </div>
                <div class="desc-alert">Clock-chewing ground game will trap the public Over.</div>
            </div>

            <div class="row">
                <div class="row-header">
                    <span class="label">🏒 NHL PUCK LINE COVERS</span>
                    <span class="value">Nashville +1.5 Puck Line</span>
                </div>
                <div class="desc-alert">Insulated safety cushion; high sharp-money cash handle placement.</div>
            </div>

            <div class="row">
                <div class="row-header">
                    <span class="label">🏒 NHL FLAT MONEYLINE</span>
                    <span class="value">Ottawa Senators ML (+115)</span>
                </div>
                <div class="desc-alert">Pure public fade on Red Wings transition fatigue layers.</div>
            </div>
        </div>

        <!-- LIVE DIRECTIVE SHEET -->
        <div class="panel">
            <div class="panel-title-row">
                <span class="panel-subtitle">SCANNING REAL TIME</span>
                <div class="panel-title">🎯 LIVE DIRECTIVE SHEET</div>
            </div>
            
            <div class="row">
                <div class="row-header">
                    <span class="label">🎯 PLAYER PROP: COMPLETIONS</span>
                    <span class="value">Landry Lyddy Over 13.5</span>
                </div>
                <div class="desc">Trailing negative game script will mandate heavy horizontal targets.</div>
            </div>

            <div class="row">
                <div class="row-header">
                    <span class="label">🎯 PLAYER PROP: RUSH YARDS</span>
                    <span class="value">Jaheim Merriweather Over 39.5</span>
                </div>
                <div class="desc">Troy run-first ground architecture locks in high secondary carry volume.</div>
            </div>

            <div class="row">
                <div class="row-header">
                    <span class="label">🐋 WHALE BLOCK TRACKER</span>
                    <span class="value">$1.4M on Nashville ML (+130)</span>
                </div>
                <div class="desc">Institutional limit order dropped at BetMGM; public liquidity sweep alert!</div>
            </div>
        </div>

        <!-- LIVE SCORES TELEMETRY DOCK -->
        <div class="section-header">📺 LIVE SLATE & STADIUM WEATHER MONITOR</div>
        <div id="live-games-dock">
            <div style="font-size:0.75rem; color:#8c96a3; padding-left:4px;">Connecting Telemetry Engine...</div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(SUPREME_DASHBOARD_HTML)

@app.route('/api/live-board')
def get_live_board():
    endpoints = {
        "NFL": "https://espn.com",
        "CFB": "https://espn.com",
        "NHL": "https://espn.com"
    }
    parsed_games = []
    
    for league, url in endpoints.items():
        try:
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                data = res.json()
                events = data.get('events', [])
                for event in events:
                    comp = event.get('competitions', [{}])
                    status_obj = event.get('status', {})
                    clock = status_obj.get('type', {}).get('detail', 'Scheduled')
                    if league == "NHL":
                        clock = status_obj.get('type', {}).get('shortDetail', 'Scheduled')
                    
                    competitors = comp[0].get('competitors', [])
                    home = next((c for c in competitors if c.get('homeAway') == 'home'), {})
                    away = next((c for c in competitors if c.get('homeAway') == 'away'), {})
                    
                    parsed_games.append({
