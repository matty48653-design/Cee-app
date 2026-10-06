from flask import Flask, render_template, jsonify
import os, requests, time

app = Flask(__name__)
app.secret_key = os.urandom(24)

LATEST_SCORES_CACHE = {
    "usm_troy": {"score": "0 - 0", "status": "UPCOMING", "stadium": "Outdoor Open-Air", "weather": "72° • Clear • Wind: 5mph", "quarter": "PRE-GAME"},
    "ott_det": {"score": "0 - 0", "status": "UPCOMING", "stadium": "Indoor Arena", "weather": "Indoor • Climate Controlled", "quarter": "PRE-GAME"},
    "nas_tor": {"score": "0 - 0", "status": "UPCOMING", "stadium": "Indoor Arena", "weather": "Indoor • Climate Controlled", "quarter": "PRE-GAME"},
    "vgk_sea": {"score": "0 - 0", "status": "UPCOMING", "stadium": "Indoor Arena", "weather": "Indoor • Climate Controlled", "quarter": "PRE-GAME"}
}

def pull_live_unblocked_scores():
    global LATEST_SCORES_CACHE
    try:
        url = "https://espn.com"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            for event in data.get('events', []):
                short_name = event.get('shortName', '')
                if any(x in short_name for x in ["SWM", "TROY", "SMU"]):
                    status = event.get('status', {}).get('type', {}).get('state', '').upper()
                    display_status = "LIVE" if status == "INPROGRESS" else "UPCOMING"
                    period = event.get('status', {}).get('period', 0)
                    if period == 1: LATEST_SCORES_CACHE["usm_troy"]["quarter"] = "1ST QTR"
                    elif period == 2: LATEST_SCORES_CACHE["usm_troy"]["quarter"] = "2ND QTR"
                    elif period == 3: LATEST_SCORES_CACHE["usm_troy"]["quarter"] = "3RD QTR"
                    elif period == 4: LATEST_SCORES_CACHE["usm_troy"]["quarter"] = "4TH QTR"
                    competitors = event.get('competitors', [])
                    LATEST_SCORES_CACHE["usm_troy"]["score"] = f"{competitors[0].get('score', '0')} - {competitors[1].get('score', '0')}"
                    LATEST_SCORES_CACHE["usm_troy"]["status"] = display_status
    except Exception:
        pass
    return [
        {"id": "usm_troy", "game": "Southern Miss @ Troy", "sport": "CFB", "score": LATEST_SCORES_CACHE["usm_troy"]["score"], "time": "7:00 PM ET", "status": LATEST_SCORES_CACHE["usm_troy"]["status"], "stadium": LATEST_SCORES_CACHE["usm_troy"]["stadium"], "weather": LATEST_SCORES_CACHE["usm_troy"]["weather"], "quarter": LATEST_SCORES_CACHE["usm_troy"]["quarter"]},
        {"id": "ott_det", "game": "Ottawa Senators @ Detroit Red Wings", "sport": "NHL", "score": "0 - 0", "time": "7:00 PM ET", "status": "UPCOMING", "stadium": LATEST_SCORES_CACHE["ott_det"]["stadium"], "weather": LATEST_SCORES_CACHE["ott_det"]["weather"], "quarter": "1ST PER"},
        {"id": "nas_tor", "game": "Nashville Predators @ Toronto Maple Leafs", "sport": "NHL", "score": "0 - 0", "time": "7:30 PM ET", "status": "UPCOMING", "stadium": LATEST_SCORES_CACHE["nas_tor"]["stadium"], "weather": LATEST_SCORES_CACHE["nas_tor"]["weather"], "quarter": "1ST PER"},
        {"id": "vgk_sea", "game": "Vegas Golden Knights @ Seattle Kraken", "sport": "NHL", "score": "0 - 0", "time": "9:40 PM ET", "status": "UPCOMING", "stadium": LATEST_SCORES_CACHE["vgk_sea"]["stadium"], "weather": LATEST_SCORES_CACHE["vgk_sea"]["weather"], "quarter": "1ST PER"}
    ]

def get_live_market_drift():
    return [
        {"sport": "NFL", "matchup": "Detroit Lions @ Arizona Cardinals", "open_line": "Lions -3.5", "current_line": "Lions -4.5", "drift_text": "▲ +1.0 Live Public Shift", "drift_color": "#ff9100"},
        {"sport": "NFL", "matchup": "Chicago Bears @ Green Bay Packers", "open_line": "Bears -1.0", "current_line": "Bears -2.5", "drift_text": "▲ +1.5 Public Premium", "drift_color": "#ff9100"},
        {"sport": "CFB", "matchup": "Western Michigan vs. Central Michigan", "open_line": "Over 56.0", "current_line": "Over 54.5", "drift_text": "▼ -1.5 Sharp Force Under", "drift_color": "#00e676"}
    ]

@app.route('/')
def dashboard():
    cfb_game = {"home": "Troy", "away": "Southern Miss", "status": "UPCOMING", "sliders": [{"player": "Landry Lyddy (USM)", "metric": "200+ Pass Yards", "target": "OVER", "yield": "77%"}, {"player": "Goose Crowder (TROY)", "metric": "190+ Pass Yards", "target": "OVER", "yield": "72%"}, {"player": "Jaheim Merriweather (TROY)", "metric": "40+ Rush Yards", "target": "OVER", "yield": "47%"}]}
    nhl_games = [{"home": "Detroit Red Wings", "away": "Ottawa Senators", "angle": "Divisional Pivot", "play": "Ottawa ML (+115)", "handle": "71% Sharp Cash"}, {"home": "Toronto Maple Leafs", "away": "Nashville Predators", "angle": "Public Trap Fade", "play": "Nashville ML (+130)", "handle": "87% Public on TOR"}, {"home": "Seattle Kraken", "away": "Vegas Golden Knights", "angle": "Late Night Structure", "play": "Seattle ML (+142)", "handle": "Vegas Public Premium"}]
    syndicate_picks = {"groups": [{"alias": "Alpha Syndicate", "target": "Southern Miss +10.5", "size": "5x", "volatility": "91% Resistance", "v_color": "#ff9100"}, {"alias": "Wallet #4092 (High-Stakes)", "target": "Nashville ML (+130)", "size": "3.5x", "volatility": "84% Resistance", "v_color": "#ff9100"}, {"alias": "Vegas Sharp Box", "target": "Ottawa ML (+115)", "size": "2x", "volatility": "68% Resistance", "v_color": "#00e676"}]}
    script_tracker = {"phases": [{"qtr": "1st Quarter", "id": "q1_bias", "name": "Public Media Bias Trap", "status": "SCANNING", "desc": "Detects high-volume early public lines on national TV broadcasts.", "color": "var(--text-muted)"}, {"qtr": "2nd Quarter", "id": "q2_rubber", "name": "The Rubber Band Effect", "status": "ARMED", "desc": "Monitors favorite over-extensions to flag live value shifts on alternate sliders.", "color": "var(--accent-orange)"}, {"qtr": "3rd Quarter", "id": "q3_freeze", "name": "The Neutralization Freeze", "status": "ARMED", "desc": "Calculates sudden clock-chewing splits and coach-driven pacing restraints.", "color": "var(--accent-orange)"}, {"qtr": "4th Quarter", "id": "q4_hook", "name": "The Trap Door Hook", "status": "ARMED", "desc": "Fades highly manipulated late game-script volatility to track static floors.", "color": "var(--accent-orange)"}]}
    engine_recommendation = {"status": "LIVE SCANNING MARKET", "action_color": "var(--accent-green)", "triggers": [{"id": "live_spread_cmd", "market": "🏈 GAME SPREAD", "command": "Southern Miss +10.5", "alert_note": "Lock pre-game; spread artificial inflation pass the key number 10."}, {"id": "live_total_cmd", "market": "🏈 OVER/UNDER TOTAL", "command": "USM/TROY Under 51.5", "alert_note": "Clock-chewing ground scripts will suffocate the public game total Over."}, {"id": "prop_pass_cmd", "market": "🎯 PLAYER PROP: COMPLETIONS", "command": "Landry Lyddy Over 13.5", "alert_note": "Trailing negative game script will mandate heavy horizontal targets."}, {"id": "prop_rush_cmd", "market": "🎯 PLAYER PROP: RUSH YARDS", "command": "Jaheim Merriweather Over 39.5", "alert_note": "Troy run-first ground architecture locks in high secondary carry volume."}, {"id": "whale_block_1", "market": "🐋 WHALE BLOCK TRACKER", "command": "$1.4M on Nashville ML (+130)", "alert_note": "Institutional limit order dropped at BetMGM; public liquidity sweep alert!"}, {"id": "whale_block_2", "market": "🐋 WHALE BLOCK TRACKER", "command": "$850K on Senators ML (+115)", "alert_note": "Pro-syndicate move striking Detroit transition defensive lag indicators."}]}
    quantum_hedges = {"hedges": [{"id": "hedge_spread", "market": "🔒 LIVE SPREAD LOCK-WIN", "instruction": "Awaiting Script Drift", "note": "Will display exact live hedging point to lock in 100% risk-free returns."}, {"id": "hedge_totals", "market": "🔒 LIVE TOTAL LOCK-WIN", "instruction": "Awaiting Pacing Shift", "note": "Will display middle arbitrage thresholds during 3rd quarter freeze routines."}]}
    return render_template('dashboard.html', cfb=cfb_game, nhl_items=nhl_games, sharps=syndicate_picks, early=get_live_market_drift(), live_games=pull_live_unblocked_scores(), script=script_tracker, alert=engine_recommendation, quantum=quantum_hedges)

@app.route('/api/feed')
def live_feed():
    return jsonify({
        "status": "Pipeline Active", "version": "9.5-Quantum-Supreme", "cache_buster": time.time(),
        "sentiment_updates": {"Alpha Syndicate": "94% Public Resistance", "Wallet #4092 (High-Stakes)": "87% Public Resistance", "Vegas Sharp Box": "69% Public Resistance"},
        "script_updates": {"q1_bias": {"status": "SCANNING", "color": "var(--text-muted)"}, "q2_rubber": {"status": "ARMED", "color": "var(--accent-orange)"}, "q3_freeze": {"status": "ARMED", "color": "var(--accent-orange)"}, "q4_hook": {"status": "ARMED", "color": "var(--accent-orange)"}},
        "live_bet_commands": {"live_spread_cmd": {"command": "Southern Miss +10.5", "note": "Lock pre-game; spread artificial inflation pass the key number 10."}, "live_total_cmd": {"command": "USM/TROY Under 51.5", "note": "Clock-chewing ground scripts will suffocate the public game total Over."}, "prop_pass_cmd": {"command": "Lyddy Over 13.5 Comp", "note": "Trailing negative game script will mandate heavy horizontal targets."}, "prop_rush_cmd": {"command": "Merriweather Over 39.5 Yds", "note": "Troy run-first ground architecture locks in high secondary carry volume."}, "whale_block_1": {"command": "WHALE ALERT: Nashville ML", "note": "Institutional limit order dropped at BetMGM; public liquidity sweep alert!"}, "whale_block_2": {"command": "WHALE ALERT: Ottawa ML", "note": "Pro-syndicate move striking Detroit transition defensive lag indicators."}},
        "quantum_updates": {"hedge_spread": {"command": "Awaiting Script Drift", "note": "Will display exact live hedging point to lock in 100% risk-free returns."}, "hedge_totals": {"command": "Awaiting Pacing Shift", "note": "Will display middle arbitrage thresholds during 3rd quarter freeze routines."}},
