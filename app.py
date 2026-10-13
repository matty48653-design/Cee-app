<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CEE SUPREME ACTION MATRIX</title>
    <style>
        :root {
            --bg-base: #0c1117;
            --bg-card: #161b22;
            --border-glow: #21262d;
            --neon-green: #00ffaa;
            --text-main: #c9d1d9;
            --text-dim: #8b949e;
            --alert-orange: #ff9f1c;
            --sky-blue: #58a6ff;
            --light-pink: #ff8ebb;
        }
        body {
            background-color: var(--bg-base);
            color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 12px;
            display: flex;
            justify-content: center;
        }
        .app-container {
            width: 100%;
            max-width: 480px;
        }
        .header-box {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid var(--border-glow);
            padding-bottom: 8px;
            margin-bottom: 16px;
        }
        .title-main {
            font-weight: 800;
            letter-spacing: 1px;
            font-size: 1.1rem;
        }
        .status-sync {
            color: var(--neon-green);
            font-size: 0.75rem;
            border: 1px solid var(--neon-green);
            padding: 2px 6px;
            border-radius: 4px;
        }
        .section-header {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-dim);
            margin: 16px 0 8px 0;
        }
        .card {
            background-color: var(--bg-card);
            border: 1px solid var(--border-glow);
            border-radius: 8px;
            padding: 14px;
            margin-bottom: 12px;
        }
        .automated-sheet {
            border: 1px solid var(--neon-green);
        }
        .card-title {
            font-size: 1.05rem;
            font-weight: bold;
            margin-bottom: 4px;
        }
        .card-subtitle {
            font-size: 0.8rem;
            color: var(--text-dim);
            margin-bottom: 12px;
        }
        .data-row {
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            margin-bottom: 6px;
        }
        .highlight {
            color: var(--alert-orange);
            font-weight: bold;
        }
        .neon-text {
            color: var(--neon-green);
            font-weight: bold;
        }
        .metric-item {
            font-size: 0.85rem;
            margin-top: 8px;
            color: var(--text-main);
            line-height: 1.4;
        }
        .blue-text {
            color: var(--sky-blue);
        }
    </style>
</head>
<body>
    <div class="app-container">
        <div class="header-box">
            <div class="title-main">🟢 CEE SUPREME ACTION MATRIX</div>
            <div class="status-sync">LIVE SYNCING</div>
        </div>

        <!-- ⚡ AUTOMATED COMM SHEET SECTION -->
        <div class="section-header">⚡ LIVE AUTOMATED COMM SHEET</div>
        <div class="card automated-sheet">
            <div class="data-row">
                <span style="font-weight:bold; color:var(--sky-blue);">📌 LIVE SPREAD RECON</span>
                <span class="neon-text">👉 TAKE: Sam Houston Alternate Pass Yards (MORE 175.0 Floor)</span>
            </div>
            <div class="card-subtitle" style="margin-bottom:8px;">Current market context target: Williams Stadium • Line: Liberty -13.5 (O/U 52.5).</div>
            
            <div class="data-row" style="margin-top:12px; border-top:1px solid var(--border-glow); padding-top:8px;">
                <span style="font-weight:bold; color:var(--sky-blue);">📌 LIVE OVER/UNDER RECON</span>
                <span class="neon-text">👉 Analyzing Pacing</span>
            </div>
            <div class="card-subtitle" style="margin-bottom:0;">Will display exact live points threshold targets based on quarter pacing.</div>
        </div>

        <!-- 👁️ SYNDICATE CONSENSUS SECTION -->
        <div class="section-header">👁️ SYNDICATE CONSENSUS & SENTIMENT VOLATILITY</div>
        <div class="card">
            <div class="data-row">
                <div>
                    <div style="font-weight:bold;">Alpha Syndicate</div>
                    <div style="font-size:0.75rem; color:var(--text-dim);">Size: 5x</div>
                </div>
                <div style="text-align:right;">
                    <div class="blue-text" style="font-weight:bold;">Sam Houston Pass Volume Sliders</div>
                    <div style="font-size:0.75rem; color:var(--alert-orange);">94% Public Resistance</div>
                </div>
            </div>
            <div class="data-row" style="margin-top:8px; border-top:1px solid var(--border-glow); padding-top:8px;">
                <div>
                    <div style="font-weight:bold;">Vegas Sharp Box</div>
                    <div style="font-size:0.75rem; color:var(--text-dim);">Size: 2.5x</div>
                </div>
                <div style="text-align:right;">
                    <div class="blue-text" style="font-weight:bold;">NHL Under Adjustments</div>
                    <div style="font-size:0.75rem; color:var(--alert-orange);">74% Public Resistance</div>
                </div>
            </div>
        </div>

        <!-- 📺 LIVE SLATE & ADVANTAGE INSIGHTS SECTION -->
        <div class="section-header">📺 LIVE SLATE & HUMAN ADVANTAGE INSIGHTS</div>
        {% if feeds %}
            {% for game in feeds %}
            <div class="card">
                <div class="data-row" style="margin-bottom:2px;">
                    <span class="card-title">{{ game.sport }} {{ game.matchup }}</span>
                    <span class="neon-text">0 - 0</span>
                </div>
                <div class="card-subtitle">{{ game.venue }} • Line: {{ game.spread_line }} ({{ game.ou_line }}) • <span class="highlight">{{ game.time_label }}</span></div>
                
                <div class="metric-item">🚀 <span class="blue-text" style="font-weight:bold;">TRAVEL TRAJECTORY:</span> {{ game.trajectory }}</div>
                <div class="metric-item">🔊 <span style="color:#ff4444; font-weight:bold;">CROWD ENVIRONMENT:</span> {{ game.crowd_env }}</div>
                <div class="metric-item">⚠️ <span class="highlight">INJURY MATRIX:</span> {{ game.injury_notes }}</div>
                <div class="metric-item">🧠 <span style="color:var(--light-pink); font-weight:bold;">ROSTER MORALE:</span> {{ game.morale_notes }}</div>
            </div>
            {% endfor %}
        {% else %}
            <div class="card">
                <div class="card-subtitle">No Insight Feed Data Live.</div>
            </div>
        {% endif %}

        <!-- 🐋 LIVE AUTOMATED WHALE MOVES -->
        <div class="section-header">🐋 LIVE AUTOMATED WHALE MOVES</div>
        {% if whale_data and whale_data.moves %}
            {% for move in whale_data.moves %}
            <div class="card" style="border-left: 3px solid var(--neon-green);">
                <div class="data-row">
                    <span style="font-weight:bold; color:var(--text-main);">🎯 {{ move.player }} ({{ move.sport }})</span>
                    <span class="neon-text">{{ move.action }}</span>
                </div>
                <div class="card-subtitle" style="margin-top:4px; margin-bottom:4px;">Line Target: {{ move.line }} | Public Resistance: <span class="highlight">{{ move.public_resistance }}</span></div>
                <div style="font-size:0.8rem; color:var(--sky-blue); font-weight:bold; margin-top:6px;">EVAL: {{ move.matrix_evaluation }}</div>
            </div>
            {% endfor %}
        {% else %}
            <div class="card">
                <div class="card-subtitle" style="margin-bottom:0;">No whale movements tracked yet. Submit payload data via your API tool to load instructions.</div>
            </div>
        {% endif %}
    </div>
</body>
</html>
