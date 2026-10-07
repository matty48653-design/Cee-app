from flask import Flask, render_template_string, jsonify
import requests

app = Flask(__name__)

# THE CONTRARIAN EDGE ENGINE (CEE) v10.8 - STABLE REAL-TIME MATRIX
# Completely overwrites app.py. Combines raw live scoring structures with market data.
# Defensive error catch blocks guarantee zero server crashes on Render.

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
        .edge-box {
            background: rgba(14, 22, 37, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-left: 3px solid #00e676;
            padding: 12px;
            border-radius: 0 6px 6px 0;
            margin-bottom: 10px;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            margin-top: 8px;
            font-size: 0.75rem;
            background: rgba(255, 255, 255, 0.02);
            padding: 6px;
            border-radius: 4px;
        }
        .metric-item {
            display: flex;
            flex-direction: column;
        }
        .metric-lbl { color: #8c96a3; font-size: 0.68rem; text-transform: uppercase;}
        .metric-val { color: #ffffff; font-weight: 600; margin-top: 2px;}
        .metric-val.edge { color: #00e676; }
        .morale-strip {
            margin-top: 8px;
            padding-top: 6px;
            border-top: 1px dashed rgba(255, 255, 255, 0.05);
            font-size: 0.72rem;
            line-height: 1.3;
        }
    </style>
    <script>
        // On-demand background fetching function loop (Interval: 10 seconds)
        async function fetchActiveMatrixData() {
            try {
                const res = await fetch('/api/active-matrix');
                const data = await res.json();
                const container = document.getElementById('market-edges-dock');
                container.innerHTML = '';
                
                if (!data.games || data.games.length === 0) {
                    container.innerHTML = '<div style="font-size:0.75rem; color:#8c96a3; padding-left:4px; font-style:italic;">No live active network feeds found for this timeframe. Monitoring pipelines...</div>';
                    return;
                }
                
                data.games.forEach(g => {
                    const box = document.createElement('div');
                    box.className = 'edge-box';
                    box.innerHTML = `
                        <div class="row-header">
                            <span style="color:#ffffff; font-size:0.82rem; font-weight:700;">[${g.league}] ${g.away_team} @ ${g.home_team}</span>
                            <span class="value" style="color:#00e676;">${g.away_score} - ${g.home_score}</span>
                        </div>
                        <div style="font-size:0.75rem; color:#66fcf1; margin-top:4px; font-weight:500;">
                            Live Status Clock: ${g.clock}
                        </div>
                        <div class="metrics-grid">
                            <div class="metric-item">
                                <span class="metric-lbl">House O/U Line</span>
                                <span class="metric-val" style="color:#66fcf1;">${g.house_line}</span>
                            </div>
                            <div class="metric-item">
                                <span class="metric-lbl">CEE Net Advantage</span>
                                <span class="metric-val edge">${g.cee_calculated_edge}</span>
                            </div>
                            <div class="metric-item">
                                <span class="metric-lbl">Public Ticket Vol</span>
                                <span class="metric-val" style="color:#e06666;">${g.public_volume}</span>
                            </div>
                            <div class="metric-item">
                                <span class="metric-lbl">Sharp Handle Share</span>
                                <span class="metric-val" style="color:#4ade80;">${g.sharp_money}</span>
                            </div>
                        </div>
                        <div class="morale-strip">
                            <span style="color:#ff4d4d; font-weight:700;">⚠️ INJURY TRACKER:</span> ${g.injury_tracker}<br>
                            <span style="color:#ff9100; font-weight:700;">📉 LOCKER ROOM MORALE:</span> ${g.morale_deficit}
                        </div>
                    `;
                    container.appendChild(box);
                });
            } catch(e) { console.error("Telemetry connection error:", e); }
        }
        setInterval(fetchActiveMatrixData, 10000);
        window.onload = fetchActiveMatrixData;
    </script>
</head>
<body>
    <div class="container">

        <!-- LOGIC HEADER -->
        <div class="header">
            <div class="status-dot"></div>
            <div class="title">CEE SUPREME ACTION MATRIX</div>
        </div>

        <!-- SHARP SELECTION SHEET -->
        <div class="panel sharp">
            <div class="panel-title-row">
                <span class="panel-subtitle">CONTRARIAN LOGIC</span>
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
        </div>

        <!-- STREAMED PANELS TARGET -->
        <div class="section-header">📊 CALCULATED EDGES & REAL-TIME CLOCKS</div>
        <div id="market-edges-dock">
            <div style="font-size:0.75rem; color:#8c96a3; padding-left:4px;">Initializing True Scoring Arrays...</div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(SUPREME_DASHBOARD_HTML)

@app.route('/api/active-matrix')
def get_active_matrix():
    parsed_games = []
    
    # 1. PARSE LIVE GAME CLOCKS AND SCORING SPLITS DIRECT FROM RAW ROOT FEEDS
    score_endpoints = {
        "NFL": "https://espn.com",
        "CFB": "https://espn.com",
        "NHL": "https://espn.com"
    }
    
    live_scores = {}
    for league, url in score_endpoints.items():
        try:
            res = requests.get(url, timeout=4)
            if res.status_code == 200:
                events = res.json().get('events', [])
                for event in events:
                    comp = event.get('competitions', [{}])[0]
                    status_obj = event.get('status', {})
                    
