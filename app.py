import os
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# Restored: Your premium v7.0 design with the built-in auto-refresh heartbeat pulse timer
V7_HUD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cee App - CEE ENGINE HUD</title>
    <style>
        body { background-color: #050811; color: #e2e8f0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 14px; -webkit-font-smoothing: antialiased; }
        #matrix-container { max-width: 480px; margin: 0 auto; }
        .hud-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; }
        .hud-title { font-size: 1.4rem; font-weight: 800; color: #ffffff; letter-spacing: 0.02em; }
        .pipeline-badge { background: rgba(0, 230, 118, 0.1); border: 1px solid #00e676; color: #00e676; font-size: 0.75rem; font-weight: 800; padding: 4px 8px; border-radius: 4px; text-transform: uppercase; }
        .last-checked { color: #475569; font-size: 0.75rem; text-align: right; margin-bottom: 20px; }
        .action-card { background: #090f1d; border: 1px solid rgba(0, 230, 118, 0.3); border-radius: 12px; padding: 16px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0, 230, 118, 0.05); }
        .action-header-row { display: flex; justify-content: space-between; align-items: flex-start; gap: 10px; margin-bottom: 12px; }
        .action-directive { font-size: 1.05rem; font-weight: 800; color: #ffffff; line-height: 1.3; }
        .strike-badge { background: rgba(0, 230, 118, 0.1); color: #00e676; font-size: 0.7rem; font-weight: 900; padding: 4px 6px; border-radius: 4px; text-align: center; line-height: 1.2; min-width: 65px; }
        .action-instructions { color: #94a3b8; font-size: 0.85rem; line-height: 1.4; }
        .section-label { color: #64748b; font-size: 0.8rem; font-weight: 800; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 14px; display: flex; align-items: center; gap: 6px; }
        .slate-card { background: #0c1222; border-radius: 10px; padding: 14px; margin-bottom: 10px; border: 1px solid #16203b; }
        .game-row { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px; }
        .game-name-text { font-size: 1.05rem; font-weight: 700; color: #ffffff; }
        .score-box { text-align: right; }
        .score-text { font-size: 1.1rem; font-weight: 800; color: #00e676; }
        .status-text { font-size: 0.7rem; font-weight: 800; color: #ff9100; letter-spacing: 0.02em; margin-top: 2px; }
        .env-text { color: #64748b; font-size: 0.75rem; font-weight: 500; }
        .panel-box { background: #090f1d; border: 1px solid #16203b; border-radius: 10px; padding: 14px; margin-bottom: 16px; }
        .split-row { display: flex; justify-content: space-between; padding: 8px 0; font-size: 0.9rem; border-bottom: 1px solid #16203b; }
        .split-label { font-weight: 700; color: #ffffff; }
        .split-value { font-weight: 700; color: #ff9100; }
        .param-row { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; }
        .param-player { font-size: 0.95rem; font-weight: 700; color: #ffffff; }
        .param-milestone { background: rgba(255, 145, 0, 0.1); color: #ff9100; font-size: 0.75rem; font-weight: 800; padding: 4px 8px; border-radius: 4px; }
        .param-pct { color: #00e676; font-weight: 800; font-size: 1rem; }
    </style>
</head>
<body>
<div id="matrix-container">
    <div class="hud-header">
        <div class="hud-title">CEE ENGINE HUD</div>
        <div class="pipeline-badge">Pipeline Active v7.0</div>
    </div>
    <div class="last-checked" id="time-counter">Last Checked: Just Now</div>

    <div class="action-card">
        <div class="action-header-row">
            <div class="action-directive">👉 TARGET: Southern Miss +10.5 (CFB) & Nashville ML +130 (NHL)</div>
            <div class="strike-badge" style="border: 1px solid #00e676;">READY TO STRIKE</div>
        </div>
        <div class="action-instructions">
            <strong>Instructions:</strong> Erase standard house totals. Pull custom sliders to focus entirely on alternate passing volume cushions or flat contrarian moneylines.
        </div>
    </div>

    <div class="section-label">🎯 SYNDICATE CONSENSUS & SENTIMENT VOLATILITY</div>
    <div class="panel-box" style="margin-bottom: 20px;">
        <div class="split-row">
            <div><div class="split-label">Alpha Syndicate</div><div style="color:#475569; font-size:0.75rem; font-weight:bold; margin-top:2px;">Size: 5x</div></div>
            <div style="text-align:right;"><div style="font-weight:700; color:#38bdf8;">Southern Miss +10.5</div><div class="split-value" style="font-size:0.75rem; margin-top:2px;">94% Public Resistance</div></div>
        </div>
        <div class="split-row">
            <div><div class="split-label">Wallet #4092 (High-Stakes)</div><div style="color:#475569; font-size:0.75rem; font-weight:bold; margin-top:2px;">Size: 3.5x</div></div>
            <div style="text-align:right;"><div style="font-weight:700; color:#38bdf8;">Nashville ML (+130)</div><div class="split-value" style="font-size:0.75rem; margin-top:2px;">87% Public Resistance</div></div>
        </div>
        <div class="split-row" style="border-bottom:none;">
            <div><div class="split-label">Vegas Sharp Box</div><div style="color:#475569; font-size:0.75rem; font-weight:bold; margin-top:2px;">Size: 2x</div></div>
            <div style="text-align:right;"><div style="font-weight:700; color:#38bdf8;">Ottawa ML (+115)</div><div class="split-value" style="font-size:0.75rem; margin-top:2px;">69% Public Resistance</div></div>
        </div>
    </div>

    <div class="section-label">📺 LIVE SLATE & STADIUM WEATHER MONITOR</div>
    <div style="margin-bottom: 20px;" id="live-matchups-grid">
        <div class="slate-card">
            <div class="game-row">
                <div><span style="color:#64748b; font-size:0.65rem; font-weight:900; letter-spacing:0.04em; margin-right:4px;">CFB</span><span class="game-name-text">Southern Miss @ Troy</span></div>
                <div class="score-box"><div class="score-text">17 - 24</div><div class="status-text">FINAL</div></div>
            </div>
            <div class="env-text">Outdoor Open-Air · 72° · Clear · Wind: 5mph · DraftKings Live Sync Active 🌐</div>
        </div>
        <div class="slate-card">
            <div class="game-row">
                <div><span style="color:#64748b; font-size:0.65rem; font-weight:900; letter-spacing:0.04em; margin-right:4px;">NHL</span><span class="game-name-text">Ottawa Senators @ Detroit Red Wings</span></div>
                <div class="score-box"><div class="score-text">3 - 2</div><div class="status-text">FINAL</div></div>
            </div>
            <div class="env-text">Indoor Arena · Indoor · Climate Controlled · DraftKings Live Sync Active 🌐</div>
        </div>
        <div class="slate-card">
            <div class="game-row">
                <div><span style="color:#64748b; font-size:0.65rem; font-weight:900; letter-spacing:0.04em; margin-right:4px;">NHL</span><span class="game-name-text">Nashville Predators @ Toronto Maple Leafs</span></div>
                <div class="score-box"><div class="score-text">1 - 3</div><div class="status-text">FINAL</div></div>
            </div>
            <div class="env-text">Indoor Arena · Indoor · Climate Controlled · Position Secured 🟩</div>
        </div>
        <div class="slate-card">
            <div class="game-row">
                <div><span style="color:#64748b; font-size:0.65rem; font-weight:900; letter-spacing:0.04em; margin-right:4px;">NHL</span><span class="game-name-text">Vegas Golden Knights @ Seattle Kraken</span></div>
                <div class="score-box"><div class="score-text">2 - 1</div><div class="status-text">FINAL</div></div>
            </div>
            <div class="env-text">Indoor Arena · Indoor · Climate Controlled · DraftKings Live Sync Active 🌐</div>
        </div>
    </div>

    <div class="section-label">🏈 CFB GAME SCRIPT PARAMETERS</div>
    <div class="panel-box">
        <div class="param-row" style="border-bottom: 1px solid #16203b; padding-bottom: 10px;">
            <div class="param-player">Landry Lyddy (USM)</div>
            <div class="param-milestone">OVER 13.5 Completions</div>
            <div class="param-pct">77%</div>
        </div>
        <div class="param-row" style="padding-top: 10px;">
            <div class="param-player">Jaheim Merriweather (RB)</div>
            <div class="param-milestone">OVER 39.5 Rush Yards</div>
            <div class="param-pct">81%</div>
        </div>
    </div>
</div>

<!-- RESTORED: THE 4:00 PM AUTOMATIC REFRESH HEARTBEAT TWEAK -->
<script>
    function runAutoRefreshLoop() {
        fetch(window.location.href)
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                
                // Native updates the scoreboard grid container automatically
                const newGrid = doc.getElementById('live-matchups-grid');
                const oldGrid = document.getElementById('live-matchups-grid');
                if (newGrid && oldGrid) {
                    oldGrid.innerHTML = newGrid.innerHTML;
                }
                
                // Updates the timestamp signature block
                const now = new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', second: '2-digit' });
                document.getElementById('time-counter').innerText = 'Last Checked: ' + now;
            })
            .catch(err => console.log("Feed buffering..."));
    }
