import os
import requests
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# BULLETPROOF SYNTAX SHELL: HOUSES YOUR ENTIRE V7.0 DARK HUD THEME NATIVELY
V7_HUD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cee App - CEE MASTER HUD CENTER</title>
    <style>
        body {
            background-color: #050811;
            color: #e2e8f0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0;
            padding: 14px;
            -webkit-font-smoothing: antialiased;
        }
        
        #matrix-container {
            max-width: 480px;
            margin: 0 auto;
        }

        .hud-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 4px;
        }

        .hud-title {
            font-size: 1.4rem;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: 0.02em;
        }

        .pipeline-badge {
            background: rgba(0, 230, 118, 0.1);
            border: 1px solid #00e676;
            color: #00e676;
            font-size: 0.75rem;
            font-weight: 800;
            padding: 4px 8px;
            border-radius: 4px;
            text-transform: uppercase;
        }

        .last-checked {
            color: #475569;
            font-size: 0.75rem;
            text-align: right;
            margin-bottom: 20px;
        }

        .action-card {
            background: #090f1d;
            border: 1px solid rgba(0, 230, 118, 0.3);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(0, 230, 118, 0.05);
        }

        .action-header-row {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 10px;
            margin-bottom: 12px;
        }

        .action-directive {
            font-size: 1.05rem;
            font-weight: 800;
            color: #ffffff;
            line-height: 1.3;
        }

        .strike-badge {
            background: rgba(0, 230, 118, 0.1);
            color: #00e676;
            font-size: 0.7rem;
            font-weight: 900;
            padding: 4px 6px;
            border-radius: 4px;
            text-align: center;
            line-height: 1.2;
            min-width: 65px;
        }

        .action-instructions {
            color: #94a3b8;
            font-size: 0.85rem;
            line-height: 1.4;
        }

        .section-label {
            color: #64748b;
            font-size: 0.8rem;
            font-weight: 800;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .panel-box {
            background: #090f1d;
            border: 1px solid #16203b;
            border-radius: 10px;
            padding: 14px;
            margin-bottom: 16px;
        }

        .split-row {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            font-size: 0.9rem;
            border-bottom: 1px solid #16203b;
        }

        .split-label { font-weight: 700; color: #ffffff; }
        .split-value { font-weight: 700; color: #ff9100; }

        .slate-card {
            background: #0c1222;
            border-radius: 12px;
            padding: 14px;
            margin-bottom: 12px;
            border: 1px solid #1a2640;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        }

        .edge-rating-tag {
            font-size: 0.7rem;
            font-weight: 900;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            margin-bottom: 8px;
            display: inline-block;
            padding: 2px 6px;
            border-radius: 4px;
            background: rgba(255, 255, 255, 0.03);
        }

        .game-title-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }

        .game-title {
            font-size: 1.25rem;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: -0.01em;
        }

        .live-clock-badge {
            background: #ff4d4d;
            color: #ffffff;
            font-size: 0.65rem;
            font-weight: 800;
            padding: 2px 6px;
            border-radius: 4px;
            text-transform: uppercase;
        }

        .line-module-row {
            display: grid;
            grid-template-columns: 80px 1fr;
            background: #060914;
            border: 1px solid #141d30;
            border-radius: 6px;
            margin-bottom: 6px;
            overflow: hidden;
            font-size: 0.8rem;
        }

        .module-label {
            background: #101726;
            color: #64748b;
            font-weight: 800;
            font-size: 0.65rem;
            display: flex;
            align-items: center;
            justify-content: center;
            text-transform: uppercase;
            border-right: 1px solid #141d30;
        }

        .module-value { padding: 10px 12px; font-weight: 700; color: #ffffff; }

        .table-header {
            display: flex;
            justify-content: space-between;
            color: #475569;
            font-size: 0.65rem;
            font-weight: 800;
            text-transform: uppercase;
            padding-bottom: 6px;
            border-bottom: 1px solid #1a2640;
            margin-bottom: 6px;
        }

        .prop-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #0f182b;
        }
        .prop-player { font-size: 0.9rem; font-weight: 700; color: #ffffff; }
        .prop-line { font-size: 0.85rem; font-weight: 700; color: #ffeb3b; }
        .prop-pct { color: #00e676; font-weight: 800; font-size: 0.95rem; text-align: right; }
    </style>
</head>
<body>

<div id="matrix-container">

    <!-- CEE MAIN HUD PANEL -->
    <div class="hud-header">
        <div class="hud-title">CEE ENGINE HUD</div>
        <div class="pipeline-badge">v7.0 PERSONAL SYNC ACTIVE 🌐</div>
    </div>
    <div class="last-checked" id="time-counter">Last Checked: Connecting Data Feed...</div>

    <!-- STRATEGIC ACTION TARGET DIRECTIVES PANEL -->
    <div class="action-card">
        <div class="action-header-row">
            <div class="action-directive">👉 TARGET LOCK: Southern Miss +10.5 (CFB) & Nashville ML +130 (NHL)</div>
            <div class="strike-badge" style="border: 1px solid #00e676; background: rgba(0, 230, 118, 0.05);">STRIKE</div>
        </div>
        <div class="action-instructions">
            <strong>Instructions:</strong> Erase standard house totals. Pull custom sliders to focus entirely on alternate passing volume cushions or flat contrarian moneylines.
        </div>
    </div>

    <!-- PERSONALIZED SYNDICATE AND WATCHLIST PANEL -->
    <div class="section-label">🎯 PERSONALIZED WHALE CONSENSUS & WATCHLIST</div>
    <div class="panel-box" style="margin-bottom: 20px;">
        <div class="split-row">
            <div><div class="split-label">🦁 Detroit Lions Tracking Array</div><div style="color:#475569; font-size:0.75rem; font-weight:bold; margin-top:2px;">Status: Priority Team</div></div>
            <div style="text-align:right;"><div style="font-weight:700; color:#38bdf8;">Alternate Sliders Active</div><div style="font-weight:700; color:#ff9100; font-size:0.75rem; margin-top:2px;">Fading Public Line Bias</div></div>
        </div>
        <div class="split-row">
            <div><div class="split-label">Alpha Syndicate Position</div><div style="color:#475569; font-size:0.75rem; font-weight:bold; margin-top:2px;">Size: 5x</div></div>
            <div style="text-align:right;"><div style="font-weight:700; color:#38bdf8;">Southern Miss +10.5</div><div style="font-weight:700; color:#ff9100; font-size:0.75rem; margin-top:2px;">94% Public Resistance</div></div>
        </div>
        <div class="split-row" style="border-bottom:none;">
            <div><div class="split-label">Wallet #4092 (High-Stakes)</div><div style="color:#475569; font-size:0.75rem; font-weight:bold; margin-top:2px;">Size: 3.5x</div></div>
            <div style="text-align:right;"><div style="font-weight:700; color:#38bdf8;">Nashville ML (+130)</div><div style="font-weight:700; color:#ff9100; font-size:0.75rem; margin-top:2px;">87% Public Exposure</div></div>
        </div>
    </div>

    <!-- FULL BOARD SCANNER AND DIRECT WEBPACK LOOPS GRID -->
    <div class="section-label">📺 LIVE BOARD SCANNER MONITOR & RECON DATA GRID</div>
    <div style="margin-bottom: 20px;" id="live-matchups-container">
        
        <!-- COLLEGE FOOTBALL ACTIVE CONTAINER DOCK -->
        <div class="slate-card">
            <div class="edge-rating-tag" style="border: 1px solid #ffeb3b; color: #ffeb3b;">SHARP VALUE WINDOW 🥈</div>
            <div class="game-title-row">
                <div class="game-title">Southern Miss @ Troy</div>
                <div class="live-clock-badge" id="cfb-clock">7:30 PM ET</div>
            </div>
            <div class="line-module-row"><div class="module-label" style="color: #ff4d4d;">SCORE</div><div class="module-value" id="cfb-score" style="color: #00e676;">0 - 0</div></div>
            <div class="line-module-row"><div class="module-label" style="color: #ffeb3b;">TOTALS</div><div class="module-value" style="color: #ffeb3b;">Pacing UNDER (Closing Line: 51.5 ▼)</div></div>
