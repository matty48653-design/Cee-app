# app.py
import os
import json
import time
import threading
import urllib.request
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# =====================================================================
# CEE CORE ENGINE SYSTEM MEMORY (No Disk Reads = No More Freezing)
# =====================================================================
SYSTEM_VERSION = "10.0 UNIFIED CORE"
SYSTEM_CACHE = {
    "timestamp": "Initializing...",
    "sharp_sheet": {
        "game_spread_edge": "Scanning...",
        "game_spread_desc": "Engaging live market contrarian data lines.",
        "totals_edge": "Scanning...",
        "totals_desc": "Analyzing public totals money distribution."
    },
    "slates": []
}

def get_espn_json(league_rpc):
    """Secure direct telemetry hook into the public ESPN tracker wire."""
    url = f"https://espn.com{league_rpc}/scoreboard"
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"[CEE Error] Network data obstruction on {league_rpc}: {e}")
        return None

def cee_background_automation_loop():
    """Isolated thread loop updating scores every 60s without disrupting the UI."""
    global SYSTEM_CACHE
    print("CEE Embedded Data Stream Engine Initialized.")
    
    while True:
        current_time_str = time.strftime("%-I:%M %p")
        
        # Fresh baseline frame mirroring your custom analytics requirements
        fresh_data = {
            "timestamp": current_time_str,
            "sharp_sheet": {
                "game_spread_edge": "Fading Public Consensus Bias",
                "game_spread_desc": "Heavy ticket concentrations filtering into house traps; sharp hard money buying the dog trenches.",
                "totals_edge": "Early-Season Total Inflations",
                "totals_desc": "Clock-bleed simulation profiles mapping massive value into overlooked Unders."
            },
            "slates": []
        }

        # 1. PARSE COLLEGE FOOTBALL LIVE TRACKS
        cfb_raw = get_espn_json("football/college-football")
        if cfb_raw and "events" in cfb_raw:
            for event in cfb_raw["events"]:
                short_name = event.get("shortName", "")
                try:
                    comp = event["competitions"][0]
                    status_text = comp["status"]["type"]["detail"]
                    
                    # Safe deep index mapping to extract real team arrays and avoid loops
                    competitors = comp["competitors"]
                    away_score = competitors[1]["score"]
                    home_score = competitors[0]["score"]
                    
                    fresh_data["slates"].append({
                        "league": "CFB",
                        "matchup": short_name,
                        "score": f"{away_score} - {home_score}",
                        "line_label": "Game Status:",
                        "line_value": status_text,
                        "target_label": "CEE Target:",
                        "target_value": "Reverse Line Bait Trap Assessment Active",
                        "kickoff": "Mid-Week Open-Air Trench Warfare Tracker"
                    })
                except Exception:
                    pass

        # 2. PARSE NHL LIVE TRACKS
        nhl_raw = get_espn_json("hockey/nhl")
        if nhl_raw and "events" in nhl_raw:
            for event in nhl_raw["events"]:
                short_name = event.get("shortName", "")
                try:
                    comp = event["competitions"][0]
                    status_text = comp["status"]["type"]["detail"]
                    
                    competitors = comp["competitors"]
                    away_score = competitors[1]["score"]
                    home_score = competitors[0]["score"]
                    
                    fresh_data["slates"].append({
                        "league": "NHL",
                        "matchup": short_name,
                        "score": f"{away_score} - {home_score}",
                        "line_label": "Game Status:",
                        "line_value": status_text,
                        "target_label": "CEE Target:",
                        "target_value": "Goaltending Slider Variance Placement",
                        "kickoff": "Arena Main Track Feed Active"
                    })
                except Exception:
                    pass

        # 3. NFL THURSDAY NIGHT FOOTBALL LANE PRE-SET
        fresh_data["slates"].append({
            "league": "NFL",
            "matchup": "TB @ DAL",
            "score": "0 - 0",
            "line_label": "House Line:",
            "line_value": "Cowboys -3.5",
            "target_label": "CEE Target:",
            "target_value": "Buccaneers +3.5 (Morale Deficit Advantage)",
            "kickoff": "TNF Kickoff: Thursday at 8:15 PM EDT • Roof Closed"
        })

        # Update server memory instantly with zero disk file-locking lag
        SYSTEM_CACHE = fresh_data
        time.sleep(60)

# Start the background data collector loop automatically on boot
threading.Thread(target=cee_background_automation_loop, daemon=True).start()

# =====================================================================
# MASTER WEB UI ROUTING LAYER (Draws your custom layout screen)
# =====================================================================
@app.route('/')
def index():
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
            let cachedTime = "";
            function refreshMatrixData() {
                fetch('/api/live_stream')
                    .then(res => res.json())
                    .then(data => {
                        document.getElementById('live-clock').innerText = "SYS TIME: " + data.timestamp + " // AUTOMATION LIVE";
                        
                        // Safely re-draw elements if fresh score variables change in memory
                        if (cachedTime !== "" && cachedTime !== data.timestamp) {
                            location.reload();
                        }
                        cachedTime = data.timestamp;
                    })
                    .catch(e => console.log("Buffering telemetry pipeline..."));
            }
            // Seamlessly refreshes phone layout elements every 30 seconds
            setInterval(refreshMatrixData, 30000);
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
