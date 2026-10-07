# app.py
import os
import json
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)
JSON_CACHE_FILE = "sports_data.json"

def read_local_feed():
    """Reads local data storage instantly with complete crash protection."""
    if os.path.exists(JSON_CACHE_FILE):
        try:
            with open(JSON_CACHE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    # Safety template fallback frame to prevent empty page crashes
    return {
        "timestamp": "12:00 AM",
        "sharp_sheet": {
            "game_spread_edge": "Syncing Data Bridge...",
            "game_spread_desc": "Waiting for feed_bridge.py background boot initialization cycle.",
            "totals_edge": "Syncing System...",
            "totals_desc": "Standby."
        },
        "slates": []
    }

@app.route('/')
def index():
    matrix_data = read_local_feed()
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CEE SUPREME ACTION MATRIX</title>
        <style>
            body { background-color: #05080e; color: #cbd5e1; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 16px; }
            .container { max-width: 480px; margin: 0 auto; }
            .main-header { display: flex; align-items: center; font-size: 15px; font-weight: bold; color: #ffffff; letter-spacing: 0.06em; margin-bottom: 20px; }
            .live-dot { width: 8px; height: 8px; background-color: #10b981; border-radius: 50%; margin-right: 10px; display: inline-block; box-shadow: 0 0 8px #10b981; }
            .sharp-box { border: 1px dashed #14532d; background: #06100a; border-radius: 8px; padding: 14px; margin-bottom: 20px; }
            .sharp-header { display: flex; justify-content: space-between; font-size: 11px; font-weight: bold; margin-bottom: 12px; letter-spacing: 0.05em; }
            .sharp-title { color: #10b981; }
            .sharp-logic { color: #059669; }
            .sheet-row { margin-bottom: 10px; }
            .sheet-label { font-size: 11px; color: #94a3b8; font-weight: 600; text-transform: uppercase; }
            .sheet-value { float: right; font-size: 12px; font-weight: bold; color: #22c55e; }
            .sheet-desc { font-size: 11px; color: #b45309; margin-top: 2px; }
            .section-title { font-size: 11px; font-weight: bold; color: #94a3b8; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 12px; }
            .game-card { background: #09111e; border-left: 3px solid #ea580c; border-radius: 0 6px 6px 0; padding: 12px; margin-bottom: 12px; }
            .card-top { display: flex; justify-content: space-between; font-weight: bold; font-size: 13px; margin-bottom: 8px; }
            .matchup-text { color: #f8fafc; }
            .live-score { color: #10b981; font-family: monospace; }
            .data-grid { font-size: 11px; line-height: 1.5; margin-bottom: 6px; }
            .data-row { display: flex; margin-bottom: 2px; }
            .lbl { color: #94a3b8; width: 85px; }
            .val-house { color: #cbd5e1; }
            .val-cee { color: #22c55e; font-weight: 600; }
            .kickoff-text { font-size: 10px; color: #ea580c; }
            .telemetry-footer { text-align: center; font-size: 10px; color: #475569; margin-top: 20px; font-family: monospace; }
        </style>
        <script>
            function autoUpdateScreen() {
                fetch('/api/live_stream')
                    .then(response => {
                        if (!response.ok) throw new Error();
                        return response.json();
                    })
                    .then(data => {
                        // Smoothly streams clock and matrix validation state changes without full page flickering
                        document.getElementById('live-clock').innerText = "SYS TIME: " + data.timestamp + " // MATRIX LIVE";
                        
                        // Forces page reload only if a live scoring data shift occurs
                        if(document.body.innerText.includes("Syncing Data Bridge...")) {
                            location.reload();
                        }
                    })
                    .catch(err => console.log("CEE Core Buffer Stream Syncing..."));
            }
            // Background thread updates your device every 30 seconds smoothly
            setInterval(autoUpdateScreen, 30000);
        </script>
    </head>
    <body>
        <div class="container">
            <div class="main-header"><span class="live-dot"></span> CEE SUPREME ACTION MATRIX</div>
            
            <div class="sharp-box">
                <div class="sharp-header">
                    <div class="sharp-title">🎯 SHARP SELECTION SHEET</div>
                    <div class="sharp-logic">CONTRARIAN LOGIC</div>
                </div>
                <div class="sheet-row">
                    <div><span class="sheet-label">Game Spread Edge</span><span class="sheet-value">{{ data.sharp_sheet.game_spread_edge }}</span></div>
                    <div class="sheet-desc">{{ data.sharp_sheet.game_spread_desc }}</div>
                </div>
                <div class="sheet-row" style="margin-bottom: 0;">
                    <div><span class="sheet-label">Totals Over/Under</span><span class="sheet-value">{{ data.sharp_sheet.totals_edge }}</span></div>
                    <div class="sheet-desc">{{ data.sharp_sheet.totals_desc }}</div>
                </div>
            </div>

            <div class="section-title">📺 UPCOMING SLATES & CEE MARGIN EDGES</div>

            {% for game in data.slates %}
            <div class="game-card">
                <div class="card-top">
                    <span class="matchup-text">[{{ game.league }}] {{ game.matchup }}</span>
                    <span class="live-score">{{ game.score }}</span>
                </div>
                <div class="data-grid">
                    <div class="data-row">
                        <span class="lbl">{{ game.line_label }}</span>
                        <span class="val-house">{{ game.line_value }}</span>
                    </div>
                    <div class="data-row">
                        <span class="lbl">{{ game.target_label }}</span>
                        <span class="val-cee">{{ game.target_value }}</span>
                    </div>
                </div>
                <div class="kickoff-text">{{ game.kickoff }}</div>
            </div>
            {% endfor %}

            <div class="telemetry-footer" id="live-clock">SYS TIME: {{ data.timestamp }} // LOC: Arcadia, FL</div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template, data=matrix_data)

@app.route('/api/live_stream')
def live_stream():
    return jsonify(read_local_feed())

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
